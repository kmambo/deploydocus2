from typing import Any, cast
from unittest.mock import Mock

import pytest
from kubernetes_asyncio import V1Deployment

from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.components.workloads.httpapps import (
    HttpIngressRule,
    HttpK8sComponentsModel,
    HttpLivenessProbe,
    HttpReadinessProbe,
    KeyValuePairsNonSensitive,
    KeyValuePairsSecretsExtSrc,
    SimpleHttpApplication,
)
from deploydocus2.pkg import InstanceSettings, K8sComponentModel


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


@pytest.mark.skip("Not now...")
def test_component_to_k8s(application: DeploydocusComponent):
    pass


def test_render_namespace(http_k8s_component: K8sComponentModel):
    assert http_k8s_component.render_namespaces() == []


def test_render_deployment(
    application: SimpleHttpApplication, http_k8s_component: HttpK8sComponentsModel
):
    component: V1Deployment = cast(
        V1Deployment, http_k8s_component.render_deployments()[0]
    )
    deployment_dict = component.to_dict()
    assert isinstance(component, V1Deployment)
    assert deployment_dict["metadata"] == {
        "name": f"{http_k8s_component.instance_settings.name}-"
        f"{http_k8s_component.hl_class.app_name}",
        "labels": http_k8s_component.default_labels,
        "namespace": http_k8s_component.instance_settings.namespace,
    }
    deployment_spec: dict[str, Any] = deployment_dict["spec"]
    # only if there are no additional labels
    pod_template: dict[str, Any] = deployment_spec["template"]
    pod_spec: dict[str, Any] = pod_template["spec"]
    container_dict: dict[str, Any] = pod_spec["containers"][0]
    deployment_selector: dict = deployment_spec["selector"]["matchLabels"]
    pod_template_labels: dict = deployment_spec["template"]["metadata"]["labels"]
    assert deployment_selector.items() <= pod_template_labels.items()
    assert pod_spec["serviceAccountName"] == f"{deployment_dict['metadata']['name']}-sa"
    assert container_dict["image"] == application.app_image
    assert container_dict["command"] == application.app_command
    assert "env" not in container_dict  # env vars are mounted
    assert (
        container_dict["args"] == application.app_entrypoint_args
        if application.app_entrypoint_args
        else "args" not in container_dict
    )
    assert (
        application.liveness_probe is None
        and "liveness" not in container_dict
        or "httpGet" in container_dict["livenessProbe"]
    )
