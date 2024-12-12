from abc import ABC
from dataclasses import dataclass

from django.db import IntegrityError

from src.infra.exceptions.repo_exceptions import UserAlreadyExistsException
from src.infra.repos.base import GenericRepository
from src.infra.repos.users.users_repo import UserRepository, TokenRepository
from src.infra.services.base import BaseService


@dataclass(eq=False)
class BaseUserService(ABC):
    repository: GenericRepository
    token_repository: GenericRepository


@dataclass(eq=False)
class UserService(BaseUserService):
    repository: UserRepository
    token_repository: TokenRepository

    def create(self, data: dict):
        try:
            user = self.repository.create(data=data)
            saved_user = self.repository.save(instance=user)
            token, created = self.token_repository.get_or_create(user=saved_user)
            return token
        except IntegrityError:
            raise UserAlreadyExistsException()
