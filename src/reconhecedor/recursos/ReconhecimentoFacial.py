import cv2, face_recognition, os, pickle
import numpy as np
from .Database import Database
from .models.Face import Face

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
		treino = []

		imagem = face_recognition.load_image_file(caminho)
		arquivo = os.path.basename(caminho)
		localizacao = face_recognition.face_locations(imagem)
		codigos = face_recognition.face_encodings(imagem, localizacao)

		for codigo in codigos:
			face = Face(arquivo)
			face.setCodigos(codigo)
			treino.append(face)

		return treino

	def __foiEncontrado(self, conhecidos, face):
		encontrados = []
		encontrados = face_recognition.compare_faces(conhecidos, face.getCodigos(), tolerance=self.tolerancia)
		return encontrados

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
