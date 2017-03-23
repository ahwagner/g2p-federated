import unittest

from g2pf.clientManager import *
from ga4gh.server import backend, datarepo
from ga4gh.client import client

b = backend.Backend(datarepo.SimulatedDataRepository())


class TestClientManager(unittest.TestCase):

    def setUp(self):
        self.http_client1 = HttpClient("http://1kgenomes.ga4gh.org")
        self.http_client2 = HttpClient("http://1kgenomes.ga4gh.org",
                                       datasets=["1kgenomes", "anotherOne"],
                                       featuresets=["f1", "f2"],
                                       phenotypeassociationsets=["p1", "p2"])
        self.local_client1 = LocalClient(b)
        self.local_client2 = LocalClient(b,
                                         datasets=['1kgenomes', 'anotherOne'],
                                         featuresets=['f1', 'f2'],
                                         phenotypeassociationsets=['p1', 'p2'])
        self.manager = ClientManager()

    def test_add_clients(self):
        counts = list()
        counts.append(len(self.manager))
        self.manager.add_http_client(self.http_client1)
        counts.append(len(self.manager))
        self.manager.add_http_client(self.http_client2)
        counts.append(len(self.manager))
        self.manager.add_local_client(self.local_client1)
        counts.append(len(self.manager))
        self.manager.add_local_client(self.local_client2)
        counts.append(len(self.manager))

        self.assertItemsEqual(counts, range(5))

    def test_add_clients_by_string(self):
        self.manager.add_http_client('http://1kgenomes.ga4gh.org')
        c = self.manager.client_list[-1]
        self.assertEqual(c._url_prefix, 'http://1kgenomes.ga4gh.org')
        self.manager.add_local_client()
        c = self.manager.client_list[-1]
        self.assertIsInstance(c, client.LocalClient)
        self.assertIsInstance(c._backend._dataRepository, datarepo.SimulatedDataRepository)

    def test_add_clients_type_error(self):
        with self.assertRaises(TypeError):
            self.manager.add_http_client(42)
        with self.assertRaises(TypeError):
            self.manager.add_local_client(None)

    def test_federated_featurephenotypeassociation_query_with_no_clients(self):
        with self.assertRaises(RuntimeError):
            feature_kwargs={'reference_name':"chr7",'start':55249005,'end':55249006}
            phenotype_kwargs={'description':"Adenosquamous carcinoma .*"}
            self.manager.federated_featurephenotypeassociaton_query(feature_kwargs,phenotype_kwargs)
            
    def test_federated_featurephenotypeassociation_query(self):
        self.manager.add_http_client('http://1kgenomes.ga4gh.org')
        #self.manager.add_local_client(datasets=["simulatedDataset0"])
        self.manager.add_local_client()
        
        #feature_kwargs={'reference_name':"GL000195.1", 'start': 149089, 'end': 149287}
        #feature_kwargs={'name':'EGFR S768I missense mutation'}
        feature_kwargs={'reference_name':"chr7",'start':55249005,'end':55249006}
        phenotype_kwargs={'description':"Adenosquamous carcinoma .*"}
        federated_associations_1=self.manager.federated_featurephenotypeassociaton_query(feature_kwargs,phenotype_kwargs)
        self.assertNotEqual(len(federated_associations_1),0)
        
        feature_kwargs={'reference_name':"chr7",'start':55249005,'end':55249006}
        phenotype_kwargs={}
        federated_associations_2=self.manager.federated_featurephenotypeassociaton_query(feature_kwargs,phenotype_kwargs)
        self.assertNotEqual(len(federated_associations_2),0)
        
        feature_kwargs={}
        phenotype_kwargs={'description':"Adenosquamous carcinoma .*"}
        federated_associations_3=self.manager.federated_featurephenotypeassociaton_query(feature_kwargs,phenotype_kwargs)
        self.assertNotEqual(len(federated_associations_3),0)
        
        self.assertTrue((len(federated_associations_2) >= len(federated_associations_1)) and 
                        (len(federated_associations_3) >= len(federated_associations_1)))
        


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


class TestLocalClient(unittest.TestCase):

    def setUp(self):
        self.local_client1 = LocalClient(b)
        self.local_client2 = LocalClient(b,
                                         datasets=['1kgenomes', 'anotherOne'],
                                         featuresets=['f1', 'f2'],
                                         phenotypeassociationsets=['p1', 'p2'])

    def test_restrictions(self):
        self.assertItemsEqual(self.local_client2.restricted_datasets, ['1kgenomes', 'anotherOne'])
        self.assertItemsEqual(self.local_client2.restricted_featuresets, ['f1', 'f2'])
        self.assertItemsEqual(self.local_client2.restricted_phenotypeassociationsets, ['p1', 'p2'])


def main():
    unittest.main()

if __name__ == '__main__':
    main()