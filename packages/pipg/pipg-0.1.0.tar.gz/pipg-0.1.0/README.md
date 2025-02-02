# pipg - Wrapper para Pip

`pipg` é um wrapper para `pip` que facilita a instalação e remoção de pacotes Python, mantendo automaticamente um arquivo `requirements.txt` atualizado.

## 🚀 Funcionalidades
- Instala pacotes com `pipg install <pacote>`.
- Remove pacotes com `pipg uninstall <pacote>`.
- Atualiza automaticamente o `requirements.txt` com a versão correta dos pacotes instalados.
- Mensagens coloridas para melhor visualização dos status.

## 📦 Instalação
Para instalar o `pipg` como um pacote local:

```sh
pip install .
```

## 🛠 Uso

### ✅ Instalar um pacote
```sh
pipg install fastapi
```
Isso instalará o pacote `fastapi` e registrará a versão no `requirements.txt`.

### ❌ Desinstalar um pacote
```sh
pipg uninstall fastapi
```
Isso removerá o `fastapi` e o excluirá do `requirements.txt`.

## 🏗 Estrutura do Projeto
```
pipg/
│── pipg/
│   │── __init__.py
│   │── cli.py
│── setup.py
│── README.md
│── LICENSE
│── setup.cfg
│── pyproject.toml
```

## 🤝 Contribuição
1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para utilizá-lo e modificá-lo conforme necessário.

