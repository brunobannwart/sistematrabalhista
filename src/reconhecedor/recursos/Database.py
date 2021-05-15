import mysql.connector as mysql

class Database:
	def __init__(self):
		conexao = mysql.connect(host='db_trabalhista.mysql.dbaas.com.br', user='db_trabalhista', password='Myext123@', database='db_trabalhista', auth_plugin='mysql_native_password')
		cursor = conexao.cursor()

		self.__criarTabela(cursor)
		
		cursor.close()
		conexao.close()

	def __criarTabela(self, cursor):
		cursor.execute("CREATE TABLE IF NOT EXISTS `treinamento`(`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `foto` VARCHAR(100), `codificações` TEXT, `grupo` VARCHAR(100)) ENGINE=InnoDB")

	def obterFaces(self):
		conexao = mysql.connect(host='db_trabalhista.mysql.dbaas.com.br', user='db_trabalhista', password='Myext123@', database='db_trabalhista', auth_plugin='mysql_native_password')
		cursor = conexao.cursor()

		faces = []

		cursor.execute("SELECT * FROM `treinamento`")
		resultados = cursor.fetchall()

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
		cursor.close()
		conexao.close()	
		return faces

	def salvarFace(self, arquivo, codigos, grupo):
		conexao = mysql.connect(host='db_trabalhista.mysql.dbaas.com.br', user='db_trabalhista', password='Myext123@', database='db_trabalhista', auth_plugin='mysql_native_password')
		cursor = conexao.cursor()

		cursor.execute("INSERT INTO `treinamento`(`foto`, `codificações`, `grupo`) VALUES (%s, %s, %s)",
				[arquivo, codigos, grupo])
		conexao.commit()
		cursor.close()
		conexao.close()
		return cursor.lastrowid

	def deletarFace(self, id_):
		conexao = mysql.connect(host='db_trabalhista.mysql.dbaas.com.br', user='db_trabalhista', password='Myext123@', database='db_trabalhista', auth_plugin='mysql_native_password')
		cursor = conexao.cursor()

		try:
			cursor.execute("DELETE FROM `treinamento` WHERE `id`=%s", [id_])
			conexao.commit()
			cursor.close()
			conexao.close() 
			return True
		except:
			cursor.close()
			conexao.close() 
			return False
