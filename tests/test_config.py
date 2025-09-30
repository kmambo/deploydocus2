from typing import Sequence, cast

from kubernetes_asyncio_pydantic import V1PodSpec, V1Volume, V1VolumeMount

from deploydocus2.components.workloads import SimpleHttpApplication


def test_config_mounted(application: SimpleHttpApplication):
    k8s_components = application.gen_k8s_components()
    podspec: V1PodSpec = k8s_components.render_deployments()[0].spec.template.spec
    cfg_map = k8s_components.render_configmaps()[0]
    volume = cast(Sequence[V1Volume], podspec.volumes)[0]
    container_vol_mnt: V1VolumeMount = podspec.containers[0].volume_mounts[0]

    assert volume.name == container_vol_mnt.name
    assert volume.config_map.name == cfg_map.name
