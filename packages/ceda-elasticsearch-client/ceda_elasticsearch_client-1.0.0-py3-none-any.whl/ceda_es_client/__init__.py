
from elasticsearch import Elasticsearch
import os

CA_ROOT = os.path.join(os.path.dirname(__file__), 'root-ca.pem')
hosts = ['https://es%s.ceda.ac.uk:9200' % i for i in range(1,9)]

class CEDAElasticsearchClient(Elasticsearch):
    """
    Wrapper class to handle SSL authentication with the correct root
    certificate for the cluster. This subclass provides defaults for kwargs from
    the main Elasticsearch Python client.
    
    For read use cases, where the indices of interest are publically available, it will be sufficient to call:
    
    es = CEDAElasticsearchClient()
    
    For application access, which requires write permissions, you will need to provide an API key. This can be done:
    
    es =  CEDAElasticsearchClient(headers={'x-api-key':'YOUR-API-KEY'})
     or 
    es =  CEDAElasticsearchClient(api_key = 'YOUR-API-KEY')
    
    For further customisations see the Python Elasticsearch client documentation
    """

    def __init__(self, hosts=hosts, ca_certs=CA_ROOT, api_key=None, **kwargs):
 
        if api_key is not None: 
            if "headers" in kwargs: 
                kwargs["headers"]["x-api-key"] = api_key
            else:
                kwargs["headers"] = {'x-api-key': api_key}

        super(CEDAElasticsearchClient, self).__init__(
            hosts=hosts,
            ca_certs=ca_certs,
            **kwargs
        )
