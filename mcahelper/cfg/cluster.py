from io import IOBase
from pathlib import Path

import tomllib
from pydantic import BaseModel


class _Frames(BaseModel):
    test: int
    prod: int


class ClusterCfg(BaseModel):
    frames: _Frames
    stdQP: dict[str, list[int]]


_CLUSTER_CFG = None


def load(f: IOBase) -> ClusterCfg:
    return ClusterCfg(**tomllib.load(f))


def from_file(path: Path) -> ClusterCfg:
    path = Path(path)
    with path.open('rb') as f:
        return load(f)


def set_cluster_cfg(path: Path) -> ClusterCfg:
    global _CLUSTER_CFG
    _CLUSTER_CFG = from_file(path)
    return _CLUSTER_CFG


def get_cluster_cfg() -> ClusterCfg | None:
    return _CLUSTER_CFG
