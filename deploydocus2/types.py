from collections import OrderedDict
from collections.abc import Sequence
from typing import Any, LiteralString, Mapping, NotRequired, TypedDict, Union

from kubernetes_asyncio.client.models import (  # type: ignore[import-untyped]
    V1APIService,
    V1ClusterRole,
    V1ClusterRoleBinding,
    V1ClusterRoleBindingList,
    V1ClusterRoleList,
    V1ConfigMap,
    V1CronJob,
    V1CustomResourceDefinition,
    V1DaemonSet,
    V1Deployment,
    V1HorizontalPodAutoscaler,
    V1Ingress,
    V1Job,
    V1LimitRange,
    V1Namespace,
    V1NetworkPolicy,
    V1PersistentVolume,
    V1PersistentVolumeClaim,
    V1Pod,
    V1PodDisruptionBudget,
    V1ReplicaSet,
    V1ReplicationController,
    V1ResourceQuota,
    V1Role,
    V1RoleBinding,
    V1RoleBindingList,
    V1RoleList,
    V1Secret,
    V1SecretList,
    V1Service,
    V1ServiceAccount,
    V1StatefulSet,
    V1StorageClass,
    V2HorizontalPodAutoscaler,
)

SUPPORTED_KINDS: OrderedDict[LiteralString, LiteralString] = OrderedDict(
    [
        ("Namespace", "v1"),
        ("NetworkPolicy", "networking.k8s.io/v1"),
        ("ResourceQuota", "v1"),
        ("LimitRange", "v1"),
        ("PodDisruptionBudget", "policy/v1"),
        ("ServiceAccount", "v1"),
        ("Secret", "v1"),
        ("SecretList", "v1"),
        ("ConfigMap", "v1"),
        ("StorageClass", "storage.k8s.io/v1"),
        ("PersistentVolume", "v1"),
        ("PersistentVolumeClaim", "v1"),
        ("CustomResourceDefinition", "apiextensions.k8s.io/v1"),
        ("ClusterRole", "rbac.authorization.k8s.io/v1"),
        ("ClusterRoleList", "rbac.authorization.k8s.io/v1"),
        ("ClusterRoleBinding", "rbac.authorization.k8s.io/v1"),
        ("ClusterRoleBindingList", "rbac.authorization.k8s.io/v1"),
        ("Role", "rbac.authorization.k8s.io/v1"),
        ("RoleList", "rbac.authorization.k8s.io/v1"),
        ("RoleBinding", "rbac.authorization.k8s.io/v1"),
        ("RoleBindingList", "rbac.authorization.k8s.io/v1"),
        ("Service", "v1"),
        ("DaemonSet", "apps/v1"),
        ("Pod", "v1"),
        ("ReplicationController", "v1"),
        ("ReplicaSet", "apps/v1"),
        ("Deployment", "apps/v1"),
        ("HorizontalPodAutoscaler", "autoscaling/v2"),
        ("StatefulSet", "apps/v1"),
        ("Job", "batch/v1"),
        ("CronJob", "batch/v1"),
        ("Ingress", "networking.k8s.io/v1"),
        ("APIService", "apiregistration.k8s.io/v1"),
    ]
)

SUPPORTED_KUBERNETES_KINDS: list[str] = list(SUPPORTED_KINDS.keys())

LabelsSelector = TypedDict(
    "LabelsSelector",
    {
        "app.kubernetes.io/instance": str,
        "app.kubernetes.io/managed-by": str,
        "app.kubernetes.io/name": NotRequired[str],
    },
)

LabelsDict = TypedDict(
    "LabelsDict",
    {
        "app.kubernetes.io/instance": str,
        "app.kubernetes.io/name": str,
        "app.kubernetes.io/version": str,
        "deploydocus-pkg": str,
        "app.kubernetes.io/managed-by": str,
    },
)

