from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to fields
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Confirm Password',
        })
