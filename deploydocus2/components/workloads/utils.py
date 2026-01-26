import base64
from collections import UserDict
from pathlib import Path
from typing import Callable, Mapping, Sequence, cast

import pydantic
from kubernetes import (
    V1ConfigMap,
    V1ConfigMapEnvSource,
    V1ConfigMapKeySelector,
    V1ConfigMapVolumeSource,
    V1Container,
    V1EnvFromSource,
    V1EnvVar,
    V1EnvVarSource,
    V1KeyToPath,
    V1ObjectMeta,
    V1PodSpec,
    V1Secret,
    V1SecretEnvSource,
    V1SecretKeySelector,
    V1SecretVolumeSource,
    V1Volume,
    V1VolumeMount,
)
from pydantic import SecretBytes, SecretStr, StrictBytes, StrictStr

from ...model_partials import ConfigMap, Secret
from .exceptions import ContainerNotFound

type _Config = UserDict[str, StrictStr | StrictBytes]


class _ConfigSecret(UserDict[str, SecretStr | SecretBytes]):
    def __setitem__(
        self, key: str, item: SecretStr | SecretBytes | StrictStr | StrictBytes
    ):
        if isinstance(item, (SecretStr, SecretBytes)):
            super().__setitem__(key, item)
        elif isinstance(item, bytes):
            super().__setitem__(key, SecretBytes(item))
        else:  # assume StrictStr
            super().__setitem__(key, SecretStr(item))


def mk_upper_case(key: str) -> str:
    """Converts a key to uppercase. Typically used to convert a lower-case key to
    uppercase and expose as an environment variable. so a key 'client-id' becomes an
    env var 'CLIENT_ID' (Note the changing of the dash to an underscore)

    Args:
        key: The key to convert.

    Returns:
        The key made uppercase
    """
    return key.upper().replace("-", "_")


def to_secret(
    cfg_secret: _ConfigSecret,
    name: str,
    namespace: str,
    labels: dict[str, str] | None = None,
    annotations: dict[str, str] | None = None,
) -> V1Secret:
    """
    Creates a Kubernetes Secret from a ConfigSecret.

    Args:
        cfg_secret:
        name:
        namespace:
        labels:
        annotations:

    Returns:

    """
    _encode: Callable[[SecretStr | SecretBytes], StrictBytes | StrictStr] = lambda x: (
        base64.b64encode(x.get_secret_value().encode("utf-8")).decode("utf-8")
        if isinstance(x, SecretStr)
        else base64.b64encode(x.get_secret_value())
    )
    return Secret(
        data={k: _encode(v) for k, v in cfg_secret.data.items()},
        metadata=V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=None if not labels else labels,
            annotations=None if not annotations else annotations,
        ),
    )


def to_config_map(
    cfg: _Config,
    name: str,
    namespace: str,
    labels: dict[str, str] | None = None,
    annotations: dict[str, str] | None = None,
) -> V1ConfigMap:
    """Creates a V1ConfigMap from a _Config object.

    Args:
        cfg: Key-Value pair
        name: Name of the ConfigMap
        namespace: The namespace in which to create the ConfigMap
        labels: Additional labels to apply to the ConfigMap
        annotations: Additional annotations to apply to the ConfigMap

    Returns:

    """
    return ConfigMap(
        data={k: v for k, v in cfg.data.items() if isinstance(v, str)},
        binary_data={k: v for k, v in cfg.data.items() if isinstance(v, bytes)},
        metadata=V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=None if not labels else labels,
            annotations=None if not annotations else annotations,
        ),
    )


