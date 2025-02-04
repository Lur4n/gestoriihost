# Tutorial de configurações do GetoriiHost 
### Configurando o AMBIENTE

#### Downloads e instalações necessárias:
- Anaconda Pyhton
- VSCode
- PostgreSQL 16+
- DataBase Client(Pluggin de gerenciamento de BD - extensão)
- Git
<div style="display: inline_block;">
    <img src="https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white">
    <img style="width: 28px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/2048px-Visual_Studio_Code_1.35_icon.svg.png">
    <img style="width: 28px;" src="https://www.postgresql.org/media/img/about/press/elephant.png">
    <img style="width: 150px;" src="https://database-client.com/text_logo.png">
    <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white">
</div>
    
### Preparando o ambiente (Terminal)
- No terminal digite:
```
conda env list
conda create -n gestoriihost python=3.11.9
conda activate gestoriihost
pip install Django==4.1
pip install psycopg2
pip install psycopg2-binary
```
### Preparando o Ambiente (IDE)
-	Abrir um terminal no VSCode e digite:
```
conda activate gestoriihost
```
-	CTRL+SHIFT+P: Selecionar o interpretador python correspondente ao ambiente virtual chamado gestoriihost
### Preparando a aplicação Django
-	Navegar via terminal (cd) até a pasta onde você irá criar o projeto Django, use:
```
django-admin startproject gestoriihost
```
-	Abra a pasta criada pelo Django no VSCode
-	Renomeie a pasta *gestoriihost/gestoriihost* para *gestoriihost/config*
-	Acesse o arquivo manage.py na raiz e altere a linha onde está *gestoriihost.settings* para *config.settings*.
-	Acesse o arquivo *wsgi.py* em config e altere *gestoriihost.settings*. para *config.settings*.
-	Crie no app config um arquivo chamado *middleware.py* e adicione o seguinte código:
```
#classe para desabilitar cache e evitar problemas com dados armazenados pelo navegador

class NoCacheMiddleware:
    def __init__(self, get_response):

    self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
```

-	Crie na raiz da aplicação uma pasta chamada resources.
-	Dentro de resources crie uma pasta chamada static.
-	Dentro de static crie 3 pastas: css, img e js.
-	 Acesse o arquivo settings.py dentro de config e:
-	Altere *WSGI_APPLICATION = "gestoriihost.wsgi.application"* para *config.wsgi.application*
-	Importe os seguintes pacotes no cabeçalho:
import os
from django.contrib.messages import constants as messages
-	Em MIDDLEWARE adicione: 
'config.middleware.NoCacheMiddleware',
-	Altere ROOT_URLCONF = "gestoriihost.urls" para config.urls.
-	Adicione a seção abaixo após ROOT_URLCONF:
```
#integra com o sistema de auth padrao do Django

#AUTH_USER_MODEL = 'cadastros.Usuario'

AUTHENTICATION_BACKENDS = [
    #'cadastros.backends.EmailBackend',  #backend de autenticacao personalizado
    'django.contrib.auth.backends.ModelBackend',  #backend de autenticacao padrao
]
```

-	Em TEMPLATES altere a linha DIRS para: 
"DIRS": [os.path.join(BASE_DIR, "resources")], #define o caminho da pasta que tera os recursos usados pelos templates
-	Após a sessão TEMPLATES adicione essa nova seção:
#URL de redirecionamento apos login
LOGIN_REDIRECT_URL = 'core:main'
LOGOUT_REDIRECT_URL = 'autenticacao:login'
LOGIN_URL = 'autenticacao:login'
-	Altere DATABASES para:
DATABASES = {
	'default': {
    	'ENGINE': 'django.db.backends.postgresql',
    	'NAME': 'db_pypel',
    	'USER': 'postgres',
    	'PASSWORD': 'root',
    	'HOST': 'localhost',
    	'PORT': '5432',
	}
}


