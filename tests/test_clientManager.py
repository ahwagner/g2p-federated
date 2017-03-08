import unittest

from g2pf.clientManager import *

class TestClientManager(unittest.TestCase):

    def setUp(self):
        self.http_client1 = HttpClient("http://1kgenomes.ga4gh.org")
        self.http_client2 = HttpClient("http://1kgenomes.ga4gh.org",
                                       datasets=["1kgenomes", "anotherOne"],
                                       featuresets=["f1", "f2"],
                                       phenotypeassociationsets=["p1", "p2"])
        self.manager = ClientManager()
        
    def check_restrictions_in_add_http_client(self, http_client, datasets=None, featuresets=None, phenotypeassociationsets=None):
        client_manager = ClientManager()
        client_manager.add_http_client(http_client, datasets, featuresets, phenotypeassociationsets)
        c = client_manager.clientList[0]
        self.check_restrictions(client_manager, c, datasets, featuresets, phenotypeassociationsets)
        
    def check_restrictions(self, client_manager, client, datasets, featuresets, phenotypeassociationsets):
        self.assertEqual(len(client_manager.dictClientToRestrictedDatasets[client]), len(datasets))
        self.assertEqual(len(client_manager.dictClientToRestrictedFeaturesets[client]), len(featuresets))
        self.assertEqual(len(client_manager.dictClientToRestrictedPhenotypeassociationsets[client]), len(phenotypeassociationsets))

    def test_add_http_clients(self):
        client_init_lenth = len(self.manager)
        self.manager.add_http_client(self.http_client1)
        client_number1 = len(self.manager)
        self.manager.add_http_client(self.http_client2)
        client_number2 = len(self.manager)
        self.assertEqual(client_init_lenth + 1, client_number1)
        self.assertEqual(client_number1 + 1, client_number2)


class TestHttpClient(unittest.TestCase):

    def setUp(self):
        self.http_client1 = HttpClient("http://1kgenomes.ga4gh.org")
        self.http_client2 = HttpClient("http://1kgenomes.ga4gh.org",
                                       datasets=["1kgenomes", "anotherOne"],
                                       featuresets=["f1", "f2"],
                                       phenotypeassociationsets=["p1", "p2"])

    def test_http_client_search_datasets(self):
        dataset = self.http_client1.search_datasets().next()
        self.assertIsNotNone(dataset)

    def test_restrictions(self):
        self.assertItemsEqual(self.http_client2.restricted_datasets, ['1kgenomes', 'anotherOne'])
        self.assertItemsEqual(self.http_client2.restricted_featuresets, ['f1', 'f2'])
        self.assertItemsEqual(self.http_client2.restricted_phenotypeassociationsets, ['p1', 'p2'])

    def test_add_local_client(self):
        self.fail()

    def test_load_clients_from_config(self):
        self.fail()

    def test_federated_featurephenotypeassociaton_query(self):
        self.fail()


def main():
    unittest.main()

if __name__ == '__main__':
    main()