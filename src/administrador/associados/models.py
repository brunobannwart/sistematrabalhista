from django.db import models

# Create your models here.
class Associado(models.Model):
	foto = models.ImageField(verbose_name='Foto', upload_to='foto/associado', null=False, blank=False)
	nome = models.CharField(verbose_name='Nome', max_length=45)
	data_nascimento = models.DateField(verbose_name='Data de nascimento')

	cpf = models.CharField(verbose_name='CPF', max_length=14, unique=True)
	celular = models.CharField(verbose_name='Celular', max_length=15)

	email =	models.EmailField(verbose_name='E-mail', unique=True, max_length=45)
	senha_hash = models.CharField(verbose_name='Hash senha', max_length=64)
	
	cep = models.CharField(verbose_name='CEP', max_length=10)
	numero = models.CharField(verbose_name='Número', max_length=5)

	pcd = models.BooleanField(verbose_name='PCD', default=False)
	outras_informacoes = models.TextField(verbose_name='Outras informações', blank=True, null=False, max_length=255)

	instituicao_ensino = models.TextField(verbose_name='Instituições de ensino', max_length=255, blank=True, null=False)
	curso_extra = models.TextField(verbose_name='Cursos extras', max_length=255, blank=True, null=False)

	empresa_trabalhada = models.TextField(verbose_name='Empresas trabalhadas', max_length=255, blank=True, null=False)
	cargo_ocupado = models.TextField(verbose_name='Cargos ocupados', max_length=255, blank=True, null=False)

	laudo_medico = models.CharField(verbose_name='Laudo médico', max_length=255, blank=True, null=False)
	acessibilidade = models.CharField(verbose_name='Acessibilidade', max_length=6, blank=True, null=False)
	treino = models.IntegerField(verbose_name='Treino facial', null=True)

	created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.nome

	def delete(self, *args, **kwargs):
		self.removePhoto()
		super().delete(*args, **kwargs)

	def removePhoto(self):
		self.foto.delete()

	class Meta:
		db_table = 'associado'
		verbose_name = 'Associado'
		verbose_name_plural = 'Associados'
		ordering = ['nome']