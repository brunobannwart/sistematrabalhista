from flask import Flask, json, Response, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from recursos.ReconhecimentoFacial import ReconhecimentoFacial
import os

PERMITIDAS = {'png', 'jpg', 'jpeg'}

diretorio_base = os.path.abspath(os.path.dirname(__file__))
diretorio_treinamento = os.path.join(diretorio_base, 'img/treinamento')
diretorio_reconhecimento = os.path.join(diretorio_base, 'img/reconhecimento')

app = Flask(__name__)

CORS(app)

app.config.from_object('config.Config')
app.face = ReconhecimentoFacial()

def tratar_sucesso(saida, status=200, mimetype='application/json'):
	return Response(saida, status=status, mimetype=mimetype)

def tratar_erro(saida, status=500, mimetype='application/json'):
	return Response(saida, status=status, mimetype=mimetype)

def permitido(nomearquivo):
	return '.' in nomearquivo and \
		nomearquivo.rsplit('.', 1)[1].lower() in PERMITIDAS

@app.route('/api/treino', methods=['POST'])
def treino_facial():
	try:
		grupo = request.form['grupo']

		if not 'file' in request.files:
			return tratar_erro('Requer imagem')

		arquivo = request.files['file']

		if not permitido(arquivo.filename):
			return tratar_erro('Imagens suportadas: *.png , *.jpg')

		nomearquivo = secure_filename(arquivo.filename)
		caminho = os.path.join(diretorio_treinamento, nomearquivo)
		arquivo.save(caminho)

		treino = app.face.adicionarFace(caminho, grupo)
		os.remove(caminho)

		if treino:
			saida = json.dumps({'treino': treino.getID() })
			return tratar_sucesso(saida)

		return tratar_erro('Nenhuma face encontrada na imagem')

	except:
		return tratar_erro('Algum erro inesperado aconteceu')

@app.route('/api/reconhecimento', methods=['POST'])
def reconhecimento_facial():
	try:
		grupo = request.form['grupo']

		if not 'file' in request.files:
			return tratar_erro('Requer imagem')

		arquivo = request.files['file']

		if not permitido(arquivo.filename):
			return tratar_erro('Imagens suportadas: *.png , *.jpg')

		nomearquivo = secure_filename(arquivo.filename)
		caminho = os.path.join(diretorio_reconhecimento, nomearquivo)
		arquivo.save(caminho)

		encontrados = app.face.encontrarConhecidos(caminho, grupo)
		os.remove(caminho)

		if len(encontrados):
			reconhecido = encontrados[0]
			saida = json.dumps({'reconhecimento': reconhecido['id']})
			return tratar_sucesso(saida)

		return tratar_erro('Nenhuma face reconhecida na imagem')

	except:
		return tratar_erro('Algum erro inesperado aconteceu')

@app.route('/api/remover', methods=['POST'])
def remover_face():
	try:
		saida = json.dumps({'sucesso': True })
		treino = request.form['treino']

		removida = app.face.removerFace(treino)

		if removida:
			return tratar_sucesso(saida)

		return tratar_erro('Face não removida')

	except:
		return tratar_erro('Algum erro inesperado aconteceu')

app.run(host=app.config['FLASK_RUN_HOST'], port=app.config['FLASK_RUN_PORT'])