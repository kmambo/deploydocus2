import enum
from collections import ChainMap
from pathlib import Path
from typing import Optional, Self, Sequence, cast

import pydantic
from kubernetes import (
    IntstrIntOrString,
    V1ConfigMap,
    V1Container,
    V1ContainerPort,
    V1DeploymentSpec,
    V1HTTPGetAction,
    V1HTTPIngressPath,
    V1HTTPIngressRuleValue,
    V1IngressBackend,
    V1IngressRule,
    V1IngressServiceBackend,
    V1IngressSpec,
    V1LabelSelector,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
    V1Probe,
    V1Secret,
    V1ServicePort,
    V1ServiceSpec,
)
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

from deploydocus2._types import (
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
from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.model_partials import Deployment, Ingress, Service
from deploydocus2.pkg import InstanceSettings, K8sComponentsModel

from .utils import (
    _Config,
    _ConfigSecret,
    to_config_map,
    to_secret,
    volume_mount_config_map_or_secret,
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
    PREFIX = "Prefix"
    EXACT = "Exact"
    IMPLEMENTATION_SPECIFIC = "ImplementationSpecific"


class HttpIngressRule(BaseModel):
    """Represents a HTTP route matching rule. For a route to match, both the host
    field and path fields must 'match'."""

    path: str = Field(
        description="For a prefix matching, must end with a /* . "
        "Otherwise assumed to be an exact match. "
        "See docs for examples"
    )
    path_type: RuleType = Field(
        default=RuleType.PREFIX, description="The type of path match. "
    )


class HttpIngressHostWithRules(BaseModel):
    host: str | None = Field(
        None,
        description="Set to None regardless of the `Host` "
        "header in the incoming HTTP request",
    )
    ingress_class_name: str | None = Field(
        default=None,
        description="(Recommended) The name of the ingress class. Leave it at None if "
        "you want to use the default class. The application developer is "
        "not expected to setup the Ingress class, that is the cluster "
        "operator's burden.",
    )
    rules: Sequence[HttpIngressRule] = Field(
        description="Set of rules to match against the host."
    )

    @model_validator(mode="after")
    def model_validate_after(self) -> Self:
        assert self.rules
        return self


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
        validate_default=True,
    )
    instance_name: str | None = Field(
        None,
        description="Normally not required to be set. Set this only if you need to "
        "deploy another instance of the same application in the same "
        "namespace. Otherwise it gets set automatically to be the same as "
        "`app_name`.",
        validate_default=True,
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
    app_config_non_sensitive: dict[str, _Config] | None = Field(
        None,
        description="Provides (non-sensitive) configuration information for the "
        "application either as environment variables or as files mounted"
        " for the container. Since, sometimes, multiple configurations are provided "
        "for the application (usually because they are mounted at different "
        "directories), this field is a dictionary with keys that serve as unique names "
        "in the application container's context.",
    )
    config_map_mount_path: dict[Path, str] | None = Field(
        None,
        description="Mount the named-config in the field `app_config_non_sensitive` "
        "to this path.",
    )
    app_config_secrets: dict[str, _ConfigSecret] | None = Field(
        None,
        description="Provides sensitive configuration information for the application."
        " Usually it is from an external source like Vault KV engine.",
    )
    secrets_mount_path: dict[Path, str] | None = Field(
        None,
        description="Mount the named-secret in the field `app_config_secrets` "
        "to this path.",
    )
    replicas: int | None = Field(
        None,
        description="Number of application instances to run in parallel. "
        "If left unset, a single replica will be created. (This field itself will be "
        "None).",
    )
    http_named_ports: dict[str, int] = Field(
        default={
            "http": 8080,
        },
        description=r"The ports used by the application's container. e.g. "
        r"{'http': 8080, 'https': 8443}. Neither port names nor their "
        r"corresponding port numbers can be repeated.",
    )

    # container probes
    startup_probe: HttpStartupProbe | None = Field(
        None,
        description="Most HTTP microservices don't need this."
        "Use only for slow starting containers. It disables liveness and "
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
    app_ports: dict[str, int] | None = Field(
        description="Must have the same keys as the `http_named_ports` field. "
        "Maps ports with the same name to the corresponding port numbers in the "
        "application container.",
        default=None,
    )
    ingress: HttpIngressHostWithRules | None = Field(
        None,
        description="A single HTTP host with routing rules. Set to None if you don't "
        "need to expose this application to the internet. See "
        "https://kubernetes.io/docs/concepts/services-networking/ingress"
        "/#single-service-ingress",
    )

    @model_validator(mode="after")
    def validate_after(self: Self) -> Self:
        assert not (self.app_entrypoint_args and self.app_command), (
            "Both app_entrypoint_args and app_command must be not be set, at least "
            "one should be None"
        )
        if not self.app_name:
            self.app_name = self.__class__.__name__
        if not self.instance_name:
            self.instance_name = self.app_name

        if self.app_ports is None:
            self.app_ports = self.http_named_ports

        assert self.app_ports.keys() <= self.http_named_ports.keys(), (
            f"There are ports defined in the app service abstraction that "
            f"are not present in the container. "
            f"{self.http_named_ports.keys() - self.app_ports.keys()}"
        )

        return self

    def gen_k8s_components(self) -> "K8sComponentsModel":
        return HttpK8sComponentsModel(
            pkg_name=self.app_name,
            pkg_version=self.version,
            instance_settings=InstanceSettings(
                name=f"{self.instance_name}-{self.app_name}", namespace=self.namespace
            ),
            hl_class=self,
        )


class HttpK8sComponentsModel(K8sComponentsModel):
    hl_class: SimpleHttpApplication = pydantic.Field(
        description="A sane template class for HTTP applications to be defined; "
        "from which to derive Kubernetes objects which can be applied to "
        "a single namespace in a cluster to run an HTTP application."
    )
    _config_maps: list[V1ConfigMap] | None = None
    _secrets: list[V1Secret] | None = None

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
        if self.hl_class.app_config_non_sensitive is None:
            return []
        self._config_maps = [
            to_config_map(
                name=f"{k}",
                namespace=self.instance_settings.namespace,
                labels=cast(dict[str, str], self.default_selectors),
                cfg=cfg,
            )
            for k, cfg in self.hl_class.app_config_non_sensitive.items()
        ]

        return self._config_maps

    def render_secrets(
        self,
    ) -> SecretSequence:
        if self.hl_class.app_config_secrets is None:
            return []
        self._secrets = [
            to_secret(
                cfg_secret=cfg,
                name=f"{k}",
                namespace=self.instance_settings.namespace,
                labels=cast(dict[str, str], self.default_selectors),
            )
            for k, cfg in self.hl_class.app_config_secrets.items()
        ]

        return self._secrets

    def render_services(
        self,
    ) -> ServiceSequence:
        meta = V1ObjectMeta(
            name=f"{self.instance_settings.name}-svc",
            namespace=self.instance_settings.namespace,
        )
        ports = [
            V1ServicePort(
                protocol="TCP",
                port=80,
                target_port=IntstrIntOrString(actual_instance=port),
            )
            for port in cast(dict[str, int], self.hl_class.app_ports)
        ]
        spec = V1ServiceSpec(
            selector=self.default_selectors,
            ports=ports,
        )
        ret = Service(
            service_ports=self.hl_class.app_ports,
            metadata=meta,
            spec=spec,
        )
        return [ret]

    def render_deployments(
        self,
    ) -> DeploymentSequence:
        """

        Returns:

        """
        pod_labels = self.default_labels

        deployment_meta = V1ObjectMeta(
            name=f"{self.instance_settings.name}-{self.pkg_name}",
            namespace=self.instance_settings.namespace,
            labels=pod_labels,
        )

        # d = cast(_Config, self.hl_class.app_config_non_sensitive)
        # mnt_paths = [
        #     (
        #         d[cast(str, cast(V1ObjectMeta, cm.metadata).name)].mount_path or "_",
        #         cm,
        #     )
        #     for cm in cfg_maps
        # ]
        #
        # volume_mounts = [
        #     V1VolumeMount(
        #         name=cast(V1ObjectMeta, cm.metadata).name,
        #         mount_path=mnt_pth if mnt_pth != "_" else None,
        #     )
        #     for mnt_pth, cm in mnt_paths
        # ]
        liveness_probe = (
            V1Probe(
                httpGet=V1HTTPGetAction(
                    path=self.hl_class.liveness_probe.rel_url,
                    port=IntstrIntOrString(actual_instance="http"),
                ),
                initial_delay_seconds=self.hl_class.liveness_probe.delay_first_probe,
                # noqa
                period_seconds=self.hl_class.liveness_probe.check_freq,
            )
            if self.hl_class.liveness_probe
            else None
        )
        readines_probe = (
            (
                V1Probe(
                    httpGet=V1HTTPGetAction(
                        path=self.hl_class.readiness_probe.rel_url,
                        port=IntstrIntOrString(actual_instance="http"),
                    )
                )
            )
            if self.hl_class.readiness_probe
            else None
        )
        startup_probe = (
            (
                V1Probe(
                    httpGet=V1HTTPGetAction(
                        path=self.hl_class.startup_probe.rel_url,
                        port=IntstrIntOrString(actual_instance="http"),
                    )
                )
            )
            if self.hl_class.startup_probe
            else None
        )
        container = V1Container(
            name=self.hl_class.app_name,
            image=self.hl_class.app_image,
            image_pull_policy="Always",
            command=self.hl_class.app_command,
            args=self.hl_class.app_entrypoint_args,
            # volume_mounts=volume_mounts,
            ports=[
                V1ContainerPort(protocol="TCP", container_port=port_no, name=port_name)
                for port_name, port_no in self.hl_class.http_named_ports.items()
                # noqa: E501
            ],
            liveness_probe=liveness_probe,
            readiness_probe=readines_probe,
            startup_probe=startup_probe,
        )
        pod_spec = V1PodSpec(
            automountServiceAccountToken=False,
            serviceAccountName=f"{self.instance_settings.name}-{self.pkg_name}-sa",
            containers=[container],
        )

        for cfg_map in (self._secrets or []) + (self._config_maps or []):
            for path, cfg_map_name in ChainMap(
                self.hl_class.config_map_mount_path or {},
                self.hl_class.secrets_mount_path or {},
            ).items():
                if cast(V1ObjectMeta, cfg_map.metadata).name == cfg_map_name:
                    volume_mount_config_map_or_secret(
                        pod_spec=pod_spec,
                        path=path,
                        config_map_name=cast(V1ObjectMeta, cfg_map.metadata).name,
                        container_name=container.name,
                        secret_name=None,
                        volume_name=f"{cfg_map_name}-vol-cfg",
                    )

        pod_tmpl_spec = V1PodTemplateSpec(
            metadata=V1ObjectMeta(
                labels=pod_labels,
            ),
            spec=pod_spec,
        )
        deployment_spec = V1DeploymentSpec(
            template=pod_tmpl_spec,
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
        if not self.hl_class.ingress:
            return []
        else:
            svc_backend = self.render_services()[0]
            return [
                Ingress(
                    metadata=V1ObjectMeta(
                        namespace=self.instance_settings.namespace,
                        name=f"{self.instance_settings.name}-{self.pkg_name}-ingress",
                    ),
                    spec=V1IngressSpec(
                        rules=[
                            V1IngressRule(
                                host=self.hl_class.ingress.host,
                                http=V1HTTPIngressRuleValue(
                                    paths=[
                                        V1HTTPIngressPath(
                                            path_type=r.path_type.value,
                                            path=r.path,
                                            backend=V1IngressBackend(
                                                service=V1IngressServiceBackend(
                                                    name=cast(
                                                        str,
                                                        cast(
                                                            V1ObjectMeta,
                                                            svc_backend.metadata,
                                                        ).name,
                                                    )
                                                )
                                            ),
                                        )
                                        for r in (self.hl_class.ingress.rules or [])
                                    ]
                                ),
                            )
                        ],
                        ingress_class_name=self.hl_class.ingress.ingress_class_name,
                    ),
                )
            ]

    def render_serviceaccounts(
        self,
    ) -> ServiceAccountSequence:
        return super().render_serviceaccounts()
