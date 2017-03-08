from ga4gh.client import client
from ga4gh.server import datarepo, backend
import ConfigParser


class ClientManager:

    def __init__(self):
        self.client_list = []

    def __len__(self):
        return len(self.client_list)
        
    def add_http_client(self, http_client, datasets=None, featuresets=None, phenotypeassociationsets=None, **kwargs):
        """Add a g2p HTTP client to manager. Optionally restrict to specified datasets, featuresets, and phenotypeassociatonsets."""
        if isinstance(http_client, str):
            c = HttpClient(http_client, datasets, featuresets, phenotypeassociationsets, **kwargs)
        elif isinstance(http_client, HttpClient):
            c = http_client
        else:
            raise TypeError('Expected http_client to be URL base string or HttpClient object')
        self.client_list.append(c)

    def add_local_client(self, local_client="simulated", datasets=None, featuresets=None, phenotypeassociationsets=None, **kwargs):
        """Add a g2p local client to manager."""
        if isinstance(local_client, str) and local_client == 'simulated':
            repository = datarepo.SimulatedDataRepository()
            b = backend.Backend(repository)
            c = LocalClient(b, datasets, featuresets, phenotypeassociationsets, **kwargs)
        elif isinstance(local_client, LocalClient):
            c = local_client
        else:
            raise TypeError('Expected local_client to be "simulated" or LocalClient object')
        self.client_list.append(c)
        
    def load_clients_from_config(self, config_file):
        """Add g2p clients from a specified configparser-compliant config file."""
        pass
        
    def federated_featurephenotypeassociaton_query(self, args):
        """Search all clients for feature-phenotype associations as defined by args."""
        pass


class HttpClient(client.HttpClient):

    def __init__(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None, **kwargs):
        super(HttpClient, self).__init__(url_prefix, **kwargs)
        self.restricted_datasets = datasets or []
        self.restricted_featuresets = featuresets or []
        self.restricted_phenotypeassociationsets = phenotypeassociationsets or []


class LocalClient(client.LocalClient):

    def __init__(self, backend, datasets=None, featuresets=None, phenotypeassociationsets=None, **kwargs):
        super(LocalClient, self).__init__(backend, **kwargs)
        self.restricted_datasets = datasets or []
        self.restricted_featuresets = featuresets or []
        self.restricted_phenotypeassociationsets = phenotypeassociationsets or []