import pytest

from deploydocus2.components.models import DeploydocusComponent
from deploydocus2.components.workloads.httpapps import (
    HttpIngressRule,
    HttpLivenessProbe,
    HttpReadinessProbe,
    SimpleHttpApplication,
)
from deploydocus2.pkg import InstanceSettings


@pytest.fixture
def application():
    return SimpleHttpApplication(
        instance=InstanceSettings(
            name="simple-http-app",
            namespace="test-ns",
        ),
        http_named_ports={
            "https": 8443,
            "http": 8080,
        },
        liveness_probe=HttpLivenessProbe(rel_url="/liveness"),
        readiness_probe=HttpReadinessProbe(),
        ingress=HttpIngressRule(
            host="api.mytestapp.org",
            path="/api/*",
        ),
    )


def test_component_to_k8s(application: DeploydocusComponent): ...
