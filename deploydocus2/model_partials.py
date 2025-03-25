from typing import Any

from kubernetes_asyncio.client import models


class Namespace(models.V1Namespace):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="Namespace")
        _data.update(data)
        super().__init__(**_data)


class NetworkPolicy(models.V1NetworkPolicy):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="networking.k8s.io/v1", kind="NetworkPolicy")
        _data.update(data)
        super().__init__(**_data)


class ResourceQuota(models.V1ResourceQuota):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="ResourceQuota")
        _data.update(data)
        super().__init__(**_data)


class LimitRange(models.V1LimitRange):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="LimitRange")
        _data.update(data)
        super().__init__(**_data)


class PodDisruptionBudget(models.V1PodDisruptionBudget):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="policy/v1", kind="PodDisruptionBudget")
        _data.update(data)
        super().__init__(**_data)


class ServiceAccount(models.V1ServiceAccount):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="ServiceAccount")
        _data.update(data)
        super().__init__(**_data)


class Secret(models.V1Secret):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="Secret")
        _data.update(data)
        super().__init__(**_data)


class SecretList(models.V1SecretList):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="SecretList")
        _data.update(data)
        super().__init__(**_data)


class ConfigMap(models.V1ConfigMap):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="ConfigMap")
        _data.update(data)
        super().__init__(**_data)


class StorageClass(models.V1StorageClass):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="storage.k8s.io/v1", kind="StorageClass")
        _data.update(data)
        super().__init__(**_data)


class PersistentVolume(models.V1PersistentVolume):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="PersistentVolume")
        _data.update(data)
        super().__init__(**_data)


class PersistentVolumeClaim(models.V1PersistentVolumeClaim):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="PersistentVolumeClaim")
        _data.update(data)
        super().__init__(**_data)


class CustomResourceDefinition(models.V1CustomResourceDefinition):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(
            api_version="apiextensions.k8s.io/v1", kind="CustomResourceDefinition"
        )
        _data.update(data)
        super().__init__(**_data)


class ClusterRole(models.V1ClusterRole):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="ClusterRole")
        _data.update(data)
        super().__init__(**_data)


class ClusterRoleList(models.V1ClusterRoleList):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="ClusterRoleList")
        _data.update(data)
        super().__init__(**_data)


class ClusterRoleBinding(models.V1ClusterRoleBinding):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(
            api_version="rbac.authorization.k8s.io/v1", kind="ClusterRoleBinding"
        )
        _data.update(data)
        super().__init__(**_data)


class ClusterRoleBindingList(models.V1ClusterRoleBindingList):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(
            api_version="rbac.authorization.k8s.io/v1", kind="ClusterRoleBindingList"
        )
        _data.update(data)
        super().__init__(**_data)


class Role(models.V1Role):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="Role")
        _data.update(data)
        super().__init__(**_data)


class RoleList(models.V1RoleList):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="RoleList")
        _data.update(data)
        super().__init__(**_data)


class RoleBinding(models.V1RoleBinding):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="RoleBinding")
        _data.update(data)
        super().__init__(**_data)


class RoleBindingList(models.V1RoleBindingList):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="rbac.authorization.k8s.io/v1", kind="RoleBindingList")
        _data.update(data)
        super().__init__(**_data)


class Service(models.V1Service):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="Service")
        _data.update(data)
        super().__init__(**_data)


class DaemonSet(models.V1DaemonSet):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="apps/v1", kind="DaemonSet")
        _data.update(data)
        super().__init__(**_data)


class Pod(models.V1Pod):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="Pod")
        _data.update(data)
        super().__init__(**_data)


class ReplicationController(models.V1ReplicationController):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="v1", kind="ReplicationController")
        _data.update(data)
        super().__init__(**_data)


class ReplicaSet(models.V1ReplicaSet):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="apps/v1", kind="ReplicaSet")
        _data.update(data)
        super().__init__(**_data)


class Deployment(models.V1Deployment):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="apps/v1", kind="Deployment")
        _data.update(data)
        super().__init__(**_data)


class HorizontalPodAutoscaler(models.V2HorizontalPodAutoscaler):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="autoscaling/v2", kind="HorizontalPodAutoscaler")
        _data.update(data)
        super().__init__(**_data)


class StatefulSet(models.V1StatefulSet):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="apps/v1", kind="StatefulSet")
        _data.update(data)
        super().__init__(**_data)


class Job(models.V1Job):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="batch/v1", kind="Job")
        _data.update(data)
        super().__init__(**_data)


class CronJob(models.V1CronJob):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="batch/v1", kind="CronJob")
        _data.update(data)
        super().__init__(**_data)


class Ingress(models.V1Ingress):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="networking.k8s.io/v1", kind="Ingress")
        _data.update(data)
        super().__init__(**_data)


class APIService(models.V1APIService):
    def __init__(self, /, **data: Any) -> None:
        _data = dict(api_version="apiregistration.k8s.io/v1", kind="APIService")
        _data.update(data)
        super().__init__(**_data)
