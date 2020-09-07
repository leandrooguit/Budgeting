# Budgeting

O microservice Budgeting vai ser responsável por armazenar o orçamento (estimativa) inicial de um conjuntos de microservices em um determinada nuvem 
(AWS, Azure e Google Cloud).

IDE utilizada para executar o projeto 
- PyCharm Community Edition

Verificar a versão do Python
- python --version

A versão utilizada para desenvolver o projeto Budgeting em Python foi 3.7

Segue abaixo o comando utilizado para fixar a versão do Python na codificação
- alias python=python3.7

Comando para instalar o ambiente virtual no PyCharm Community Edition
- pip install virtualenv

Comando para criar o ambiente virtual e fixar a versão do Python 
- virtualenv ambvir --python=python3.7

Comando para acessar o ambiente virtual no linux
- source ambvir/bin/activate

Comando para verificar as bibliotecas instaladas no ambiente virtual
- pip freeze

Comando para desativar o ambiente virtual
- deactivate

Nesse projeto foi utilizado o Flask para desenvolver o Budgeting.
Comando para instalar o Flask
- pip install Flask

Comando para instalar a biblioteca que vai criar a API REST
- pip install Flask-Restful

Comando para instalar o sql-alchemy para geração do banco de dados relacional
- pip install Flask-SQLAlchemy

Comando para subir o servidor
- python app.py

Comando para instalar a lib JWT
- pip install Flask-JWT-Extended
