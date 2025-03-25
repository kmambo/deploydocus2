from abc import ABC, abstractmethod
from typing import Self, Sequence

import pydantic as pyd

from .pkg import K8sModel


class Component(pyd.BaseModel, ABC):
    """Represents a self-contained 'microservice' or an 'application'. This is the
    source from which a set of Kubernetes manifests will be generated and locked.
    Roughly the equivalent of a Helm chart
    """

    _lock: Sequence[K8sModel | Self]
    locked: bool = pyd.Field(default=False, exclude=True)

    @abstractmethod
    def gen_lock(self):
        """Regenerate the locked version of the component.

        Returns:

        """
        ...

    @pyd.computed_field
    def lock(self) -> Sequence[K8sModel | Self]:
        return self._lock
