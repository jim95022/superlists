from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models


class Token(models.Model):
    """Маркер"""
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    """менеджер пользователя списка"""

    def create_user(self, email):
        """Создать пользователя"""
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """создать супервользователя"""
        self.create_superuser(email) # ??


class ListUser(AbstractBaseUser, PermissionsMixin):
    """Пользователь списка"""
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email", "height"]

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == "jim95022@gmail.com"

    @property
    def is_active(self):
        return True
