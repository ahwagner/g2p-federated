from ga4gh.client import client
import configparser


class ClientManager:

    def __init__(self, args):
        self.clientList=[]
        self.restriction_mapping_datasets={}
        self.restriction_mapping_featuresets={}
        self.restriction_mapping_phenotypeassociationsets={}
        
    def add_client(self, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p client to manager. Optionally restrict to specified
        datasets, featuresets, and phenotypeassociatonsets."""
        pass
    
    def add_http_client(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p HTTP client to manager. Optionally restrict to specified datasets, featuresets, and phenotypeassociatonsets."""
        c = client.HttpClient(url_prefix)
        self.clientList.append(c)
        self.restrictClient(c,datasets, featuresets, phenotypeassociationsets)
        
        
    #HTTP and Local client methods are seperate because local client constructor can take more parameters although I'm not using currently. 
    def add_local_client(self,backend, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p local client to manager."""
        c = client.LocalClient(backend)
        self.clientList.append(c)
        self.restrictClient(c,datasets, featuresets, phenotypeassociationsets)
        
        
    def restrictClient(self, client, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Restrict the client to specified datasets, featuresets, and phenotypeassociatonsets."""
        if datasets is not None:
            self.restriction_mapping_datasets[client]=datasets
        if featuresets is not None:
            self.restriction_mapping_featuresets[client]=featuresets
        if phenotypeassociationsets is not None:
            self.restriction_mapping_phenotypeassociationsets[client]=phenotypeassociationsets
        
    def load_clients_from_config(self, config_file):
        """Add g2p clients from a specified configparser-compliant config
        file."""
        pass

    def federated_featurephenotypeassociaton_query(self, args):
        """Search all clients for feature-phenotype associations as defined by
        args."""
        pass


#Code for trial
clientManager = ClientManager("")
clientManager.add_http_client("http://1kgenomes.ga4gh.org", datasets=["1kgenomes","anotherOne"])
dataset = clientManager.clientList[0].search_datasets().next()
print dataset
print clientManager.restriction_mapping_datasets
print clientManager.restriction_mapping_featuresets
print clientManager.restriction_mapping_phenotypeassociationsets