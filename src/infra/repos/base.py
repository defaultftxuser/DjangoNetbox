from dataclasses import dataclass

from django.db.models import Model, QuerySet, Q

@dataclass(eq=False)
class GenericRepository:
    model: Model
    queryset: QuerySet

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, expression: Q):
        try:
            return self.queryset.get(expression)
        except self.model.DoesNotExist:
            return None

    def filter(self, expression: Q):
        return self.queryset.filter(expression)

    def get_by_pk(self, pk: int):
        try:
            return self.queryset.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get_list(self):
        return list(self.queryset)

    def get_all(self):
        return self.queryset

    def create(self, data: dict):
        return self.model.objects.create(**data)

    def bulk_create(self, data: list[dict]):
        instances = [self.model(**item) for item in data]
        return self.model.objects.bulk_create(instances)

    def delete(self, expression: Q):
        return self.queryset.filter(expression).delete()

    def update(self, pk: int, data: dict) -> QuerySet:
        instance = self.get_by_pk(pk)
        if instance:
            for field, value in data.items():
                setattr(instance, field, value)
        return instance

    def partial_update(self, pk: int, data: dict) -> QuerySet:
        instance = self.get_by_pk(pk)
        if instance:
            for field, value in data.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)
        return instance

    @staticmethod
    def save(instance):
        instance.save()
        return instance
