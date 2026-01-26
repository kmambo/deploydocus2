from typing import cast

from kubernetes import (
    V1Deployment,
    V1DeploymentSpec,
    V1ObjectMeta,
    V1Service,
    V1ServiceSpec,
)

from deploydocus2.components.workloads.httpapps import (
    HttpK8sComponentsModel,
    SimpleHttpApplication,
)


def test_svc_rendered(http_k8s_component: HttpK8sComponentsModel):
    svcs = http_k8s_component.render_services()
    assert svcs is not None
    assert len(svcs) == 1
    assert isinstance(svcs[0], V1Service)


def test_svc_selects_deployment_pods(
    svc: V1Service,
    deployment: V1Deployment,
):
    deployment_spec = cast(V1DeploymentSpec, deployment.spec)
    # only if there are no additional labels
    pod_template = deployment_spec.template
    assert (
        cast(dict[str, str], cast(V1ServiceSpec, svc.spec).selector).items()
        <= cast(
            dict[str, str], cast(V1ObjectMeta, pod_template.metadata).labels
        ).items()
    )


def test_svc_from_hl_application(svc: V1Service, application: SimpleHttpApplication):
    assert (
        cast(V1ObjectMeta, svc.metadata).name
        == f"{application.instance_name}-{application.app_name}-svc"
    )
