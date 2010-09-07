from django import forms
from accounts.models import User
from django.utils.translation import ugettext_lazy as _

class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password_verify = forms.CharField(widget=forms.PasswordInput,
                                          required=False,
                                          label=_(u'Confirm new password:'))    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo', 'biography', 'email')
        
    def clean(self):
        current, new, verify = map(self.cleaned_data.get,
                    ('current_password', 'new_password', 'new_password_verify'))
        if current and not self.instance.check_password(current):
            raise forms.ValidationError(_(u'Invalid password.'))
        if new and new != verify:
            raise forms.ValidationError(_(u'The two passwords did not match.'))
        if not self.cleaned_data['photo']:
            del self.cleaned_data['photo']
        return self.cleaned_data
    
    def clean_email(self):
        value = self.cleaned_data['email']
        if value:
            try:
                User.objects.exclude(pk=self.instance.pk).get(email=value)
                raise forms.ValidationError(_(u'This email is used already.'))
            except User.DoesNotExist:
                pass
        return value
    
    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)        