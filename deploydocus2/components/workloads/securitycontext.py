from typing import TypeAlias

from kubernetes import (
    V1AppArmorProfile,
    V1Capabilities,
    V1PodSecurityContext,
    V1SeccompProfile,
    V1SecurityContext,
)

sane_app_armor_profile = V1AppArmorProfile(
    type="RuntimeDefault",
)
sane_seccomp_profile = V1SeccompProfile(
    type="RuntimeDefault",
)
SanePodSecurityContext = V1PodSecurityContext(
    app_armor_profile=sane_app_armor_profile,
    run_as_non_root=True,
    run_as_group=1000,  # arbitrarily chosen, can be changed
    run_as_user=1000,  # arbitrarily chosen, can be changed
    seccomp_profile=sane_seccomp_profile,
)

ContainerSecurityContext: TypeAlias = V1SecurityContext
sane_container_capabilities = V1Capabilities(
    drop=[
        "ALL",
    ]
)
sane_container_security_context = ContainerSecurityContext(
    allow_privilege_escalation=False,
    capabilities=sane_container_capabilities,
    privileged=False,
    app_armor_profile=sane_app_armor_profile,
    run_as_non_root=True,
    run_as_group=1000,  # arbitrarily chosen, can be changed
    run_as_user=1000,  # arbitrarily chosen, can be changed
    seccomp_profile=sane_seccomp_profile,
)
