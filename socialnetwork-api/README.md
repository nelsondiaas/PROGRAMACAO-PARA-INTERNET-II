# Social Network - API

## Dependências
* Django
* django_extensions
* rest_framework
  
## Migrando os dados do arquivo db.json para o banco de dados
Para iniciar tudo do zero, exclua o arquivo ``db.sqlite3`` e realize o ``makemigrations`` & ``migrate``, logo em seguida poderá executar esse comando abaixo, para que o povoamento do banco sejá realizado. 
```
python manager.py runscript load_data
```