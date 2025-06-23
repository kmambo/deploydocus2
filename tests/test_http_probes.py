from typing import cast

from kubernetes_asyncio.models import V1HTTPGetAction, V1Probe

from deploydocus2.components.workloads import HttpLivenessProbe


def test_http_liveness_probe(
    container_liveness_probe: V1Probe, http_liveness_probe: HttpLivenessProbe
) -> None:
    assert (
        not (http_liveness_probe or container_liveness_probe)
        if http_liveness_probe is None
        else (
            http_liveness_probe.delay_first_probe
            == cast(V1Probe, container_liveness_probe).initial_delay_seconds
        )
    )

    assert "httpGet" in container_liveness_probe.to_dict()
    assert (
        container_liveness_probe.initial_delay_seconds is None
        and cast(HttpLivenessProbe, http_liveness_probe).delay_first_probe is None
    )
    assert (
        cast(V1HTTPGetAction, container_liveness_probe.http_get).path
        == cast(HttpLivenessProbe, http_liveness_probe).rel_url
    )

    assert (
        cast(V1Probe, container_liveness_probe).period_seconds
        == cast(HttpLivenessProbe, http_liveness_probe).check_freq
    )
