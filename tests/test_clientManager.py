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