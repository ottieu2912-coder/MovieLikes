from django.contrib.auth.models import User
from django.forms import ModelForm

#A user form that is used to for new user registration
class UserForm(ModelForm):
	class META:
		model= User
		fields=['username', 'password', 'email']
		