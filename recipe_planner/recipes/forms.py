from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class AddRecipeToPlanForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)
    SLOT_CHOICES = [
        (1, 'Breakfast'),
        (2, 'Lunch'),
        (3, 'Dinner'),
    ]
    slot = forms.ChoiceField(choices=SLOT_CHOICES)
    position = forms.IntegerField(min_value=0)
    recipe_id = forms.CharField()


class DateFilterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                           required=False, label='Select a date')
