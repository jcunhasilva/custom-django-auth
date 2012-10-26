from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Profile, PublicProfile

class RegisterForm(ModelForm):
    username = forms.CharField(label=(u'Username'))
    email = forms.EmailField(label=(u'Email Address'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class':"span6"}),
            'hobbies': forms.Textarea(attrs={'rows':"6", 'class':"span6"}),
        }

    def clean_username(self):
      username = self.cleaned_data.get('username')
      try:
          User.objects.get(username=username)
      except User.DoesNotExist:
          return username
      raise forms.ValidationError('This username is already taken.')
          
          
    def clean(self):
      password = self.cleaned_data.get('password', None)
      password1 = self.cleaned_data.get('password1', None)
      if password != password1:
          raise forms.ValidationError('The password does not match its validaton. Please try again.')
      return self.cleaned_data

class RegisterPublicForm(RegisterForm):
    public_bio = forms.CharField(label=u'Public biography', required=False, max_length=1000, widget=forms.Textarea(attrs={'rows':"6", 'class':"span6"}))        
