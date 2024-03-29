from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser


class LoginForm(forms.Form):
	username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'youremail@provider.com'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

	def clean_password2(self):
        # Check that the two password entries match

		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if len(password1) < 5:
			raise forms.ValidationError("Password is too short")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			exists = MyUser.objects.get(username=username)
			if exists:
				raise forms.ValidationError("This usernam is taken")
		except MyUser.DoesNotExist:
			return username
		except:
			raise forms.ValidationError("There was an error, please try again or contact us.")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			exists = MyUser.objects.get(email=email)
			raise forms.ValidationError("This email is taken")
		except MyUser.DoesNotExist:
			return email
		except:
			raise forms.ValidationError("There was an error, please try again or contact us.")

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = MyUser
		fields = ('email', 'username', 'first_name', 'last_name')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
		    raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
		    user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = MyUser
		fields = ('username', 'email', 'password', 'username', 'first_name', 'last_name', 'is_member', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]
