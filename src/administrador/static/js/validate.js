async function validarCEP(entrada) {
	var cep, valido;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('erro_endereco');
	const titulo = document.getElementById('titulo_endereco');
	const rua = document.getElementById('rua');
	const bairro = document.getElementById('bairro');
	const cidade = document.getElementById('cidade');
	const estado = document.getElementById('estado');
	const mensagem = document.getElementById('erro');
	const leitor = document.getElementById('erro_leitor');

	valido = document.getElementById('endereco_valido');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	rua.style.display = 'none';
	bairro.style.display = 'none';
	cidade.style.display = 'none';
	estado.style.display = 'none';
	mensagem.style.display = 'none';

	cep = entrada.value.replace(exp, '');

	const parametros = {
		method: 'GET',
		mode: 'cors',
		cache: 'default'
	}

	if (cep.length == 8) {
		await fetch(`https://viacep.com.br/ws/${cep}/json/`, parametros)
			.then(resposta => {
				resposta.json().then(dados => {
					if (dados.erro != true) {
						if (!leitor) {
							bloco.style.display = 'block';
							titulo.style.display = 'block';
							rua.style.display = 'block';
							bairro.style.display = 'block';
							cidade.style.display = 'block';
							estado.style.display = 'block';
							titulo.innerHTML = 'CEP';
				  			rua.innerHTML = dados.logradouro;
				  			bairro.innerHTML = dados.bairro;
				  			cidade.innerHTML = dados.localidade;
				  			estado.innerHTML = dados.uf;
				  		}

			  			valido.value = 'sim';

					} else {
						if (!leitor) {
							bloco.style.display = 'block';
							titulo.style.display = 'block';
							mensagem.style.display = 'block';
							titulo.innerHTML = 'Aviso';
							mensagem.innerHTML = 'Informe um CEP válido';
						} else {
							audio('Informe um CEP válido');
						}

						valido.value = 'nao';
					}
				});
			})
			.catch(erro => {
				if (!leitor) {
					bloco.style.display = 'block';
					titulo.style.display = 'block';
					mensagem.style.display = 'block';
					titulo.innerHTML = 'Aviso';
					mensagem.innerHTML = 'Informe um CEP válido';
				} else {
					audio('Informe um CEP válido');
				}

				valido.value = 'nao';
			});
	}
}

function validarCPF(entrada) {
	var cpf, valido, numeros, digitos, soma, resultado, i, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('erro_documento');
	const titulo = document.getElementById('titulo_documento');
	const mensagem = document.getElementById('mensagem_documento');
	const leitor = document.getElementById('erro_leitor');

	valido = document.getElementById('documento_valido');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cpf = entrada.value.replace(exp, '');

	if (cpf.length == 11) {
		controle = 0;
		iguais = 1;

		for (i = 0; i < cpf.length - 1; i++) {
			if (cpf.charAt(i) != cpf.charAt(i + 1)) {
				iguais = 0;
				break;
			}
		}

		if (!iguais) {
			numeros = cpf.substring(0, 9);
			digitos = cpf.substring(9);
			soma = 0;

			for (i = 10; i > 1; i--) {
				soma += numeros.charAt(10 - i) * i;
			}

			resultado = (soma * 10) % 11;

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				numeros = cpf.substring(0, 10);
				soma = 0;

				for (i = 11; i > 1; i--) {
					soma += numeros.charAt(11 - i) * i;
				}

				resultado = (soma * 10) % 11;

				if (resultado != digitos.charAt(1)) {
					controle = 0;
				} else {
					controle = 1;
				}
			}
		} else {
			controle = 0;
		}

		if (!controle) {
			if (!leitor) {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'Informe um documento válido';
			} else {
				audio('Informe um documento válido');
			}

			valido.value = 'nao';
		} else {
			valido.value = 'sim';
		}
	}
}

function validarCNPJ(entrada) {
	var cnpj, valido, posicao, tamanho, numeros, digitos, soma, resultado, i, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('erro_documento');
	const titulo = document.getElementById('titulo_documento');
	const mensagem = document.getElementById('mensagem_documento');
	const leitor = document.getElementById('erro_leitor');

	valido = document.getElementById('documento_valido');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cnpj = entrada.value.replace(exp, '');

	if (cnpj.length == 14) {
		controle = 0;
		iguais = 1;

		for (i = 0; i < cnpj.length - 1; i++) {
			if (cnpj.charAt(i) != cnpj.charAt(i + 1)) {
				iguais = 0;
				break;
			}
		}

		if (!iguais) {
			tamanho = cnpj.length - 2;
			numeros = cnpj.substring(0, tamanho);
			digitos = cnpj.substring(tamanho);
			soma = 0;
			posicao = tamanho - 7;

			for (i = tamanho; i >= 1; i--) {
				soma += numeros.charAt(tamanho - i) * posicao--;
				if (posicao < 2) {
					posicao = 9;
				}
			}

			resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				tamanho += 1;
				numeros = cnpj.substring(0, tamanho);
				soma = 0;
				posicao = tamanho - 7;

				for (i = tamanho; i >= 1; i--) {
					soma += numeros.charAt(tamanho - i) * posicao--;
					if (posicao < 2) {
						posicao = 9;
					}
				}

				resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;

				if (resultado != digitos.charAt(1)) {
          			controle = 0;

				} else {
					controle = 1;
				}
			}

		} else {
			controle = 0;
		}

		if (!controle) {
			if (!leitor) {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'Informe um documento válido';
			} else {
				audio('Informe um documento válido');
			}

			valido.value = 'nao';
		} else {
			valido.value = 'sim';
		}
	}
}

function validarDados() {
	const documento = document.getElementById('documento_valido').value;
	const endereco = document.getElementById('endereco_valido').value;
	const botao = documento.getElementById('salvar');

	const bloco = document.getElementById('erro_documento');
	const titulo = document.getElementById('titulo_documento');
	const mensagem = document.getElementById('mensagem_documento');
	const leitor = document.getElementById('erro_leitor');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	if (documento == 'sim' && endereco == 'sim') {
		botao.disabled = true;
		return true;
	} 

	if (documento == 'sim' && endereco == 'nao') {
		if (!leitor) {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'CEP continua inválido';
		} else {
			audio('CEP continua inválido');
		}
	}

	if (documento == 'nao' && endereco == 'sim') {
		if (!leitor) {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'Documento continua inválido';
		} else {
			audio('Documento continua inválido');
		}
	}

	if (documento == 'nao' && endereco == 'nao') {
		if (!leitor) {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'Documento e CEP continuam inválidos';
		} else {
			audio('Documento e CEP continuam inválidos');
		}
	}

	botao.disabled = false;
	return false;
}