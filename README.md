# Facebook Scraper

[![Build Status](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper.svg?branch=master)](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d78fb4221b49847ca9c/maintainability)](https://codeclimate.com/github/unb-cic-esw/facebook-page-post-scraper/maintainability)

[:brazil: Readme](./README.md) | [:us: Readme](./.github/Readme/Language/English/README.md)

[:brazil: Documentação](./.github/Docs/Portuguese/Doc.md) |
[:us: Documentation](./.github/Docs/English/Doc.md)

## Tabela de Conteudo

* [Inicio](#facebook-scraper)
* [Tabela de Conteudo](#tabela-de-conteudo)
* [Fazendo tudo rodar](#fazendo-tudo-rodar)
* [Usando o Programa](#usando-o-programa)
* [Rodando os testes](#rodando-os-testes)
* [Verificando estilo](#verificando-estilo)
* [Heroku](#heroku)
* [Banco de dados Heroku](#banco-de-dados-heroku)
* [APScheduled](#apscheduled)
* [Agendamento](#agendamento)
* [BuildPacks](#buildpacks)
* [Projeto de](#um-projeto-de)
* [Showcases](#showcases)

## Fazendo tudo rodar

Uma vez que se tenha instalado python 3 e Git, baixado o repositório e
esteja com um editor de texto adequado (Atom, VSCode, Sublime ou Pycharm), deve-se
seguir os seguintes passos:

Criar o ambiente virtual (venv) e entrar no mesmo

```
python3 -m venv venv
source venv/bin/activate
```

Para aqueles no Linux ou Mac

```
make install
```

Para windows

```
pip install -r requirements.txt
```

Uma vez instalados todos os módulos, é necessário configurar o token.
Para isso devemos baixar o ChromeDriver, seguindo as instruções do Splinter de acordo
com seu sistema operacional: ([Instruções para baixar ChromeDriver](https://splinter.readthedocs.io/en/latest/drivers/chrome.html)).

Uma vez com o ChromeDriver instalado corretamente, é necessário setar uma variável de ambiente da 
seguinte forma: utilizando um editor de texto, vá em venv/bin/activate e, logo abaixo de deactivate()
coloque o seguinte comando:

``` 
unset GOOGLE_CHROME_SHIM
```

E, na última linha do arquivo escreva:  
 
```
export GOOGLE_CHROME_SHIM=$HOME/bin/chromedriver
```

Agora, para coletar um token, basta utilizar o comando:
```
make autotoken
```

## Usando o Programa

Uma vez com todas as configurações feitas, use:

```
make run
```

## Rodando os testes

Por enquanto rodar testes é a principal funcionalidade. Em breve serão adicionadas
mais funções. Portanto, para testes

```
make
```

E para saber qual a cobertura dos testes, use

```
make cov
```

## Verificando estilo

Para verificar se o seu código encontra-se bem indentado e bonito, use
o seguinte comando

```
make style
```

Importante usar este comando antes de mandar uma PR para garantir código mais legível.

## Heroku

O Heroku é uma das mais populares de plataforma como serviço que suporta
aplicações escritas em diversas linguagens, dentre elas, Python, java, node, etc.

Primeiro precisa criar uma conta.

requirements.txt - especifica todas as dependencias que a aplicação
precisa para rodar dentro do Heroku.

Procfile - especifica os comandos que serão executados pela aplicação
dentro da máquina Dynos. Nossa aplicação é um serviço de coleta de
dados que será todos dias da semana em um horário especifico.
Formato do arquivo:
clock: python heroku_clock.py

runtime.txt - especifica a versão do python que é suportada pela aplicação.
python-3.6.5

Link Heroku - ([facebook-page-post-scraper](https://dashboard.heroku.com/apps/facebook-page-post-scraper)).

Clone do repositorio:
heroku git:clone -a facebook-page-post-scraper

Adicionar um remote:

```
heroku login
git remote add heroku https://git.heroku.com/facebook-page-post-scraper.git
git pull heroku master
```

Link Heroku - Git ([Deploying with Git](https://devcenter.heroku.com/articles/git)).

Link Heroku - Agendamento ([Scheduled (Agendamento)](https://devcenter.heroku.com/articles/scheduled-jobs-custom-clock-processes)).

## Banco de dados Heroku

Utilizamos o banco de dados Heroku Postgres que funciona como um add-on instalado
 dentro do heroku.

Para a criação da tabela no banco de dados foi necessário instalar o psql na máquina.
Depois disso é necessário utilizar o comando abaixo para se conectar com o banco:

```
psql -h "Host" -U "User" "Database"
```

As aspas representam as credenciais do banco que podem ser encontradas ao entrar
 no Heroku Postgres, ir em 'Settings' e depois 'View Credentials'.

Agora que estamos conectados no banco de dados podemos executar vários comandos
 como criar tabelas, fazer select em tabelas existentes, excluir tabelas, inserir
 e excluir dados, entre outros.
Para a criação da tabela é necessário utilizar o comando:

```
CREATE TABLE Nome_da_tabela(nome_do_campo tipo_do_campo, ...);
```

A tabela criada deve ser a utilizada no comando executado na função calldb, portanto,
ela deve conter o campos que são utilizados para inserir dados na tabela.

## API Rest

Para exportação dos dados pela web utilizamos uma API Rest e um dyno web no 
 heroku. A API Rest foi implementada em server/rest.py, que disponibiliza os 
 dados em formato JSON de acordo com os endpoints especificados.
Para visualizar os endpoints, basta acessar a página inicial:
```
https://<nome-do-app>.herokuapp.com/
```
Também é possível rodar localmente, utilizando o Flask, basta usar:
```
python3 server/rest.py
```
Para se informar mais sobre [O que é uma API Rest](https://github.com/unb-cic-esw/Desenvolvendo-Software/wiki/O-que-%C3%A9-uma-API-REST-e-como-implementar-uma%3F).

## APScheduled

É uma biblioteca em python que permite realizar agendamento de tarefas (jobs). ([APScheduled](http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html)).

## Agendamento

Para automatizar a coleta de dados periodicamente, utilizamos
um modelo do heroku de agendamento chamado clock.
O programa será executado todos os dias à oito horas da manhã.
python heroku_clock.py

## BuildPacks

Os buildpacks são responsáveis por transformar o código implantado
no Heroku, que pode ser executado em um dyno.
Os buildpacks são compostos por um conjunto de scripts e,
dependendo da linguagem de programação.
Para adicionar um BuildPack segue os passos:
Settings -> Add buildpack

Segue aqui o [link do BuildPack](https://github.com/jontewks/puppeteer-heroku-buildpack)
da dependência (chromium-browser) projeto necessita

## Um projeto de

[![alt text][unb]](https://www.unb.br/)

[unb]:./.github/Images/logo_unb.png

Universidade de Brasília

[![alt text][resocie]](https://www.resocie.org/)

[resocie]:./.github/Images/resocie.jpg

Resocie : Repensando as Relações entre Sociedade e Estado

O projeto consiste na coleta sistêmica de informações quantitativas da
plataforma Facebook das páginas cadastradas no arquivo de entidades.csv
com o objetivo de subsidiar a análise comportamental política dos candidatos
durante o período eletorial brasileiro 2018.
Além do objetivo principal da coleta sistêmica das informações, o projeto
tem também por intuito servir de aprendizado de trabalho em time, de
tecnologias utilizadas e integração social entre os alunos da disciplina
Engenharia de Software do Departamento de Ciência da Computação da UnB
do 1º semestre de 2018.

## Showcases

[Apresentação interna pdf](./Resocie.pdf)
[Link da apresentação interna no canva](https://www.canva.com/design/DAC7AQM8vco/85lnoZTb57_TbLWPpDPeEQ/view?utm_content=DAC7AQM8vco&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton)
