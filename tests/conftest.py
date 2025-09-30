from typing import Mapping, cast
from unittest.mock import Mock

import pytest
from kubernetes_asyncio_pydantic import (
    V1Container,
    V1Deployment,
    V1DeploymentSpec,
    V1Ingress,
    V1PodSpec,
    V1Probe,
    V1Service,
)

from deploydocus2.components.workloads.httpapps import (
    HttpIngressHostWithRules,
    HttpIngressRule,
    HttpK8sComponentsModel,
    HttpLivenessProbe,
    HttpReadinessProbe,
    HttpStartupProbe,
    KeyValuePairsNonSensitive,
    KeyValuePairsSecretsExtSrc,
    RuleType,
    SimpleHttpApplication,
)


@pytest.fixture
def app_config_nonsensitive() -> dict[str, KeyValuePairsNonSensitive]:
    return {
        "lone_cfg": KeyValuePairsNonSensitive(
            kv_pairs={"key1": "value1"},
            mount_path="/var/run/config",
        ),
        "env_vars": KeyValuePairsNonSensitive(kv_pairs={"key1": "value1"}),
    }


@pytest.fixture
def app_config_sensitive_mock() -> Mapping[str, KeyValuePairsSecretsExtSrc]:
    kv_ext_src = Mock(KeyValuePairsSecretsExtSrc)
    kv_ext_src.kv_pairs = {"secret_key1": "secret_value1"}
    return {"mock_secret": kv_ext_src}


@pytest.fixture
def app_config_nonsensitive_mock() -> Mapping[str, KeyValuePairsNonSensitive]:
    ret = {"env_dir": Mock(KeyValuePairsNonSensitive)}
    return ret


@pytest.fixture
def application(
    app_config_nonsensitive_mock: Mapping[str, KeyValuePairsNonSensitive],
    app_config_sensitive_mock: Mapping[str, KeyValuePairsSecretsExtSrc],
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
        ingress=HttpIngressHostWithRules(
            host="api.mytestapp.app",
            ingress_class_name="nginx",
            rules=[HttpIngressRule(path="/api", path_type=RuleType.PREFIX)],
        ),
        app_ports={"http": 8080},
    )


@pytest.fixture
def http_k8s_component(application: SimpleHttpApplication) -> HttpK8sComponentsModel:
    return cast(HttpK8sComponentsModel, application.gen_k8s_components())


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


@pytest.fixture
def svc(http_k8s_component: HttpK8sComponentsModel) -> V1Service:
    return cast(V1Service, http_k8s_component.render_services()[0])


@pytest.fixture
def ingress(http_k8s_component: HttpK8sComponentsModel) -> V1Ingress:
    return cast(V1Ingress, http_k8s_component.render_ingresses()[0])
