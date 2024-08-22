<h1 align="center">LabAssist</h1>

<p>Este projeto visa desenvolver um sistema web para o gerenciamento eficiente do controle de
estoque de reagentes químicos, tanto ativos quanto passivos, além de fornecer ferramentas
para a gestão de laudos e relatórios de análises químicas e microbiológicas. O sistema será
projetado para o LAQUAM (Laboratório de Química Ambiental) do IFCE Campus Juazeiro
do Norte.</p>

<h3 align="center">Sumário</h3>

* [Links úteis](#links-úteis)

* [Tecnologias utilizadas](#tecnologias-utilizadas)

* [Instalação:](#instalação)
  * [Linux](#linux)
  * [Windows](#windows)

* [Guia do Projeto:](#guia-do-projeto)
  * [Apps](#apps)
  * [Pastas](#pastas)

# Links úteis:

* [Pasta no Drive](https://drive.google.com/drive/folders/1yNdqTN-Bp2tZvwYVXwnVFvTgU9JhXJ2h)

* [Design no Figma](https://www.figma.com/design/RvGgnZ638xNMSMfuQpRX2i/IFCE-LAQUAM?node-id=0-1&t=t5MnuxHTRbyjWUNy-1)

* [Painel no Jira](FALTA)

* [Repositório no Github](https://github.com/PedroLucasMoraisBorges/labAssist)

# Tecnologias utilizadas:

* [Django](https://docs.djangoproject.com/)

* [PostgreSQL](https://www.postgresql.org/) (Durante o desenvolvimento está sendo usado o SQLite)

# Instalação:

## Linux:

**OBS.:** Se você utiliza qualquer distro Linux, não será necessário a instalação do Python nem Git.

### 1. Repositório:

Clone o repositório através do comando:
```
git clone https://github.com/PedroLucasMoraisBorges/labAssist.git
```
OU você pode usar a extensão do VSCode para clonar.

### 2. VirtualEnv:

Esse passo não é obrigatório, mas extremamente recomendado, principalmente para organização. O VirtualEnv ajudará a separar os pacotes de vários projetos diferentes através da criação de ambientes virtuais isolados.

No terminal, digite:
```
sudo apt install virtualenv
```
Após a instalação, navegue até a diretório do projeito e crie um ambiente virtual através do comando:
```
virtualenv nome_da_venv
```
Sendo "nome_da_venv" o nome escolhido para seu ambiente virtual, pode ser qualquer um, mas recomenda-se que seja um nome fácil de lembrar e que seja relacionado ao projeto, normalmente é utilizado 'venv'.

Entre no ambiente virtual:
```
source nome_da_env/bin/activate
```
E para sair do ambiente virtual (mas isso não será necessário agora), use:
```
deactivate
```
**OBS.:** Todo pacote instalado (através do pip) enquanto o ambiente virtual estiver ativo, ficará instalado apenas dentro do ambiente.

### 3. Requerimentos:

No terminal, digite:
```
pip install -r requeriments.txt
```
Tenha certeza de estar dentro do diretório do projeto, ou você irá receber um erro. Se estiver usando o ambiente virtual, garanta que está com ele ativado.

### 4. Migrations:

Para realizar as migrações e preparar o Banco de Dados, use o seguinte comando no terminal:
```
python3 manage.py migrate
```
Mais uma vez, lembre de estar com a virtualenv ativa, e que instalou os pacotes do passo anterior corretamente.

As migrações são uma maneira de atualizar ou modificar a estrutura de um banco de dados em um projeto Django. Elas são criadas a partir de mudanças feitas nos modelos de dados do projeto, e servem para manter o banco de dados sincronizado com o código do projeto. Cada migração representa uma alteração específica no modelo de dados, e pode ser aplicada ou desfeita para atualizar ou retroceder a estrutura do banco de dados.

### 5. Iniciando o projeto:

Inicie o projeto utilizando:
```
python3 manage.py runserver
```
Sempre que quiser iniciar o projeto, basta utilizar esse comando, sempre garantindo que está com a venv ativa e na raíz do projeto. Não é necessário repetir todos os passos sempre. As migrações só serão necessárias caso o Django aponte (no terminal, quando você iniciar o projeto) que há migrações não aplicadas.

Boa sorte.

[Volte ao sumário](#sumário)

## Windows:

### 1. Repositório:

Para clonar o repositório, você precisará do Git instalado em sua máquina. Caso ainda não tenha instalado, você pode baixá-lo através do link: https://git-scm.com/downloads

Navegue até o diretório onde deseja clonar o repositório. Em seguida, execute o seguinte comando:
```
git clone https://github.com/PedroLucasMoraisBorges/labAssist.git
```
OU você pode usar a extensão do VSCode para clonar.

### 2. Python:

Baixe a versão mais recente do Python no site oficial: https://www.python.org/downloads/. Durante a instalação, certifique-se de marcar a opção "Add Python to PATH".

### 3. VirtualEnv:

Esse passo não é obrigatório, mas extremamente recomendado, principalmente para organização. O VirtualEnv ajudará a separar os pacotes de vários projetos diferentes através da criação de ambientes virtuais isolados.

Abra o prompt de comando do Windows e digite:

```
pip install virtualenv
```

Após a instalação, navegue até o diretório do projeto e crie um ambiente virtual através do comando:
```
python -m venv nome_da_venv
```
Sendo "nome_da_venv" o nome escolhido para seu ambiente virtual, pode ser qualquer um, mas recomenda-se que seja um nome fácil de lembrar e que seja relacionado ao projeto, normalmente é utilizado 'venv'.

Entre no ambiente virtual:
```
nome_da_env\Scripts\Activate.ps1
```

E para sair do ambiente virtual (mas isso não será necessário agora), use:
```
deactivate
```
**OBS.:** Todo pacote instalado (através do pip) enquanto o ambiente virtual estiver ativo, ficará instalado apenas dentro do ambiente.

### 4. Requerimentos:

No prompt de comando do Windows, digite:
```
pip install -r requeriments.txt
```
Tenha certeza de estar dentro do diretório do projeto, ou você irá receber um erro. Se estiver usando o ambiente virtual, garanta que está com ele ativado.

### 5. Migrations:

Para realizar as migrações e preparar o Banco de Dados, use o seguinte comando no prompt:
```
python manage.py migrate
```
Mais uma vez, lembre de estar com a virtualenv ativa, e que instalou os pacotes do passo anterior corretamente.

As migrações são uma maneira de atualizar ou modificar a estrutura de um banco de dados em um projeto Django. Elas são criadas a partir de mudanças feitas nos modelos de dados do projeto, e servem para manter o banco de dados sincronizado com o código do projeto. Cada migração representa uma alteração específica no modelo de dados, e pode ser aplicada ou desfeita para atualizar ou retroceder a estrutura do banco de dados.

### 6. Iniciando o projeto:

Inicie o projeto utilizando:
```
python manage.py runserver
```
Sempre que quiser iniciar o projeto, basta utilizar esse comando, sempre garantindo que está com a venv ativa e na raíz do projeto. Não é necessário repetir todos os passos sempre. As migrações só serão necessárias caso o Django aponte (no terminal, quando você iniciar o projeto) que há migrações não aplicadas.

Boa sorte.

[Volte ao sumário](#sumário)

# Guia do Projeto

## Apps:

Os aplicativos em um projeto Django são os componentes independentes que realizam tarefas específicas. Os aplicativos são úteis para dividir a lógica do projeto em partes menores e mais gerenciáveis, que podem ser facilmente testadas e mantidas separadamente.

### Auth_user:

O aplicativo auth_user é responsável por toda a parte de autenticação e gerenciamento de usuários. Aqui, você encontra todas as views e urls para login, cadastro e logout de usuários, além das models relacionadas ao usuário, perfil do aluno e informações de currículo de aluno.

### Pages:

O aplicativo pages é onde toda a parte principal da aplicação é tratada. Aqui é onde as informações sobre vagas e empresas são tratadas e gerenciadas. Esse aplicativo é responsável por todo o gerenciamento de páginas, como a página inicial, a página de vagas, a página de detalhes da empresa, entre outras. Também responsável pelas funções para candidatura em vagas, indicações e notificações.

## Pastas:

###  Assets:

A pasta "assets" é usada para armazenar alguns dos arquivos estáticos, como imagens, arquivos CSS e JavaScript, ou outros recursos necessários para a interface do usuário do projeto. No caso desse projeto, é usada somente para armezenar arquivos estáticos do painel de administração. A pasta 'admin' dentro da pasta 'assets' contém arquivos de estilo e imagens usados para personalizar a aparência do painel de administração do Django. Esses arquivos são usados para personalizar a aparência das páginas do Django Admin, permitindo que você altere o estilo dos botões, a cor do fundo, fontes, etc.

### Auth_user e Pages:

São os diretórios dos apps [auth_user](#auth_user) e [pages](#pages), para saber melhor sobre os arquivos, funções e classes atibuídos a esse app, acesse o [guia dos aplicativos](https://docs.google.com/document/d/1rZMDSGvpejIyQCigBzkQtkjEUPIzhqGbmsZNT_XQZ5c/edit?usp=sharing). Uma breve descrição sobre os arquivos e pastas desses diretórios:

* migrations: esta pasta é usada para armazenar as migrações do aplicativo. As migrações são arquivos Python que descrevem como os modelos do aplicativo devem ser alterados. Elas são criadas automaticamente sempre que um modelo é alterado usando o comando makemigrations.

* models: esta pasta contém os arquivos Python que definem os modelos de dados do aplicativo. Esses modelos são usados para criar tabelas no banco de dados e mapear as relações entre elas.

* views: esta pasta contém as funções de visualização do aplicativo. As funções de visualização são responsáveis por receber as solicitações do usuário, processá-las e devolver uma resposta.

* forms: esta pasta contém os arquivos Python que definem os formulários do aplicativo. Os formulários são usados para coletar dados do usuário e validá-los antes de serem salvos no banco de dados.

* admin: esta pasta contém os arquivos Python que definem a interface administrativa do aplicativo. A interface administrativa é uma maneira fácil de gerenciar os dados do aplicativo diretamente pelo navegador.

* tests: esta pasta contém os arquivos Python que definem os testes do aplicativo. Os testes são usados para garantir que o aplicativo esteja funcionando corretamente e que novas alterações não causem regressões.

### Core:

A pasta Core é o diretório principal onde todos os arquivos e pastas do projeto Django são armazenados. Ela é nomeada assim por ser a pasta central.

* O arquivo "settings.py", que é responsável por definir as configurações do projeto, como por exemplo, as informações do banco de dados, configurações de segurança, configurações de cache, etc.

* O arquivo "urls.py", que é responsável por definir as rotas do projeto, ou seja, as URLs que serão utilizadas para acessar as diferentes funcionalidades do sistema.

### Media:

Essa pasta não irá aparecer até que se faça o upload de algum arquivo nos formulários do projeto. Essa pasta é responsável por armazenar os arquivos submetidos pelos usuários; porém, essa pasta será presente somente no momento de desenvolvimento, já que não é uma solução escalável para se armazenar esses arquivos quando o projeto estiver em Produção.

### Static:

Essa é a pasta responsável por armazenar os arquivos estáticos do projeto, como arquivos CSS, JavaScript e imagens, independente de qual aplicativo eles serão usados.

### Templates:

Essa é a pasta responsável por armazenar os arquivos HTML do projeto, independente de qual aplicativo esse template será usado.
