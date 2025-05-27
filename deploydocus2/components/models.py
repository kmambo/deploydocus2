from abc import ABC, abstractmethod

import pydantic as pyd

from deploydocus2.pkg import K8sComponentModel


class DeploydocusComponent(pyd.BaseModel, ABC):
    """Represents a self-contained 'microservice' or an 'application'. This is the
    source from which a set of Kubernetes manifests will be generated and locked.
    Roughly the equivalent of a Helm chart
    """

    @abstractmethod
    def gen_k8s_components(self) -> K8sComponentModel:
        """Generate a"""
        ...
