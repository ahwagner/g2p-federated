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

    def add_local_client(self, local_client="simulated", datasets=None, featuresets=None, phenotypeassociationsets=None):
        """Add a g2p local client to manager."""
        if isinstance(local_client, str) and local_client == 'simulated':
            repository = datarepo.SimulatedDataRepository()
            b = backend.Backend(repository)
            c = LocalClient(b, datasets, featuresets, phenotypeassociationsets)
        elif isinstance(local_client, LocalClient):
            c = local_client
        else:
            raise TypeError('Expected local_client to be "simulated" or LocalClient object')
        self.client_list.append(c)
        
    def load_clients_from_config(self, config_file):
        """Add g2p clients from a specified configparser-compliant config file."""
        pass
        
    def federated_featurephenotypeassociaton_query(self, feature_kwargs={}, phenotype_kwargs={}):
        """Search all clients for feature-phenotype associations as defined by args."""
        if not self.client_list:
            raise RuntimeError('No client is added to the manager')
        federated_associations=[]
        for c in self.client_list:
            datasets = c.search_datasets()
            phenotype_association_set_ids = []
            for dataset in datasets:
                feature_ids = []
                phenotype_ids = []
                phenotype_association_sets = c.search_phenotype_association_sets(dataset_id=dataset.id)
                for phenotype_association_set in phenotype_association_sets:
                    phenotype_association_set_ids.append(phenotype_association_set.id)
                    if phenotype_kwargs:
                        phenotypes_generator = c.search_phenotype(phenotype_association_set_id=phenotype_association_set.id, **phenotype_kwargs)
                        for phenotype in phenotypes_generator:
                            phenotype_ids.append(phenotype.id)
                featuresets = c.search_feature_sets(dataset_id=dataset.id)
                for featureset in featuresets:
                    if feature_kwargs:
                        feature_generator = c.search_features(feature_set_id=featureset.id, **feature_kwargs)
                        for feature in feature_generator:
                            feature_ids.append(feature.id)
                for phenotype_association_set_id in phenotype_association_set_ids:  
                    feature_phenotype_associations = c.search_genotype_phenotype(phenotype_association_set_id = phenotype_association_set_id,
                                                                                 phenotype_ids=phenotype_ids, feature_ids=feature_ids)
                    for association in feature_phenotype_associations:
                        federated_associations.append(association)
        return federated_associations


class HttpClient(client.HttpClient):

    def __init__(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None, **kwargs):
        super(HttpClient, self).__init__(url_prefix, **kwargs)
        self.allowed_datasets = datasets or []
        self.allowed_featuresets = featuresets or []
        self.allowed_phenotypeassociationsets = phenotypeassociationsets or []

    def search_datasets(self):
        datasets = super(HttpClient, self).search_datasets()
        if self.allowed_datasets:
            datasets = [dataset for dataset in datasets if dataset.id in self.allowed_datasets]
        return datasets

    def search_phenotype_association_sets(self, dataset_id):
        pa_sets = super(HttpClient, self).search_phenotype_association_sets(dataset_id)
        if self.allowed_phenotypeassociationsets:
            pa_sets = [pa_set for pa_set in pa_sets if pa_set.id in self.allowed_phenotypeassociationsets]
        return pa_sets

    def search_feature_sets(self, dataset_id):
        f_sets = super(HttpClient, self).search_feature_sets(dataset_id)
        if self.allowed_featuresets:
            f_sets = [f_set for f_set in f_sets if f_set.id in self.allowed_featuresets]
        return f_sets


class LocalClient(client.LocalClient):

    def __init__(self, backend, datasets=None, featuresets=None, phenotypeassociationsets=None):
        super(LocalClient, self).__init__(backend)
        self.allowed_datasets = datasets or []
        self.allowed_featuresets = featuresets or []
        self.allowed_phenotypeassociationsets = phenotypeassociationsets or []

    def search_datasets(self):
        datasets = super(LocalClient, self).search_datasets()
        datasets = [dataset for dataset in datasets if dataset.name in self.allowed_datasets]
        return datasets

    def search_phenotype_association_sets(self, dataset_id):
        pa_sets = super(LocalClient, self).search_phenotype_association_sets(dataset_id)
        pa_sets = [pa_set for pa_set in pa_sets if pa_set.id in self.allowed_phenotypeassociationsets]
        return pa_sets

    def search_feature_sets(self, dataset_id):
        f_sets = super(LocalClient, self).search_feature_sets(dataset_id)
        f_sets = [f_set for f_set in f_sets if f_set.id in self.allowed_featuresets]
        return f_sets
