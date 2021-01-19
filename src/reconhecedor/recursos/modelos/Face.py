import numpy as np

class Face:
	id_ = 0
	arquivo = ''
	codigos = []
	grupo = ''

	def __init__(self, arquivo):
		self.arquivo = arquivo

	def setID(self, id_):
		self.id_ = id_

	def setArquivo(self, arquivo):
		self.arquivo = arquivo

	def setCodigos(self, codigos):
		self.codigos = codigos

	def setGrupo(self, grupo):
		self.grupo = grupo

	def getID(self):
		return self.id_

	def getArquivo(self):
		return self.arquivo

	def getCodigos(self):
		return self.codigos

	def getGrupo(self):
		return self.grupo

	def parseDados(self):
		json = {
			'id': self.id_,
			'arquivo': self.arquivo,
			'codigos': self.codigos,
			'grupo': self.grupo,
		}

		return json

	def parseJSON(self, json):
		face = Face(json['arquivo'])
		face.setID(json['id'])
		face.setGrupo(json['grupo'])

		codigos = np.array(json['codigos'])
		face.setCodigos(codigos.astype(np.float))
		return face
