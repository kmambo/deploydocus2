from typing import cast

import pytest
from kubernetes_asyncio import (
    V1Container,
    V1ContainerPort,
    V1Deployment,
    V1DeploymentSpec,
    V1ObjectMeta,
    V1PodSpec,
)

from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.components.workloads.httpapps import (
    HttpK8sComponentsModel,
    SimpleHttpApplication,
)
from deploydocus2.pkg import K8sComponentsModel


@pytest.mark.skip("Not now...")
def test_component_to_k8s(application: DeploydocusComponent):
    pass


def test_render_namespace(http_k8s_component: K8sComponentsModel):
    assert http_k8s_component.render_namespaces() == []


def test_deployment(
    application: SimpleHttpApplication,
    deployment: V1Deployment,
    http_k8s_component: HttpK8sComponentsModel,
):
    deployment_metadata = cast(V1ObjectMeta, deployment.metadata)
    assert cast(str, deployment_metadata.name) == (
        f"{http_k8s_component.instance_settings.name}-"
        f"{cast(str, http_k8s_component.hl_class.app_name)}"
    )
    assert deployment_metadata.labels == http_k8s_component.default_labels
    assert (
        cast(str, deployment_metadata.namespace)
        == http_k8s_component.instance_settings.namespace
    )
    deployment_spec = cast(V1DeploymentSpec, deployment.spec)
    # only if there are no additional labels
    pod_template = deployment_spec.template
    pod_spec = cast(V1PodSpec, pod_template.spec)
    deployment_selector = deployment_spec.selector.match_labels or {}
    pod_template_labels = (
        cast(V1ObjectMeta, deployment_spec.template.metadata).labels or {}
    )
    assert deployment_selector.items() <= pod_template_labels.items()
    assert (
        cast(str, pod_spec.service_account_name)
        == f"{cast(str, deployment_metadata.name)}-sa"
    )


def test_container_image(container: V1Container, application: SimpleHttpApplication):
    assert container.image == application.app_image


def test_container_cmd(container: V1Container, application: SimpleHttpApplication):
    assert container.command == application.app_command


def test_container_env(container: V1Container, application: SimpleHttpApplication):
    assert not container.env


def test_container_args(container: V1Container, application: SimpleHttpApplication):
    assert container.args == application.app_entrypoint_args


def test_container_ports(container: V1Container, application: SimpleHttpApplication):
    port_name, port_no = next(iter(application.http_named_ports.items()))
    assert cast(list[V1ContainerPort], container.ports)[0] == V1ContainerPort(
        protocol="TCP", name=port_name, container_port=port_no
    )
