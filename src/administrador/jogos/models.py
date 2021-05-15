from django.db import models

# Create your models here.
class Jogo(models.Model):
	logo = models.ImageField(verbose_name='Logo', upload_to='logo/jogo', null=False, blank=False)
	titulo = models.CharField(verbose_name='Titulo', max_length=50)
	url	= models.URLField(verbose_name='URL', max_length=100)
	descricao = models.TextField(verbose_name='Descrição', blank=False, null=False, max_length=150)
	created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.titulo

	def delete(self, *args, **kwargs):
		self.removeLogo()
		super().delete(*args, **kwargs)

	def removeLogo(self):
		self.logo.delete()

	class Meta:
		db_table = 'jogo'
		verbose_name = 'Jogo'
		verbose_name_plural = 'Jogos'
		ordering = ['titulo']