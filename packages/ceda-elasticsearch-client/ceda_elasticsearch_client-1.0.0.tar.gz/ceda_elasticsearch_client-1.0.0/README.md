
# A CEDA elastic search client

Just a layer over the elasticsearch lib with the CEDA elastic search config baked in.

```
>>> from ceda_es_client import CEDAElasticsearchClient
>>> es = CEDAElasticsearchClient()
>>> es.search(index="fbi-2022", ...
```

If you need to add an API key 

```
>>> from ceda_es_client import CEDAElasticsearchClient
>>> es = CEDAElasticsearchClient(api_key=MYAPIKEY)
>>> es.index(index="myindex", id=10, document=...
```