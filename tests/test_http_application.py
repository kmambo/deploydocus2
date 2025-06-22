from typing import Any, cast

import pytest
from kubernetes_asyncio import V1Container, V1Deployment, V1HTTPGetAction, V1Probe

from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.components.workloads.httpapps import (
    HttpK8sComponentsModel,
    HttpLivenessProbe,
    SimpleHttpApplication,
)
from deploydocus2.pkg import K8sComponentsModel


@pytest.mark.skip("Not now...")
def test_component_to_k8s(application: DeploydocusComponent):
    pass


def test_render_namespace(http_k8s_component: K8sComponentsModel):
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
    deployment_selector: dict = deployment_spec["selector"]["matchLabels"]
    pod_template_labels: dict = deployment_spec["template"]["metadata"]["labels"]
    assert deployment_selector.items() <= pod_template_labels.items()
    assert pod_spec["serviceAccountName"] == f"{deployment_dict['metadata']['name']}-sa"


def test_container(container: V1Container, application: SimpleHttpApplication):
    assert container.image == application.app_image
    assert container.command == application.app_command
    assert not container.env
    assert container.args == application.app_entrypoint_args
    assert (
        not (application.liveness_probe or container.liveness_probe)
        if application.liveness_probe is None
        else (
            application.liveness_probe.delay_first_probe
            == cast(V1Probe, container.liveness_probe).initial_delay_seconds
        )
    )
    liveness_probe = cast(V1Probe, container.liveness_probe)

    assert "httpGet" in liveness_probe.to_dict()
    assert (
        liveness_probe.initial_delay_seconds is None
        and cast(HttpLivenessProbe, application.liveness_probe).delay_first_probe
        is None
    )
    assert (
        cast(V1HTTPGetAction, liveness_probe.http_get).path
        == cast(HttpLivenessProbe, application.liveness_probe).rel_url
    )
