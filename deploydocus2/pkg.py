import itertools
import logging
from functools import wraps
from typing import LiteralString, Self

import pydantic as pyd

from .types import (
    SUPPORTED_KINDS,
    APIServiceSequence,
    ClusterRoleBindingSequence,
    ClusterRoleSequence,
    ConfigMapSequence,
    CronJobSequence,
    CustomResourceDefinitionSequence,
    DaemonSetSequence,
    DeploymentSequence,
    HorizontalPodAutoscalerSequence,
    IngressSequence,
    JobSequence,
    LabelsDict,
    LabelsSelector,
    LimitRangeSequence,
    ManifestSequence,
    NamespaceSequence,
    NetworkPolicySequence,
    PersistentVolumeClaimSequence,
    PersistentVolumeSequence,
    PodDisruptionBudgetSequence,
    PodSequence,
    ReplicaSetSequence,
    ReplicationControllerSequence,
    ResourceQuotaSequence,
    RoleBindingSequence,
    RoleSequence,
    SecretSequence,
    ServiceAccountSequence,
    ServiceSequence,
    StatefulSetSequence,
    StorageClassSequence,
)

logger = logging.getLogger(__name__)

DEPLOYDOCUS_DOMAIN: LiteralString = "deploydocus.io"


class InstanceSettings(pyd.BaseModel):
    instance_name: str
    instance_version: str
    instance_namespace: str
    image_name_with_tag: str | None = None


