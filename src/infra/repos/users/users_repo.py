from dataclasses import dataclass
from django.db.models import Q, QuerySet
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token

from src.infra.repos.base import GenericRepository


@dataclass(eq=False)
class UserRepository(GenericRepository):
    queryset: QuerySet = User.objects.all()
    model: User = User

    def create(self, data: dict):
        return self.model.objects.create_user(**data)


@dataclass(eq=False)
class TokenRepository(GenericRepository):
    queryset: QuerySet = Token.objects.all()
    model: Token = Token

    def get(self, query):
        try:
            return Token.objects.get(query)
        except Token.DoesNotExist:
            return None

    def create(self, user: User) -> (str, bool):
        return self.model.objects.create(user=user)

    def get_or_create(self, user: User) -> (str, bool):
        return self.model.objects.get_or_create(user=user)
