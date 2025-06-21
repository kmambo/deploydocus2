import abc
import base64
import enum
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Callable, Optional, Self, cast

from kubernetes_asyncio.models import (
    IntstrIntOrString,
    V1Container,
    V1ContainerPort,
    V1DeploymentSpec,
    V1HTTPGetAction,
    V1LabelSelector,
    V1PodSpec,
    V1PodTemplateSpec,
    V1Probe,
)
from kubernetes_asyncio.models import V1ObjectMeta, V1ServicePort, V1ServiceSpec
from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    SecretStr,
    model_validator,
)

from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.model_partials import ConfigMap, Deployment, Secret, Service
from deploydocus2.pkg import InstanceSettings, K8sComponentModel
from deploydocus2.types import (
    ConfigMapSequence,
    CronJobSequence,
    DeploymentSequence,
    HorizontalPodAutoscalerSequence,
    IngressSequence,
    JobSequence,
    NamespaceSequence,
    ResourceQuotaSequence,
    SecretSequence,
    ServiceAccountSequence,
    ServiceSequence,
)


class HttpProbe(BaseModel):
    """Represents a probe - an HTTP endpoint that the Kubernetes control plane will
    issue HTTP GET requests and if the the HTTP server inside the main pod's container
     returns a 2XX status,"""

    _default_url: str | None = None

    def __init_subclass__(cls, /, default_url=None, **kwargs):
        cls._default_url = default_url
        super().__init_subclass__(**kwargs)

    rel_url: str | None = Field(
        None,
        description="The relative URL the Kubernetes will "
        "periodically issue HTTP GET requests to.",
    )
    check_freq: int | None = Field(
        default=None,
        description="The frequency of liveness checks (in secs). This is ignored if "
        "liveness is unset. If unset, defaults to 10 seconds.",
    )

    @model_validator(mode="after")
    def model_validate_after(self) -> Self:
        self.rel_url = self.rel_url or self._default_url
        return self


class HttpLivenessProbe(HttpProbe, default_url="/livez"):
    delay_first_probe: int | None = Field(
        None,
        description="If set, wait these many seconds before starting to probe the "
        "container.",
    )


class HttpReadinessProbe(HttpProbe, default_url="/readyz"):
    pass


class HttpStartupProbe(HttpProbe, default_url="/startz"):
    pass


class RuleType(enum.StrEnum):
    prefix = "Prefix"
    exact = "Exact"
    implementation_specific = "ImplementationSpecific"


class HttpIngressRule(BaseModel):
    """Represents a HTTP route matching rule. For a route to match, both the host
    field and path fields must 'match'."""

    host: str | None = Field(
        None,
        description="Set to None regardless of the `Host` "
        "header in the incoming HTTP request",
    )
    path: str = Field(
        description="For a prefix matching, must end with a /* . "
        "Otherwise assumed to be an exact match. "
        "See docs for examples"
    )
    implementation_specific: bool = Field(
        default=False, description="Set to True if you want the path rule to "
    )
    ingress_class_name: str | None = Field(
        default=None,
        description="The name of the ingress class. Leave it at None if you want to use"
        " the default class. Unless ",
    )


def mk_upper_case(key: str) -> str:
    """Converts a key to uppercase. Typically used to convert a lower-case key to
    uppercase and expose as an environment variable. so a key 'client-id' becomes an
    env var 'CLIENT_ID' (Note the changing of the minus to an underscore)

    Args:
        key: The key to convert.

    Returns:

    """
    return key.upper().replace("-", "_")


class KeysMapper(abc.ABC):
    _key_mapper_fn: Callable[[str], str] = lambda x: x

    @property
    def keys_mapper(self) -> Callable[[str], str]:
        return self._key_mapper_fn

    @keys_mapper.setter
    def keys_mapper(self, transformer: Callable[[str], str]):
        """Used to set a function which is used to change how the the KV-pairs'
        keys are exposed. Typically used to change keys such as 'client-id' to
        'CLIENT_ID' before exposing as environment variables.

        Args:
            transformer:

        Returns:

        """
        self._key_mapper_fn = transformer

    @abc.abstractmethod
    def map_keys(self) -> Mapping[str, str]: ...


