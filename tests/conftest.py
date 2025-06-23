from typing import cast
from unittest.mock import Mock

import pytest
from kubernetes_asyncio import (
    V1Container,
    V1Deployment,
    V1DeploymentSpec,
    V1PodSpec,
    V1Probe,
)

from deploydocus2.components.workloads.httpapps import (
    HttpIngressRule,
    HttpK8sComponentsModel,
    HttpLivenessProbe,
    HttpReadinessProbe,
    HttpStartupProbe,
    KeyValuePairsNonSensitive,
    KeyValuePairsSecretsExtSrc,
    SimpleHttpApplication,
)
from deploydocus2.pkg import InstanceSettings


@pytest.fixture
def app_config_nonsensitive() -> KeyValuePairsNonSensitive:
    return KeyValuePairsNonSensitive(
        kv_pairs={"key1": "value1"},
        mount_path="/var/run/config",
    )


@pytest.fixture
def app_config_sensitive_mock() -> KeyValuePairsSecretsExtSrc:
    kv_ext_src = Mock(KeyValuePairsSecretsExtSrc)
    kv_ext_src.kv_pairs = {"secret_key1": "secret_value1"}
    return kv_ext_src


@pytest.fixture
def app_config_nonsensitive_mock() -> KeyValuePairsNonSensitive:
    ret = Mock(KeyValuePairsNonSensitive)
    return ret


@pytest.fixture
def application(
    app_config_nonsensitive_mock: KeyValuePairsNonSensitive,
    app_config_sensitive_mock: KeyValuePairsSecretsExtSrc,
):
    return SimpleHttpApplication(
        app_name="test-app",
        namespace="test-ns",
        http_named_ports={
            "http": 9080,
        },
        version="1.0.0",
        app_image="test.io/testimage:v1.0.7",
        app_command=["--arg1=value1", "--arg2=value2"],
        liveness_probe=HttpLivenessProbe(rel_url="/liveness"),
        readiness_probe=HttpReadinessProbe(rel_url="/readyz"),
        app_config_non_sensitive=app_config_nonsensitive_mock,
        app_config_secrets=app_config_sensitive_mock,
        ingress=HttpIngressRule(
            host="api.mytestapp.app",
            path="/api/*",
            ingress_class_name="nginx",
            implementation_specific=True,
        ),
        service_ports={"http": 8080},
    )


@pytest.fixture
def http_k8s_component(application: SimpleHttpApplication) -> HttpK8sComponentsModel:
    return HttpK8sComponentsModel(
        hl_class=application,
        pkg_name=application.app_name,
        pkg_version=application.version,
        instance_settings=InstanceSettings(
            name="inst1",
            namespace="test-ns",
        ),
    )


@pytest.fixture
def deployment(
    http_k8s_component: HttpK8sComponentsModel,
) -> V1Deployment:
    return cast(V1Deployment, http_k8s_component.render_deployments()[0])


@pytest.fixture
def container(http_k8s_component: HttpK8sComponentsModel) -> V1Container:
    return cast(
        V1PodSpec,
        cast(
            V1DeploymentSpec,
            cast(V1Deployment, http_k8s_component.render_deployments()[0]).spec,
        ).template.spec,
    ).containers[0]


@pytest.fixture
def container_liveness_probe(container: V1Container) -> V1Probe:
    return cast(V1Probe, container.liveness_probe)


@pytest.fixture
def http_liveness_probe(application: SimpleHttpApplication) -> HttpLivenessProbe:
    return cast(HttpLivenessProbe, application.liveness_probe)


@pytest.fixture
def container_readiness_probe(container: V1Container) -> V1Probe:
    return cast(V1Probe, container.readiness_probe)


@pytest.fixture
def http_readiness_probe(application: SimpleHttpApplication) -> HttpLivenessProbe:
    return cast(HttpLivenessProbe, application.readiness_probe)


@pytest.fixture
def container_startup_probe(container: V1Container) -> V1Probe | None:
    return container.startup_probe


@pytest.fixture
def http_startup_probe(application: SimpleHttpApplication) -> HttpStartupProbe | None:
    return application.startup_probe
