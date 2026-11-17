from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        AGENT = "agent", "Support Agent"
        ADMIN = "admin", "Administrator"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=30, blank=True)

    @property
    def is_agent(self) -> bool:
        """True for anyone who can manage requests (agents and admins)."""
        return self.role in (self.Role.AGENT, self.Role.ADMIN) or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username