class KeyValuePairsNonSensitive(BaseModel, KeysMapper):
    """Becomes a Kubernetes ConfigMap which exposes these KV-pairs as either
    environment variables or as files mounted on the container's as a volume on a given
    path. Note: do not use this for any sensitive  info such as passwords, SSL private
    keys, SSN etc. There are different classes to handle sensitive information.
    """

    kv_pairs: Mapping[str, str] = Field(description="The key-value pairs")
    mount_path: Path | None = Field(
        None,
        description="Leave it unset (None) if you want to expose "
        "these as environment variables. Otherwise, the KV-pairs are exposed under "
        "the directory specified by this field. The keys becomes the filenames and "
        "the values become the file contents",
    )
    name: str | None = Field(
        None,
        description="A unique name of the KV-pair. Leave it unset and a default name "
        "will be supplied.",
    )

    def map_keys(self) -> Mapping[str, str]:
        return {
            (self.keys_mapper(k)): v
            for k, v in self.kv_pairs.items()
            if self.keys_mapper(k)
        }

    def generate_config_map(
        self,
        namespace: str,
        *,
        annotations: dict[str, str] | None = None,
        labels: dict[str, str] | None = None,
    ) -> ConfigMap:
        _kv_xform = self.map_keys()

        return ConfigMap(
            data=_kv_xform,
            metadata=V1ObjectMeta(
                name=self.name,
                namespace=namespace,
                annotations=annotations or {},
                labels=labels or {},
            ),
        )


def encode_secret_data(value: str) -> SecretStr:
    return SecretStr(base64.b64encode(value.encode("utf-8")).decode("utf-8"))


class KeyValuePairsSensitive(KeyValuePairsNonSensitive):
    kv_pairs: Annotated[dict[str, str], AfterValidator(encode_secret_data)]


class KeyValuePairsSecretsExtSrc(BaseModel, KeysMapper):
    """Becomes a Kubernetes secret. Exposes these KV-pairs as either environment
    variables or as files mounted on the container's as a volume on a given path.
    """

    secrets_key_mapping: dict[str, str] = Field(
        description="This is to control which entries are exposed in the Kubernetes "
        "namespace and what keys they will be exposed as. For example, "
        " if your secrets in Vault KV store has 2 secrets as "
        "{'key1': 'value1' ,'key2': 'value2'}, and you only want to "
        "expose 'value2' as an environment variable 'MY_TERRIBLE_SECRET' "
        "then you will need this field to be {'key2': 'MY_TERRIBLE_SECRET'} "
    )

    def map_keys(self) -> Mapping[str, str]:
        return {(self.keys_mapper(k)): v for k, v in self.secrets_key_mapping.items()}

    def generate_secrets_mapping(self, metadata: V1ObjectMeta | None = None):
        _kv_xform = self.map_keys()
        return Secret(data=_kv_xform, type="Opaque", metadata=metadata)


