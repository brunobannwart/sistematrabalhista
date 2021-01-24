from django import forms

class FormCadastro(forms.Form):
	curriculo = forms.FileField(label='Curriculo')

	def clean_form(self):
		curriculo = self.cleaned_data.get('curriculo')

		return { 'curriculo': curriculo }