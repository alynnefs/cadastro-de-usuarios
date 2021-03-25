# web-users

Esse projeto consiste em uma aplicação na web com cadastro de usuários. Os dados de cadastro estão na estrutura a seguir:
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
+ Algumas variáveis são declaradas no arquivo `local_settings.py`, que por motivos de segurança, está sendo ignorado pelo git. Ele é identico ao [local_settings.py](https://github.com/alynnefs/web-users/blob/main/backend/local_settings.example.py). É necessário apenas substituir a `SECRET_KEY`, colocando o resultado de `openssl rand -hex 32`.

## Como executar o projeto
Com o ambiente virtual ativo, execute:
```
uvicorn backend.main:app --reload
```
Você pode acessar as rotas descritas no [main.py](https://github.com/alynnefs/web-users/blob/main/backend/main.py) pela barra de buscas ou usar o [Interactive API docs](http://127.0.0.1:8000/docs#/)

## Como popular o banco de dados manualmente
Para inserir dados pelo [Interactive API docs](http://127.0.0.1:8000/docs#/), siga os seguintes passos:
- clicar em uma rota marcada como POST
- clicar em `Try it out`
- adicionar os campos desejados

Obs: e-mail, CPF e PIS estão sendo validados. Para o POST funcionar, é necessário adicionar um domínio de e-mail válido. Para [CPF](https://theonegenerator.com/generators/documents/cpf-generator/) e [PIS](https://www.geradorpis.com/), você pode usar os geradores marcados como link. Não importa se a entrada tem ou não os caracteres padrão, eles serão removidos. Caso um desses campos já exista, o POST não será feito.

## Como popular o banco de dados por script

Para facilitar os testes iniciais, existe o arquivo [populate.sh](https://github.com/alynnefs/web-users/blob/main/backend/populate.sh). Caso ele não esteja com permissão de execução, basta executar

```chmod +x caminho/para/populate.sh```

Para executá-lo e, consequentemente, adicionar valores ao banco de dados, basta usar

```./caminho/para/populate.sh```

Este arquivo cria 2 usuários. O primeiro com 1 endereço e o segundo com 2.
OBS: O backend deve estar rodando. 

## Como rodar os testes
- na raiz do projeto e com o ambiente virtual ativo, execute
```
pytest tests/tests.py
```
Obs: esses testes precisam ser melhor desenvolvidos e e necessário remover alguns hard codes.

## Dificuldades encontradas
- Quando o usuário está logado, um cookie é gerado. Entretanto ele se perde quando a página é atualizada. Não descobri a tempo como armazená-lo.
- Adicionei uma mensagem para quando um usuário faz login, mas ao meu ver isso deveria acontecer no front. Caso exista usuário mostra o nome, caso não, mostra "visitante".
- Até o momento não encontrei uma biblioteca de validação de CEP que funcione para todos os países.
- Os testes estão com id hard coded, por dificuldade em pegar o id do usuário.

## Próximos passos
Além de resolver os mencionados em "dificuldades encontradas":
- Colocar autorização nas rotas. O login existe e funciona, mas só está sendo usado na rota que pega o usuário atual (/users/me) e na rota que pega o token.
- Adicionar docstrings e gerar documentação através delas.
- Melhorar testes.
