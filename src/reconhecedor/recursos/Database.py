import mysql.connector as mysql

class Database:
	def __init__(self):
		self.conexao = mysql.connect(host='localhost', user='tr_reconhecedor', password='reconhecedor$trabalhista', database='db_trabalhista', auth_plugin='mysql_native_password')
		
		self.cursor = self.conexao.cursor()
		self.__criarTabela()

	def __criarTabela(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `treinamento`(`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `foto` VARCHAR(100), `codificações` TEXT, `grupo` VARCHAR(100)) ENGINE=InnoDB")

	def obterFaces(self):
		faces = []

		self.cursor.execute("SELECT * FROM `treinamento`")
		resultados = self.cursor.fetchall()

		for resultado in resultados:
			id_ = resultado[0]
			arquivo = resultado[1]
			codigos = resultado[2].split(',')
			grupo = resultado[3]

			face = {
				'id': id_,
				'arquivo': arquivo,
				'codigos': codigos,
				'grupo': grupo
			}

			faces.append(face)	
		return faces

	def salvarFace(self, arquivo, codigos, grupo):
		self.cursor.execute("INSERT INTO `treinamento`(`foto`, `codificações`, `grupo`) VALUES (%s, %s, %s)",
				[arquivo, codigos, grupo])
		self.conexao.commit()
		return self.cursor.lastrowid

	def deletarFace(self, id_):
		try:
			self.cursor.execute("DELETE FROM `treinamento` WHERE `id`=%s", [id_])
			self.conexao.commit()
			return True
		except:
			return False