-	Adicione após DATABASES:
```
#Settings for messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

-	Altere LANGUAGE_CODE e TIME_ZONE para:
LANGUAGE_CODE = "pt-BR"
TIME_ZONE = "America/Sao_Paulo"
 
-	Altere a seção Static files para:
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resources/static/"),
]
```
-	Crie as duas variáveis globais no final do arquivo com:
```
#Configurações de variáveis globais
NUMBER_GRID_PAGES = 20
NUMBER_GRID_MODAL = 20
```
### Criando os **APPS** Django
Vamos criar os apps responsáveis por autenticar, guardar os códigos reutilizáveis e o que armazenará os cadastros do sistema. Para isso execute:
```
python manage.py startapp core
python manage.py startapp autenticacao
python manage.py startapp cadastros
```
-	Em settings.py dentro do app config adicione os apps dentro de INSTALLED_APPS para ficar da seguinte forma:
```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
	"autenticacao",
	"core",
	"cadastros",
] 
```
### Criando o **MODELO** de usuário do sistema
> 🐒olhar com o ciniro como a gente pode criar nossas tabelas com base nos nosso projeto de hotelaria, a gente já tem um der ai meio que no pente, dá pra expressar bastante ideia pra ele, acho que ele da um help pa nois
-	Insira o seguinte o código dentro de models.py no app cadastros

``` 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import ProtectedError
class Departamento(models.Model):
    nome = models.CharField(max_length=500)
    sigla = models.CharField(max_length=30)
   
    def delete(self, *args, **kwargs):
    	if self.usuario_set.exists():
        	raise ProtectedError(
            	"Não é possível excluir este departamento, pois ele possui usuarios vinculados.",
            	self
        	)
    	super().delete(*args, **kwargs)
    	
    def __str__(self):
    	return self.nome
 
class Perfil(models.Model):
    nome = models.CharField(max_length=100, unique=True)
 
    def delete(self, *args, **kwargs):
    	if self.usuario_set.exists():
        	raise ProtectedError(
            	"Não é possível excluir este perfil, pois ele possui usuarios vinculados.",
            	self
        	)
    	super().delete(*args, **kwargs)
    	
    def __str__(self):
    	return self.nome
   
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
    	if not email:
        	raise ValueError('O usuário deve ter um endereço de e-mail')
    	user = self.model(email=self.normalize_email(email), nome=nome)
    	user.set_password(password)
    	user.save(using=self._db)
    	return user
 
    def create_superuser(self, email, nome, password=None):
    	user = self.create_user(email, nome, password)
    	user.is_admin = True
    	user.save(using=self._db)
    	return user
 
class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    perfis = models.ManyToManyField(Perfil)
 
    objects = UsuarioManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
 
    def __str__(self):
    	return self.email
 
    def has_perm(self, perm, obj=None):
    	return True
 
    def has_module_perms(self, app_label):
    	return True
 
    @property
    def is_staff(self):
    	return self.is_admin
 
	def tem_perfil(self, perfil_nome):
    	return self.perfis.filter(nome=perfil_nome).exists()
 
```
### Criando o **BANCO DE DADOS**
-	Verifique se o psql está acessível via terminal como uma variável de ambiente. Isso depende de como está configurado o seu sistema operacional. Se não for o caso, identifique como fazer isso e adicione a variável PATH ao ambiente.
-	Acesse o psql via terminal com:
```
sudo -u postgres psql
```
-	Digite a senha do seu usuário sudo
-	Acesse o PostgreSQL
-	Digite a senha root do usuário postgres
-	Crie o banco:
```
CREATE DATABASE bd_gestoriihost;
```
-	Conceda privilégios no banco:
```
GRANT ALL PRIVILEGES ON DATABASE bd_gestoriihost TO postgres;
```
-	Cheque a criação do banco:
```
\l
```
-	Saia do psql
```
\q
```
### Acessando **BANCO DE DADOS** pela extensão do *VSCode*
-	Entre no DB Client e crie uma conexão com o banco de dados preenchendo os campos com os dados condizentes com a string de conexão com o banco de dados.
-	Visualize o banco.

### Gerando o **BANCO DE DADOS** com base no MODELO
-	No terminal digite: 
```
python manage.py makemigrations
python manage.py migrate
```

-	Abra o DB Client e cheque se as tabelas foram criadas corretamente.

-	Descomente em *settings.py* no diretório config os modelos de autenticação de usuário:

```
#integra com o sistema de auth padrao do Django
AUTH_USER_MODEL = 'cadastros.Usuario'
AUTHENTICATION_BACKENDS = [
	'cadastros.backends.EmailBackend',  #backend de autenticacao personalizado
	'django.contrib.auth.backends.ModelBackend',  #backend de autenticacao padrao
]
```
### Testando a aplicação
```
python manage.py runserver
```
-	Se tiver feito tudo certo verá o foguetinho do Django!



