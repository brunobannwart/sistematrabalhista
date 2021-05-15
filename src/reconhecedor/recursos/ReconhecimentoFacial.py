import cv2, face_recognition, os, pickle
import numpy as np
from .Database import Database
from .modelos.Face import Face

class ReconhecimentoFacial:
	def __init__(self, tolerancia=0.6):
		self.tolerancia = tolerancia
		self.conhecidos = []
		self.db = Database()
		self.__carregarFaces()

	def __carregarFaces(self):
		faces = self.db.obterFaces()

		for face in faces:
			self.conhecidos.append(Face.parseJSON(self, face))

	def __novaFace(self, face):
		json = face.parseDados()
		arquivo = json['arquivo']
		codigos = json['codigos']
		grupo = json['grupo']

		codificacao = ','.join([str(codigo) for codigo in codigos])

		return self.db.salvarFace(arquivo, codificacao, grupo)

	def __encontrarFaces(self, caminho):
		faces = []

		imagem = face_recognition.load_image_file(caminho)
		arquivo = os.path.basename(caminho)
		localizacao = face_recognition.face_locations(imagem)
		codigos = face_recognition.face_encodings(imagem, localizacao)

		for codigo in codigos:
			face = Face(arquivo)
			face.setCodigos(codigo)
			faces.append(face)

		return faces

	def __encontrarCombinacao(self, conhecidos, face):
		combinacao = []
		combinacao = face_recognition.compare_faces(conhecidos, face.getCodigos(), tolerance=self.tolerancia)
		return combinacao

	def adicionarFace(self, caminho, grupo):
		faces = self.__encontrarFaces(caminho)

		if len(faces):
			faces[0].setGrupo(grupo)
			id_ = self.__novaFace(faces[0])
			faces[0].setID(id_)
			self.conhecidos.append(faces[0])
			return faces[0]

		return None

	def removerFace(self, id_):
		contador = 0

		for conhecido in self.conhecidos:
			if conhecido.getID() == int(id_):
				if self.db.deletarFace(id_):
					self.conhecidos.pop(contador)
					return True

				return False

			contador += 1

		return False

	def encontrarConhecidos(self, caminho, grupo):
		encontrados = []
		conhecidosGrupo = []
		codigos = []

		faces = self.__encontrarFaces(caminho)

		for conhecido in self.conhecidos:
			if conhecido.getGrupo() == grupo:
				conhecidosGrupo.append(conhecido)

		for conhecidoGrupo in conhecidosGrupo:
			codigos.append(conhecidoGrupo.getCodigos())
		for face in faces:
			combinacao = self.__encontrarCombinacao(codigos, face)

			if len(combinacao) and True in combinacao:
				indice = combinacao.index(True)
				encontrado = conhecidosGrupo[indice]
				encontrados.append(encontrado.parseDados())

		return encontrados

