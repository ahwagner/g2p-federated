from ga4gh.client import client
import configparser


class ClientManager:

    def __init__(self, args):
        pass

    def add_client(self, datasets=None, featuresets=None,
                   phenotypeassociationsets=None):
        """Add a g2p client to manager. Optionally restrict to specified
        datasets, featuresets, and phenotypeassociatonsets."""
        pass

    def load_clients_from_config(self, config_file):
        """Add g2p clients from a specified configparser-compliant config
        file."""
        pass

    def federated_featurephenotypeassociaton_query(self, args):
        """Search all clients for feature-phenotype associations as defined by
        args."""
        pass
