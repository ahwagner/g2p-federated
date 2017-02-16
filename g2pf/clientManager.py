from ga4gh.client import client
import configparser


class ClientManager:

    def __init__(self, args):
        self.clientList=[]
        self.dictClientToRestrictedDatasets={}
        self.dictClientToRestrictedFeaturesets={}
        self.dictClientToRestrictedPhenotypeassociationsets={}
        
    def add_http_client(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p HTTP client to manager. Optionally restrict to specified datasets, featuresets, and phenotypeassociatonsets."""
        c = client.HttpClient(url_prefix)
        self.clientList.append(c)
        self.restrict_client(c,datasets, featuresets, phenotypeassociationsets)
        
    #HTTP and Local client methods are seperate because local client constructor can take more parameters although I'm not using currently. 
    def add_local_client(self,backend, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p local client to manager."""
        c = client.LocalClient(backend)
        self.clientList.append(c)
        self.restrict_client(c,datasets, featuresets, phenotypeassociationsets)
        
    def restrict_client(self, client, datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Restrict the client to specified datasets, featuresets, and phenotypeassociatonsets."""
        if datasets is None:
            self.dictClientToRestrictedDatasets[client]=[]
        else:
            self.dictClientToRestrictedDatasets[client]=datasets
        if featuresets is None:
            self.dictClientToRestrictedFeaturesets[client]=[]
        else:
            self.dictClientToRestrictedFeaturesets[client]=featuresets
        if phenotypeassociationsets is None:
            self.dictClientToRestrictedPhenotypeassociationsets[client]=[]
        else:
            self.dictClientToRestrictedPhenotypeassociationsets[client]=phenotypeassociationsets
        
    def load_clients_from_config(self, config_file):
        """Add g2p clients from a specified configparser-compliant config
        file."""
        pass
        
    def federated_featurephenotypeassociaton_query(self, args):
        """Search all clients for feature-phenotype associations as defined by
        args."""
        pass