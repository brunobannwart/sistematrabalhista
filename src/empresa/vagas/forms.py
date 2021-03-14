from django import forms

# Create your form here.
class FormCadastro(forms.Form):
	titulo = forms.CharField(label='Titulo', max_length=50)
	data_exp = forms.DateField(label='Data de expiração')
	descricao =	forms.CharField(label='Descrição', widget=forms.Textarea, max_length=255)
	logo = forms.ImageField(label='logo')

	def clean_form(self):
		logo = self.cleaned_data.get('logo')
		titulo = self.cleaned_data.get('titulo')
		data_exp = self.cleaned_data.get('data_exp')
		descricao =	self.cleaned_data.get('descricao')

		return { 'logo': logo, 'titulo': titulo, 'data_exp': data_exp, 'descricao': descricao }

class FormEditar(forms.Form):
	titulo = forms.CharField(label='Titulo', max_length=50)
	data_exp = forms.DateField(label='Data de expiração')
	descricao = forms.CharField(label='Descrição', widget=forms.Textarea, max_length=255)
	logo = forms.ImageField(label='logo', required=False)

	def clean_form(self):
		logo = self.cleaned_data.get('logo')
		titulo = self.cleaned_data.get('titulo')
		data_exp = self.cleaned_data.get('data_exp')
		descricao =	self.cleaned_data.get('descricao')

		return { 'logo': logo, 'titulo': titulo, 'data_exp': data_exp, 'descricao': descricao }