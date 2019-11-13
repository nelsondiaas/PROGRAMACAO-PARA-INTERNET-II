# Social Network - API

## Dependências
* Django
* django_extensions
* rest_framework

## Install dependências
```
$ pip install -r requirements.txt
```

## Migrando os dados do arquivo db.json para o banco de dados
Para iniciar, primeiro você deve realizar o ``migrate`` no projeto, logo em seguida poderá executar o script ``load_data``, para que o povoamento do banco sejá realizado. 

```
$ python manager.py migrate
```

```
$ python manager.py runscript load_data
```

## Iniciando tests
Para iniciar os testes, temos que comentar alguns dados no projeto, o motivo é que o ``THROTTLE`` irá bloquear nossas requisições de token. Então temos que comentar no arquivo ``socialnetwork/views.py`` na class ``CustomAuthToken`` comente esses dados ``throttle_scope='api-token'`` , ``throttle_classes=[ScopedRateThrottle]``, também temos que comentar em outro local no arquivo ``config/settings.py`` você procura pelo nome ``DEFAULT_THROTTLE_RATES`` e comenta todo ele, finalizando isso poderá iniciar os proximos procedimentos dos tests.

Agora temos que executar um comando, para que possamos criar um ``.json`` dos nossos dados em banco. O porque disso? teremos que fazer testes com esses dados povoado em um arquivo de teste ``.sqlite3`` que o proprio django ira criar e povoar esse novo banco com nossos dados em ``.json``. Logo em seguida podera executar os tests.

```
$ python manager.py dumpdata -o my_db_test.json --exclude=contenttypes
```
```
$ python manager.py test
```
