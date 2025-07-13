from collections.abc import Sequence
from typing import Union

from kubernetes_asyncio.models import (  # type: ignore[import-untyped]
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

type NamespaceSequence = Sequence[V1Namespace]
type NetworkPolicySequence = Sequence[V1NetworkPolicy]
type ResourceQuotaSequence = Sequence[V1ResourceQuota]
type LimitRangeSequence = Sequence[V1LimitRange]
type PodDisruptionBudgetSequence = Sequence[V1PodDisruptionBudget]
type ServiceAccountSequence = Sequence[V1ServiceAccount]
type SecretSequence = Sequence[V1Secret]
type SecretListSequence = Sequence[V1SecretList]
type ConfigMapSequence = Sequence[V1ConfigMap]
type StorageClassSequence = Sequence[V1StorageClass]
type PersistentVolumeSequence = Sequence[V1PersistentVolume]
type PersistentVolumeClaimSequence = Sequence[V1PersistentVolumeClaim]
type CustomResourceDefinitionSequence = Sequence[V1CustomResourceDefinition]
type ClusterRoleSequence = Sequence[V1ClusterRole]
type ClusterRoleListSequence = Sequence[V1ClusterRoleList]
type ClusterRoleBindingSequence = Sequence[V1ClusterRoleBinding]
type ClusterRoleBindingListSequence = Sequence[V1ClusterRoleBindingList]
type RoleSequence = Sequence[V1Role]
type RoleListSequence = Sequence[V1RoleList]
type RoleBindingSequence = Sequence[V1RoleBinding]
type RoleBindingListSequence = Sequence[V1RoleBindingList]
type ServiceSequence = Sequence[V1Service]
type DaemonSetSequence = Sequence[V1DaemonSet]
type PodSequence = Sequence[V1Pod]
type ReplicationControllerSequence = Sequence[V1ReplicationController]
type ReplicaSetSequence = Sequence[V1ReplicaSet]
type DeploymentSequence = Sequence[V1Deployment]
type HorizontalPodAutoscalerSequence = Sequence[V2HorizontalPodAutoscaler]
type StatefulSetSequence = Sequence[V1StatefulSet]
type JobSequence = Sequence[V1Job]
type CronJobSequence = Sequence[V1CronJob]
type IngressSequence = Sequence[V1Ingress]
type APIServiceSequence = Sequence[V1APIService]

type K8sModel = Union[
    V1APIService,
    V1ClusterRoleBinding,
    V1ClusterRole,
    V1ConfigMap,
    V1CronJob,
    V1CustomResourceDefinition,
    V1DaemonSet,
    V1Deployment,
    V2HorizontalPodAutoscaler,
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
