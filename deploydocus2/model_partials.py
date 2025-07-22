from kubernetes_asyncio import models
from pydantic import Field, StrictStr


class Namespace(models.V1Namespace):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Namespace",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class NetworkPolicy(models.V1NetworkPolicy):
    api_version: StrictStr = Field(
        default="networking.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="NetworkPolicy",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ResourceQuota(models.V1ResourceQuota):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ResourceQuota",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class LimitRange(models.V1LimitRange):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="LimitRange",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class PodDisruptionBudget(models.V1PodDisruptionBudget):
    api_version: StrictStr = Field(
        default="policy/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="PodDisruptionBudget",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ServiceAccount(models.V1ServiceAccount):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ServiceAccount",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Secret(models.V1Secret):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Secret",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class SecretList(models.V1SecretList):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="SecretList",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ConfigMap(models.V1ConfigMap):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ConfigMap",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class StorageClass(models.V1StorageClass):
    api_version: StrictStr = Field(
        default="storage.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="StorageClass",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class PersistentVolume(models.V1PersistentVolume):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="PersistentVolume",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class PersistentVolumeClaim(models.V1PersistentVolumeClaim):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="PersistentVolumeClaim",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class CustomResourceDefinition(models.V1CustomResourceDefinition):
    api_version: StrictStr = Field(
        default="apiextensions.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="CustomResourceDefinition",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ClusterRole(models.V1ClusterRole):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ClusterRole",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ClusterRoleList(models.V1ClusterRoleList):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ClusterRoleList",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ClusterRoleBinding(models.V1ClusterRoleBinding):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ClusterRoleBinding",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ClusterRoleBindingList(models.V1ClusterRoleBindingList):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ClusterRoleBindingList",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Role(models.V1Role):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Role",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class RoleList(models.V1RoleList):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="RoleList",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class RoleBinding(models.V1RoleBinding):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="RoleBinding",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class RoleBindingList(models.V1RoleBindingList):
    api_version: StrictStr = Field(
        default="rbac.authorization.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="RoleBindingList",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Service(models.V1Service):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Service",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class DaemonSet(models.V1DaemonSet):
    api_version: StrictStr = Field(
        default="apps/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="DaemonSet",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Pod(models.V1Pod):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Pod",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ReplicationController(models.V1ReplicationController):
    api_version: StrictStr = Field(
        default="v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ReplicationController",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class ReplicaSet(models.V1ReplicaSet):
    api_version: StrictStr = Field(
        default="apps/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="ReplicaSet",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Deployment(models.V1Deployment):
    api_version: StrictStr = Field(
        default="apps/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Deployment",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class HorizontalPodAutoscaler(models.V2HorizontalPodAutoscaler):
    api_version: StrictStr = Field(
        default="autoscaling/v2",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="HorizontalPodAutoscaler",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class StatefulSet(models.V1StatefulSet):
    api_version: StrictStr = Field(
        default="apps/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="StatefulSet",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Job(models.V1Job):
    api_version: StrictStr = Field(
        default="batch/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Job",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class CronJob(models.V1CronJob):
    api_version: StrictStr = Field(
        default="batch/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="CronJob",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class Ingress(models.V1Ingress):
    api_version: StrictStr = Field(
        default="networking.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="Ingress",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )


class APIService(models.V1APIService):
    api_version: StrictStr = Field(
        default="apiregistration.k8s.io/v1",
        description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",  # noqa: E501
        alias="apiVersion",
    )
    kind: StrictStr = Field(
        default="APIService",
        description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds",  # noqa: E501
    )
