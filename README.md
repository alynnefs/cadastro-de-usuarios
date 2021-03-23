# web-users

Esse projeto consite em uma aplicação na web com cadastro de usuários. Os dados de cadastro estão na estrutura a seguir:
+ nome
+ email
+ endereço do usuário
  - País
  - Estado
  - Município
  - CEP
  - Rua
  - Número
  - Complemento
+ CPF
+ PIS
+ Senha

## Dependências Utilizadas
+ Linux 18.04
+ [Python 3.8.7](https://www.python.org/)
+ [PostgreSQL 13.2](https://www.postgresql.org/)
+ [jq](https://stedolan.github.io/jq/download/)
  - usado para filtrar o retorno do curl que é usado no script de população do banco de dados
+ [virtualenv](https://www.pythoncentral.io/how-to-install-virtualenv-python/)
  - usado para separar bibliotecas usadas caso execute o projeto diretamente
+ outras bibliotecas podem ser encontrada no arquivo [requirements.txt](https://github.com/alynnefs/web-users/blob/main/requirements.txt)


## Criação do ambiente e Execução

Na raiz do projeto:
+ Criar o ambiente virtual usando
```
virtualenv -p python3.8 .env
```
+ Ativar o ambiente virtual com
```
source .env/bin/activate
```
+ Instalar as dependências
```
pip install -r requirements.txt
```
+ No PostgreSQL deve haver dois bancos: web_user e test_web_user. Um para a aplicação e outro para testes, respectivamente. Esses bancos de dados não precisam ter tabelas, eles só precisam existir.

## Como popular o banco de dados

Para facilitar os testes iniciais, existe o arquivo [populate.sh](https://github.com/alynnefs/web-users/blob/main/backend/populate.sh). Caso ele não esteja com permissão de execução, basta executar

```chmod +x caminho/para/populate.sh```

Para executá-lo e, consequentemente, adicionar valores ao banco de dados, basta usar

```./caminho/para/populate.sh```

Este arquivo cria 2 usuários. O primeiro com 1 endereço e o segundo com 2.