class SimpleHttpApplication(DeploydocusComponent):
    """Represents a simple HTTP(s) application which generates a single Kubernetes
    service, a deployment and an ingress object or a Gateway API.
    """

    app_name: str | None = Field(
        None,
        description="(Recommended) The application name. Don't make it overly "
        "long because it forms the basis of other kubernetes "
        "objects' names such deployments and services and they "
        "may become too long and fail to be created.",
    )
    instance_name: str | None = Field(
        None,
        description="Normally not required to be set. Set this only if you need to "
        "deploy another instance of the same application in the same "
        "namespace. Otherwise it gets set automatically to be the same as "
        "`app_name`.",
    )
    version: str = Field(description="A semver-ed version number.")
    namespace: str = Field(
        description="The cluster namespace in which to deploy the application."
    )
    app_image: str = Field(
        description="The fully tagged image to run. Something like "
        "'gcr.io/kaniko-project/executor:v1.23.2'"
    )
    app_command: Optional[list[str]] = Field(
        None,
        description="Command to run in the application container instead of the default"
        " command. Only one of app_entrypoint_args or app_command must be "
        "set. If you want the default container entrypoint/command to"
        " be run, don't set either. Provide it as a string-array without spaces. So, "
        "if the command in the container application was meant to be "
        "'application_exec --env1=arg1 --env2=arg2', "
        "then set this field to ['application_exec', '--env1=arg1', '--env2=arg2']",
    )
    app_entrypoint_args: Optional[list[str]] = Field(
        None,
        description="The arguments passed to container's entrypoint. Only one of "
        "app_entrypoint_args or app_command must be set. If you want the "
        "default container entrypoint/command to be run, don't set either."
        "Provide it as a string-array without spaces. So, "
        "if the args to te the container application was meant to be "
        "'--env1=arg1 --env2=arg2', "
        "then set this field to ['--env1=arg1', '--env2=arg2']",
    )
    app_config_non_sensitive: KeyValuePairsNonSensitive | None = Field(
        None,
        description="Provides (non-sensitive) configuration information for the "
        "application either as environment variables or as files mounted"
        " for the container.",
    )
    app_config_secrets: KeyValuePairsSecretsExtSrc | None = Field(
        None,
        description="Provides sensitive configuration information for the application."
        " Usually it is from an external source like Vault KV engine.",
    )
    replicas: int | None = Field(
        None, description="Number of application instances to run in parallel."
    )
    http_named_ports: dict[str, int] = Field(
        default={"http": 8080, "https": 8443},
        description=r"The ports used by the application's container. e.g. "
        r"{'http': 8080, 'https': 8443}. Neither port names nor their "
        r"corresponding port numbers can be repeated.",
    )

    # container probes
    startup_probe: HttpStartupProbe | None = Field(
        None,
        description="Use only for slow starting containers. It disables liveness and "
        "readiness checks until it succeeds.",
    )
    liveness_probe: Optional[HttpLivenessProbe] = Field(
        HttpLivenessProbe(),
        description="Determines when a container is ready to start accepting traffic. "
        "If a container fails its liveness probe repeatedly, it is "
        "presumed dead and thus restarted. By convention, it is '/livez'. "
        "Set to None to disable liveness probe.",
    )
    readiness_probe: Optional[HttpReadinessProbe] = Field(
        HttpReadinessProbe(),
        description="Determines when a container is ready to start accepting traffic."
        " If a container fails its readiness probe , traffic is not "
        "directed to it. By convention, it is '/readyz'. Set to None to "
        "disable readiness probe.",
    )
    service_ports: dict[str, int] = Field(
        description="Must have the same keys as the `http_named_ports` field. "
        "Maps ports with the same name to the corresponding port numbers in the "
        "application container."
    )
    ingress: HttpIngressRule | None = Field(
        None,
        description="A single HTTP routing rule. Set to None if you don't "
        "need to expose this to the internet",
    )

    @model_validator(mode="after")
    def validate_after(self: Self) -> Self:
        assert not (self.app_entrypoint_args and self.app_command), (
            "Both app_entrypoint_args and app_command must be not be set, at least "
            "one should be None"
        )
        if not self.app_name:
            self.app_name = self.__class__.__name__

        return self

    def gen_k8s_components(self) -> "K8sComponentModel":
        return HttpK8sComponentsModel(
            pkg_name=self.app_name,
            pkg_version=self.version,
            instance_settings=InstanceSettings(
                name=self.instance_name, namespace=self.namespace
            ),
            hl_class=self,
        )


