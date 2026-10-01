from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import BooleanField, CharField, EmailField


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password):
        user = self.model(
            email = self.normalize_email(email).lower(),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save()
        return user 
        
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    NAME_MAX_LEN = 50
    email = EmailField(
        unique = True,
    )
    first_name = CharField(
        max_length = NAME_MAX_LEN
    )
    last_name = CharField(
        max_length = NAME_MAX_LEN
    )
    is_active = BooleanField(
        default = True
    )
    is_staff = BooleanField(
        default = False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'first_name', 'last_name'
