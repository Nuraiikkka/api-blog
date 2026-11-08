from django.contrib.auth import get_user_model
from unfold.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a user without username.
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing a user without username.
    """

    class Meta:
        model = User
        fields = "__all__"