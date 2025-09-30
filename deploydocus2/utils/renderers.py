import json
from typing import cast

import yaml

from deploydocus2 import K8sModel, K8sModelSequence


def render(obj: K8sModelSequence | K8sModel, fmt="python") -> str:
    """Render a single Kubernetes object as YAML, JSON or a Python dict;
    Or a sequence of Kubernetes objects as YAML, JSON or list of Python dicts.
    Each of these are then converted to a string

    Args:
        obj: Must be a sequence of Kubernetes objects (usually a list)
            or a single Kubernetes object.
        fmt: The default is 'dict' and will return the dictionary as a string.
        The other valid values are 'yaml' and

    Returns:
        The rendered YAML, JSON or Python dictionary.
    """
    accepted_fmts = ["yaml", "json", "python"]
    if not fmt.lower() in accepted_fmts:
        raise ValueError(f"Invalid format {fmt}: Expected one of {accepted_fmts}")
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return str(obj.to_dict())
    else:  # assume a sequence of K8sModels
        ret2 = [x.to_dict() for x in cast(K8sModelSequence, obj)]
        match fmt.lower():
            case "python":
                return str(ret2)
            case "yaml":
                return yaml.safe_dump_all(ret2)
            case "json":
                return json.dumps(ret2)
            case _:
                return ""  # it should never get here