def update_container_env_refs(
    cm_or_secret: V1ConfigMap | V1Secret,
    container: V1Container,
    keys_as: Mapping[str, str] | None = None,
) -> Sequence[V1EnvVar | V1EnvFromSource]:
    """

    Args:
        container:
        cm_or_secret:
        keys_as:

    Returns:

    """
    assert (
        cm_or_secret.data is not None and cm_or_secret.data
    ), "cm_or_secret.data  cannot be null or empty"
    assert cm_or_secret.metadata is not None, "cm_or_secret.metadata must be set"
    cm = isinstance(cm_or_secret, V1ConfigMap)
    if keys_as is None:  # create .envFrom:
        env_from: list[V1EnvFromSource] = [
            (
                V1EnvFromSource(
                    config_map_ref=V1ConfigMapEnvSource(name=cm_or_secret.metadata.name)
                )
                if cm
                else V1EnvFromSource(
                    secret_ref=V1SecretEnvSource(name=cm_or_secret.metadata.name)
                )
            )
        ]
        if container.env_from is None:
            container.env_from = env_from
        else:
            container.env_from.extend(env_from)
        return env_from
    else:  # create .env:
        env: list[V1EnvVar] = [
            V1EnvVar(
                name=keys_as[k],
                value_from=(
                    V1EnvVarSource(
                        config_map_key_ref=(
                            (
                                V1ConfigMapKeySelector(
                                    name=cm_or_secret.metadata.name, key=k
                                )
                            )
                        )
                    )
                    if cm
                    else V1EnvVarSource(
                        secret_key_ref=V1SecretKeySelector(
                            name=cm_or_secret.metadata.name, key=k
                        )
                    )
                ),
            )
            for k in keys_as.keys()
            if k in cm_or_secret.data.keys()
        ]

        if container.env is not None:
            container.env.extend(env)
        else:
            container.env = env

        return env


def encode_secret_data(kv: dict[str, str]) -> dict[str, SecretStr]:
    """Helper to create base64-encoded secrets data. The keys are unaffected. The
    value is base64-enoded and then converted to a SecretStr
    (to protect against accidental exposure in logs).

    Args:
        kv:

    Returns:

    """
    return {
        k: SecretStr(base64.b64encode(value.encode("utf-8")).decode("utf-8"))
        for k, value in kv.items()
    }


@pydantic.validate_call
def volume_mount_config_map_or_secret(
    pod_spec: V1PodSpec,
    path: Path,
    config_map_name: str | None = None,
    container_name: str | None = None,
    secret_name: str | None = None,
    volume_name: str | None = None,
    keys_map: dict[str, Path] | None = None,
):
    """

    Args:
        secret_name:
        volume_name: The name of the volume
        keys_map: rarely required and usually a bad idea to set.
        config_map_name:
        pod_spec:
        container_name:
        path:

    Returns:

    """
    assert pod_spec.containers is not None, "pod_spec.containers must be set"
    assert (config_map_name is None) ^ (
        secret_name is None
    ), "exactly one of config_map_name and secret_name must be set"
    assert (
        len(pod_spec.containers) == 1 if container_name is None else True
    ), "container_name required must not be empty"
    try:
        mounted_vol_name = volume_name or config_map_name or secret_name
        container = (
            [c for c in pod_spec.containers if c.name == container_name][0]
            if container_name
            else pod_spec.containers[0]
        )
        existing_volume_mounts: Sequence[str] = (
            [c.name for c in container.volume_mounts] if container.volume_mounts else []
        )
        assert mounted_vol_name not in existing_volume_mounts, (
            f"{container.name} already has a volume mounted in "
            f"pod_spec as {mounted_vol_name}"
        )
        existing_volume_names = (
            [c.name for c in pod_spec.volumes] if pod_spec.volumes else []
        )
        assert (
            mounted_vol_name not in existing_volume_names
        ), f"{mounted_vol_name} already exists as volume in pod_spec"

        # create and add volume to pod_spec
        volume = V1Volume(
            name=mounted_vol_name,
            config_map=(
                V1ConfigMapVolumeSource(
                    name=config_map_name,
                    items=(
                        None
                        if not keys_map
                        else [
                            V1KeyToPath(path=str(v), key=k) for k, v in keys_map.items()
                        ]
                    ),
                )
                if config_map_name
                else None
            ),
            secret=V1SecretVolumeSource(
                secret_name=secret_name,
                items=(
                    (
                        None
                        if not keys_map
                        else [
                            V1KeyToPath(path=str(v), key=k) for k, v in keys_map.items()
                        ]
                    )
                    if secret_name
                    else None
                ),
            ),
        )
        volumes = cast(list[V1Volume], pod_spec.volumes or [])
        volumes.append(volume)
        pod_spec.volumes = volumes

        # create and add volume mount to container
        volume_mounts = container.volume_mounts or []
        volume_mounts.append(
            V1VolumeMount(
                read_only=True,
                name=mounted_vol_name,
                mount_path=str(path),
            )
        )
        container.volume_mounts = volume_mounts
    except IndexError as err:
        raise ContainerNotFound(f"{container_name} not found in pod_spec") from err
