from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Inserire Titolo"}))
    text = forms.CharField

    class Meta:
        model = Post
        fields = ('title', 'text')

# Richiesta n°7 sistema di controllo che impedisca la creazione di post con la parola "Hack"
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "hack" in title or "HACK" in title or "Hack" in title or "H4CK" in title or "H4ck" in title or "h4ck" in title:
            raise forms.ValidationError("Non puoi creare contenuti che contengano il termine Hack")
        return title

    def clean_text(self, *args, **kwargs):
        text = self.cleaned_data.get("text")
        if "hack" in text or "HACK" in text or "Hack" in text or "H4CK" in text or "H4ck" in text or "h4ck" in text:
            raise forms.ValidationError("Non puoi creare contenuti che contengano il termine Hack")
        return text