type NamespaceSequence = Sequence[Mapping[str, Any] | V1Namespace]
type NetworkPolicySequence = Sequence[Mapping[str, Any] | V1NetworkPolicy]
type ResourceQuotaSequence = Sequence[Mapping[str, Any] | V1ResourceQuota]
type LimitRangeSequence = Sequence[Mapping[str, Any] | V1LimitRange]
type PodDisruptionBudgetSequence = Sequence[Mapping[str, Any] | V1PodDisruptionBudget]
type ServiceAccountSequence = Sequence[Mapping[str, Any] | V1ServiceAccount]
type SecretSequence = Sequence[Mapping[str, Any] | V1Secret]
type SecretListSequence = Sequence[Mapping[str, Any] | V1SecretList]
type ConfigMapSequence = Sequence[Mapping[str, Any] | V1ConfigMap]
type StorageClassSequence = Sequence[Mapping[str, Any] | V1StorageClass]
type PersistentVolumeSequence = Sequence[Mapping[str, Any] | V1PersistentVolume]
type PersistentVolumeClaimSequence = Sequence[
    Mapping[str, Any] | V1PersistentVolumeClaim
]
type CustomResourceDefinitionSequence = Sequence[
    Mapping[str, Any] | V1CustomResourceDefinition
]
type ClusterRoleSequence = Sequence[Mapping[str, Any] | V1ClusterRole]
type ClusterRoleListSequence = Sequence[Mapping[str, Any] | V1ClusterRoleList]
type ClusterRoleBindingSequence = Sequence[Mapping[str, Any] | V1ClusterRoleBinding]
type ClusterRoleBindingListSequence = Sequence[
    Mapping[str, Any] | V1ClusterRoleBindingList
]
type RoleSequence = Sequence[Mapping[str, Any] | V1Role]
type RoleListSequence = Sequence[Mapping[str, Any] | V1RoleList]
type RoleBindingSequence = Sequence[Mapping[str, Any] | V1RoleBinding]
type RoleBindingListSequence = Sequence[Mapping[str, Any] | V1RoleBindingList]
type ServiceSequence = Sequence[Mapping[str, Any] | V1Service]
type DaemonSetSequence = Sequence[Mapping[str, Any] | V1DaemonSet]
type PodSequence = Sequence[Mapping[str, Any] | V1Pod]
type ReplicationControllerSequence = Sequence[
    Mapping[str, Any] | V1ReplicationController
]
type ReplicaSetSequence = Sequence[Mapping[str, Any] | V1ReplicaSet]
type DeploymentSequence = Sequence[Mapping[str, Any] | V1Deployment]
type HorizontalPodAutoscalerSequence = Sequence[
    Mapping[str, Any] | V2HorizontalPodAutoscaler
]
type StatefulSetSequence = Sequence[Mapping[str, Any] | V1StatefulSet]
type JobSequence = Sequence[Mapping[str, Any] | V1Job]
type CronJobSequence = Sequence[Mapping[str, Any] | V1CronJob]
type IngressSequence = Sequence[Mapping[str, Any] | V1Ingress]
type APIServiceSequence = Sequence[Mapping[str, Any] | V1APIService]

type K8sModel = Union[
    V1APIService,
    V1ClusterRoleBinding,
    V1ClusterRole,
    V1ConfigMap,
    V1CronJob,
    V1CustomResourceDefinition,
    V1DaemonSet,
    V1Deployment,
    V1HorizontalPodAutoscaler,
    V1Ingress,
    V1Job,
    V1LimitRange,
    V1Namespace,
    V1NetworkPolicy,
    V1PersistentVolume,
    V1PersistentVolumeClaim,
    V1Pod,
    V1PodDisruptionBudget,
    V1ReplicaSet,
    V1ReplicationController,
    V1ResourceQuota,
    V1RoleBinding,
    V1Role,
    V1Secret,
    V1Service,
    V1ServiceAccount,
    V1StatefulSet,
    V1StorageClass,
]
K8sListModel = Union[
    V1ClusterRoleBindingList,
    V1ClusterRoleList,
    V1RoleBindingList,
    V1RoleList,
    V1SecretList,
]

K8sModelSequence = Sequence[K8sModel]
# TODO: Deprecate the ones below
ManifestDict = Mapping[str, Any] | K8sModel
ManifestSequence = Sequence[ManifestDict]
ManifestAll = ManifestDict | ManifestSequence