class HttpK8sComponentsModel(K8sComponentModel):
    hl_class: SimpleHttpApplication

    def render_namespaces(
        self,
    ) -> NamespaceSequence:
        """Since workload deployers are not expected to create namespaces (the
            namespace will be created by the cluster operator aka cluster admin),
            this just return an empty sequence.

        Returns:
            An empty sequence

        """
        return []

    def render_resourcequotas(
        self,
    ) -> ResourceQuotaSequence:
        """Since resource quotas are set by the cluster operator, application deployers
         don't have to worry about this. Override this method if you want to

        Returns:
            An empty sequence
        """
        return []

    def render_configmaps(
        self,
    ) -> ConfigMapSequence:
        """rendered from

        Returns:

        """
        if self.hl_class.app_config_secrets is None:
            return []
        ret = cast(
            KeyValuePairsNonSensitive, self.hl_class.app_config_non_sensitive
        ).generate_config_map(
            namespace=self.instance_settings.namespace,
            labels=cast(dict[str, str], self.default_selectors),
        )
        return [ret]

    def render_secrets(
        self,
    ) -> SecretSequence:
        return (
            [self.hl_class.app_config_secrets.generate_secrets_mapping()]
            if self.hl_class.app_config_secrets
            else []
        )

    def render_services(
        self,
    ) -> ServiceSequence:
        meta = V1ObjectMeta(
            name=f"{self.instance_settings.name}-svc",
            namespace=self.instance_settings.namespace,
        )
        ports = [
            V1ServicePort(protocol="TCP", port=80, targetPort=port)
            for port in self.hl_class.service_ports
        ]
        spec = V1ServiceSpec(
            selector=self.default_selectors,
            ports=ports,
        )
        ret = Service(
            service_ports=self.hl_class.service_ports,
            metadata=meta,
            spec=spec,
        )
        return [ret]

    def render_deployments(
        self,
    ) -> DeploymentSequence:
        pod_labels = self.default_labels
        deployment_meta = V1ObjectMeta(
            name=f"{self.instance_settings.name}-{self.pkg_name}",
            namespace=self.instance_settings.namespace,
            labels=pod_labels,
        )
        podspec = V1PodTemplateSpec(
            metadata=V1ObjectMeta(
                labels=pod_labels,
            ),
            spec=V1PodSpec(
                automountServiceAccountToken=False,
                serviceAccountName=f"{self.instance_settings.name}-{self.pkg_name}-sa",
                containers=[
                    V1Container(
                        name=self.hl_class.app_name,
                        image=self.hl_class.app_image,
                        imagePullPolicy="Always",
                        command=self.hl_class.app_command,
                        args=self.hl_class.app_entrypoint_args,
                        ports=[
                            V1ContainerPort(
                                protocol="TCP", container_port=port_no, name=port_name
                            )
                            for port_name, port_no in self.hl_class.http_named_ports.items()  # noqa: E501
                        ],
                        livenessProbe=(
                            V1Probe(
                                httpGet=V1HTTPGetAction(
                                    path=self.hl_class.liveness_probe.rel_url,
                                    port=IntstrIntOrString("http"),
                                ),
                                initial_delay_seoonds=self.hl_class.liveness_probe.delay_first_probe,  # noqa
                                period_seconds=self.hl_class.liveness_probe.check_freq,
                            )
                            if self.hl_class.liveness_probe
                            else None
                        ),
                        readinessProbe=(
                            (
                                V1Probe(
                                    httpGet=V1HTTPGetAction(
                                        path=self.hl_class.readiness_probe.rel_url,
                                        port=IntstrIntOrString("http"),
                                    )
                                )
                            )
                            if self.hl_class.readiness_probe
                            else None
                        ),
                        startupProbe=(
                            (
                                V1Probe(
                                    httpGet=V1HTTPGetAction(
                                        path=self.hl_class.startup_probe.rel_url,
                                        port=IntstrIntOrString("http"),
                                    )
                                )
                            )
                            if self.hl_class.startup_probe
                            else None
                        ),
                    )
                ],
            ),
        )
        deployment_spec = V1DeploymentSpec(
            template=podspec,
            replicas=self.hl_class.replicas,
            selector=V1LabelSelector(matchLabels=self.default_selectors),
        )
        deploy = Deployment(metadata=deployment_meta, spec=deployment_spec)
        return [deploy]

    def render_horizontalpodautoscalers(
        self,
    ) -> HorizontalPodAutoscalerSequence:
        return super().render_horizontalpodautoscalers()

    def render_jobs(
        self,
    ) -> JobSequence:
        return super().render_jobs()

    def render_cronjobs(
        self,
    ) -> CronJobSequence:
        return super().render_cronjobs()

    def render_ingresses(
        self,
    ) -> IngressSequence:
        return super().render_ingresses()

    def render_serviceaccounts(
        self,
    ) -> ServiceAccountSequence:
        return super().render_serviceaccounts()
