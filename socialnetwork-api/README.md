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