def autosort(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        ret: ManifestSequence = f(*args, **kwargs)
        ret.sort(
            key=lambda obj: list(SUPPORTED_KINDS).index(
                obj["kind"] if isinstance(obj, dict) else obj.kind
            )
        )
        return ret

    return wrapped


class K8sModel(pyd.BaseModel):
    """
    This is created by a Component
    """

    pkg_name: str = pyd.Field(default="", description="A name of this application")
    pkg_version: str = pyd.Field(
        description="Provide a version number for the application. This is independent"
        " of the individual components  of the application"
    )
    instance_settings: InstanceSettings

    @pyd.model_validator(mode="after")
    def validate_after(self: Self) -> Self:
        if not self.pkg_name:
            self.pkg_name = self.__class__.__name__
        return self

    @property
    def default_labels(self) -> LabelsDict:
        """Override this if you need to. The default labels which are generated
        and can and should be applied to the mani"""
        return {
            "app.kubernetes.io/name": self.pkg_name,
            "app.kubernetes.io/instance": self.instance_settings.instance_name,
            "app.kubernetes.io/version": self.instance_settings.instance_version,
            "app.kubernetes.io/managed-by": DEPLOYDOCUS_DOMAIN,
            "deploydocus-pkg": f"{self.pkg_name}-{self.pkg_version}",
        }

    @property
    def default_selectors(self) -> LabelsSelector:
        return {
            "app.kubernetes.io/name": self.pkg_name,
            "app.kubernetes.io/instance": self.instance_settings.instance_name,
            "app.kubernetes.io/managed-by": DEPLOYDOCUS_DOMAIN,
        }

    def render_namespaces(self) -> NamespaceSequence:
        """

        Returns:
            A sequence of Namespace objects (or their dict equivalents)
        """

        return []

    def render_networkpolicies(self) -> NetworkPolicySequence:
        """

        Returns:
            A sequence of NetworkPolicy objects (or their dict equivalents)
        """

        return []

    def render_resourcequotas(self) -> ResourceQuotaSequence:
        """

        Returns:
            A sequence of ResourceQuota objects (or their dict equivalents)
        """

        return []

    def render_limitranges(self) -> LimitRangeSequence:
        """

        Returns:
            A sequence of LimitRange objects (or their dict equivalents)
        """

        return []

    def render_poddisruptionbudgets(self) -> PodDisruptionBudgetSequence:
        """

        Returns:
            A sequence of PodDisruptionBudget objects (or their dict equivalents)
        """

        return []

    def render_serviceaccounts(self) -> ServiceAccountSequence:
        """

        Returns:
            A sequence of ServiceAccount objects (or their dict equivalents)
        """

        return []

    def render_secrets(self) -> SecretSequence:
        """

        Returns:
            A sequence of Secret objects (or their dict equivalents)
        """

        return []

    def render_configmaps(self) -> ConfigMapSequence:
        """

        Returns:
            A sequence of ConfigMap objects (or their dict equivalents)
        """

        return []

    def render_storageclasses(self) -> StorageClassSequence:
        """

        Returns:
            A sequence of StorageClass objects (or their dict equivalents)
        """

        return []

    def render_persistentvolumes(self) -> PersistentVolumeSequence:
        """

        Returns:
            A sequence of PersistentVolume objects (or their dict equivalents)
        """

        return []

    def render_persistentvolumeclaims(self) -> PersistentVolumeClaimSequence:
        """

        Returns:
            A sequence of PersistentVolumeClaim objects (or their dict equivalents)
        """

        return []

    def render_customresourcedefinitions(
        self,
    ) -> CustomResourceDefinitionSequence:
        """

        Returns:
            A sequence of CustomResourceDefinition objects (or their dict equivalents)
        """

        return []

    def render_clusterroles(self) -> ClusterRoleSequence:
        """

        Returns:
            A sequence of ClusterRole objects (or their dict equivalents)
        """

        return []

    def render_clusterrolebindings(self) -> ClusterRoleBindingSequence:
        """

        Returns:
            A sequence of ClusterRoleBinding objects (or their dict equivalents)
        """

        return []

    def render_roles(self) -> RoleSequence:
        """

        Returns:
            A sequence of Role objects (or their dict equivalents)
        """

        return []

    def render_rolebindings(self) -> RoleBindingSequence:
        """

        Returns:
            A sequence of RoleBinding objects (or their dict equivalents)
        """

        return []

    def render_services(self) -> ServiceSequence:
        """

        Returns:
            A sequence of Service objects (or their dict equivalents)
        """

        return []

    def render_daemonsets(self) -> DaemonSetSequence:
        """

        Returns:
            A sequence of DaemonSet objects (or their dict equivalents)
        """

        return []

    def render_pods(self) -> PodSequence:
        """

        Returns:
            A sequence of Pod objects (or their dict equivalents)
        """

        return []

    def render_replicationcontrollers(self) -> ReplicationControllerSequence:
        """

        Returns:
            A sequence of ReplicationController objects (or their dict equivalents)
        """

        return []

    def render_replicasets(self) -> ReplicaSetSequence:
        """

        Returns:
            A sequence of ReplicaSet objects (or their dict equivalents)
        """

        return []

    def render_deployments(self) -> DeploymentSequence:
        """

        Returns:
            A sequence of Deployment objects (or their dict equivalents)
        """

        return []

    def render_horizontalpodautoscalers(self) -> HorizontalPodAutoscalerSequence:
        """

        Returns:
            A sequence of HorizontalPodAutoscaler objects (or their dict equivalents)
        """

        return []

    def render_statefulsets(self) -> StatefulSetSequence:
        """

        Returns:
            A sequence of StatefulSet objects (or their dict equivalents)
        """

        return []

    def render_jobs(self) -> JobSequence:
        """

        Returns:
            A sequence of Job objects (or their dict equivalents)
        """

        return []

    def render_cronjobs(self) -> CronJobSequence:
        """

        Returns:
            A sequence of CronJob objects (or their dict equivalents)
        """

        return []

    def render_ingresses(self) -> IngressSequence:
        """

        Returns:
            A sequence of Ingress objects (or their dict equivalents)
        """

        return []

    def render_apiservices(self) -> APIServiceSequence:
        """

        Returns:
            A sequence of APIService objects (or their dict equivalents)
        """

        return []

    def render(self) -> ManifestSequence:
        """Renders the Kubernetes manifests for the application

        Returns:

        """
        manifests: ManifestSequence = list(
            itertools.chain.from_iterable(
                [
                    m
                    for m in [
                        self.render_namespaces(),
                        self.render_networkpolicies(),
                        self.render_resourcequotas(),
                        self.render_limitranges(),
                        self.render_poddisruptionbudgets(),
                        self.render_serviceaccounts(),
                        self.render_secrets(),
                        self.render_configmaps(),
                        self.render_storageclasses(),
                        self.render_persistentvolumes(),
                        self.render_persistentvolumeclaims(),
                        self.render_customresourcedefinitions(),
                        self.render_clusterroles(),
                        self.render_clusterrolebindings(),
                        self.render_roles(),
                        self.render_rolebindings(),
                        self.render_services(),
                        self.render_daemonsets(),
                        self.render_pods(),
                        self.render_replicationcontrollers(),
                        self.render_replicasets(),
                        self.render_deployments(),
                        self.render_horizontalpodautoscalers(),
                        self.render_statefulsets(),
                        self.render_jobs(),
                        self.render_cronjobs(),
                        self.render_ingresses(),
                        self.render_apiservices(),
                    ]
                    if m
                ]
            )
        )

        return manifests
