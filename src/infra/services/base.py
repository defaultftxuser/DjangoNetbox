from abc import ABC
from dataclasses import dataclass

from src.infra.repos.base import GenericRepository


@dataclass(eq=False)
class BaseService(ABC):
    repository: GenericRepository
