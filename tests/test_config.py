from typing import Sequence, cast

from kubernetes import (
    V1ConfigMap,
    V1ConfigMapVolumeSource,
    V1DeploymentSpec,
    V1ObjectMeta,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)

from deploydocus2.components.workloads import SimpleHttpApplication


def test_config_mounted(application: SimpleHttpApplication):
    k8s_components = application.gen_k8s_components()
    podspec: V1PodSpec = cast(
        V1PodSpec,
        cast(
            V1DeploymentSpec, k8s_components.render_deployments()[0].spec
        ).template.spec,
    )
    cfg_map = cast(list[V1ConfigMap], k8s_components.render_configmaps())[0]
    volume = cast(Sequence[V1Volume], podspec.volumes)[0]
    container_vol_mnt: V1VolumeMount = cast(
        list[V1VolumeMount], podspec.containers[0].volume_mounts
    )[0]

    assert volume.name == container_vol_mnt.name
    assert (
        cast(V1ConfigMapVolumeSource, volume.config_map).name
        == cast(V1ObjectMeta, cfg_map.metadata).name
    )
