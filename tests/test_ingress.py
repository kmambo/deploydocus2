from typing import cast

from kubernetes_asyncio import V1Ingress, V1IngressRule, V1IngressSpec, V1Service

from deploydocus2.components.workloads import SimpleHttpApplication


def test_ingress_exposed(
    application: SimpleHttpApplication, ingress: V1Ingress, svc: V1Service
) -> None:
    hl_ingress = application.ingress
    assert hl_ingress is not None
    assert hl_ingress.host is not None
    v1_ingress_rules: list[V1IngressRule] = cast(
        list[V1IngressRule], cast(V1IngressSpec, ingress.spec).rules
    )
    assert v1_ingress_rules is not None and len(v1_ingress_rules) == 1
    assert v1_ingress_rules[0].host is not None
    assert len(hl_ingress.rules) == len(
        [
            rule
            for rule in ingress.spec.rules
            if rule.host is not None and rule.host == hl_ingress.host
        ]
    )
    assert hl_ingress.host == ingress.spec.rules[0].host
    assert (
        hl_ingress.rules[0].path_type == ingress.spec.rules[0].http.paths[0].path_type
    )
    assert hl_ingress.rules[0].path == ingress.spec.rules[0].http.paths[0].path
