from typing import cast

from kubernetes_asyncio.models import V1HTTPGetAction, V1Probe

from deploydocus2.components.workloads import (
    HttpLivenessProbe,
    HttpReadinessProbe,
    HttpStartupProbe,
)


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


def test_http_readiness_probe(
    container_readiness_probe: V1Probe, http_readiness_probe: HttpReadinessProbe
) -> None:
    assert "httpGet" in container_readiness_probe.to_dict()
    assert (
        cast(V1HTTPGetAction, container_readiness_probe.http_get).path
        == cast(HttpLivenessProbe, http_readiness_probe).rel_url
    )

    assert (
        cast(V1Probe, container_readiness_probe).period_seconds
        == cast(HttpLivenessProbe, http_readiness_probe).check_freq
    )


def test_http_startup_probe(
    container_startup_probe: V1Probe, http_startup_probe: HttpStartupProbe
) -> None:
    assert (
        container_startup_probe is None
        or "httpGet" in container_startup_probe.to_dict()
    )
    assert (
        container_startup_probe is None
        and http_startup_probe is None
        or cast(V1HTTPGetAction, container_startup_probe.http_get).path
        == cast(HttpStartupProbe, http_startup_probe).rel_url
    )

    assert (
        container_startup_probe is None
        and http_startup_probe is None
        or cast(V1Probe, container_startup_probe).period_seconds
        == cast(HttpStartupProbe, http_startup_probe).check_freq
    )
