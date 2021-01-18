from django import forms
import hashlib

class FormCadastro(forms.Form):
	nome = forms.CharField(label='Nome', max_length=45)
	email =	forms.EmailField(label='Email')
	senha =	forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
	foto = forms.ImageField(label='Foto')

	def clean_form(self):
		foto = self.cleaned_data.get('foto')
		nome = self.cleaned_data.get('nome')
		email =	self.cleaned_data.get('email')
		senha =	self.cleaned_data.get('senha')

		senha_hash = hashlib.sha256(senha.encode()).hexdigest()

		return { 
			'foto': foto,
			'nome': nome, 
			'email': email, 
			'senha_hash': senha_hash,  
		}

class FormEditar(forms.Form):
	nome = forms.CharField(label='Nome', max_length=45)
	email =	forms.EmailField(label='Email')
	senha =	forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
	foto = forms.ImageField(label='Foto', required=False)

	def clean_form(self):
		foto = self.cleaned_data.get('foto')
		nome = self.cleaned_data.get('nome')
		email =	self.cleaned_data.get('email')
		senha =	self.cleaned_data.get('senha')

		senha_hash = hashlib.sha256(senha.encode()).hexdigest()

		return { 
			'foto': foto,
			'nome': nome, 
			'email': email, 
			'senha_hash': senha_hash,  
		}