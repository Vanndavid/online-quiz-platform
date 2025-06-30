from django.forms import ModelForm
from .models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
