from django import forms
import hashlib

class FormLogin(forms.Form):
	email = forms.EmailField(label='email')
	senha = forms.CharField(label='senha', max_length=100, widget=forms.PasswordInput)

	def clean_form(self):
		email = self.cleaned_data.get('email')
		senha = self.cleaned_data.get('senha')

		senha_hash = hashlib.sha256(senha.encode()).hexdigest()

		return { 'email': email, 'senha_hash': senha_hash }