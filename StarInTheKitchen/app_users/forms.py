from cloudinary import CloudinaryResource
from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from StarInTheKitchen.app_users.widgets import CustomClearableFileInput
from StarInTheKitchen.app_users.models import Profile
import cloudinary.uploader
UserModel = get_user_model()


class AppUserForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        min_length=2
    )

    last_name = forms.CharField(
        max_length=150,
        min_length=2
    )

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            "password2": "Confirm password"
        }

    def save(self, commit=True):
        user = super().save(commit=commit)

        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        profile = user.profile
        profile.first_name = first_name
        profile.last_name = last_name

        profile.save()

        return user


class EditAppUserForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_picture')
        widgets = {
            'profile_picture': ClearableFileInput(),
        }
        labels = {
            'profile_picture': 'Change image'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

        profile_pic = self.instance.profile_picture
        is_default = False
        if profile_pic and hasattr(profile_pic, 'public_id'):
            is_default = 'default_profile_picture' in profile_pic.public_id or "default-user" in profile_pic.public_id
        self.fields['profile_picture'].widget = CustomClearableFileInput(is_default=is_default)
        # if self.instance.profile_picture and 'default_profile_picture' in str(self.instance.profile_picture):
        #     self.fields['profile_picture'].widget.clear_checkbox_label = ''
        #     self.fields['profile_picture'].widget.attrs['hidden-clear'] = 'true'

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data['profile_picture']

        if profile_picture is False:
            return False

        if not profile_picture:
            return self.instance.profile_picture

        if isinstance(profile_picture, CloudinaryResource):
            return profile_picture
        try:
            img = Image.open(profile_picture)
            img.verify()

            return profile_picture
        except:
            raise ValidationError('Profile picture needs to be an image.')

    def save(self, commit=True):
        profile = super().save(commit=False)

        user = profile.user
        email = self.cleaned_data.get('email')

        if email:
            user.email = email
            user.save()

        new_picture = self.cleaned_data.get('profile_picture')
        old_picture = self.instance.profile_picture

        if new_picture is False:
            if old_picture and hasattr(old_picture,
                                       'public_id') and 'default_profile_picture' not in old_picture.public_id:
                cloudinary.uploader.destroy(old_picture.public_id)
            profile.profile_picture = None

        elif new_picture and new_picture != old_picture:
            if old_picture and hasattr(old_picture,
                                       'public_id') and 'default_profile_picture' not in old_picture.public_id:
                cloudinary.uploader.destroy(old_picture.public_id)

        # if self.cleaned_data.get('profile_picture') is False:
        #     profile.profile_picture = None

        if commit:
            profile.save()

        return profile


class DeleteAppUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = 'readonly'
            self.fields[field].disabled = 'disabled'
