from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Bet, Team, Player, Match


'''class CustomUserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True)

 class Meta(UserCreationForm.Meta):
   model = User
     fields = ('username', 'email', 'password1', 'password2')

class CustomPasswordResetForm(PasswordResetForm):
   email = forms.EmailField(required=True)

   class Meta:
#       model = User
#       fields = ('email',)'''

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm password does not match"
            )


class TeamForm(forms.ModelForm):#to creat or edit "Team" instance
    class Meta:
        model = Team
        fields = ['name', 'logo', 'location', 'coach_name']


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'team', 'player_number']


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'match_time', 'venue', 'status']


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['chosen_team', 'amount']
