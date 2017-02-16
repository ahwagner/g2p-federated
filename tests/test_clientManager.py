import unittest

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from g2pf.clientManager import *


class TestClientManager(unittest.TestCase):
    
    def check_client_number_in_add_http_client(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None):
        clientManager = ClientManager("")
        clientNumber1=len(clientManager.clientList)
        clientManager.add_http_client(url_prefix, datasets, featuresets, phenotypeassociationsets)
        clientNumber2=len(clientManager.clientList)
        self.assertEqual(clientNumber1+1, clientNumber2)
        
        clientManager.add_http_client(url_prefix, datasets, featuresets, phenotypeassociationsets)
        clientNumber3=len(clientManager.clientList)
        self.assertEqual(clientNumber2+1, clientNumber3)
        
    def check_restrictions_in_add_http_client(self, url_prefix, datasets=None, featuresets=None, phenotypeassociationsets=None):
        clientManager = ClientManager("")
        clientManager.add_http_client(url_prefix, datasets, featuresets, phenotypeassociationsets)
        c=clientManager.clientList[0]
        if datasets is None:
            datasets=[]
        if featuresets is None:
            featuresets=[]
        if phenotypeassociationsets is None:
            phenotypeassociationsets=[]
        self.check_restrictions(clientManager, c, datasets, featuresets, phenotypeassociationsets)
        
    def check_restrictions(self, clientManager, client, datasets, featuresets, phenotypeassociationsets):
        self.assertEqual(len(clientManager.dictClientToRestrictedDatasets[client]),len(datasets))
        self.assertEqual(len(clientManager.dictClientToRestrictedFeaturesets[client]),len(featuresets))
        self.assertEqual(len(clientManager.dictClientToRestrictedPhenotypeassociationsets[client]),len(phenotypeassociationsets))
        
        
    def test_add_http_client_1(self):
        self.check_client_number_in_add_http_client("http://1kgenomes.ga4gh.org")
        
    def test_add_http_client_2(self):
        self.check_client_number_in_add_http_client("http://1kgenomes.ga4gh.org", datasets=["1kgenomes","anotherOne"], featuresets=["f1","f2"], phenotypeassociationsets=["p1","p2"])
        
    def test_restrictions_in_add_http_client_1(self):
        self.check_restrictions_in_add_http_client("http://1kgenomes.ga4gh.org")
        
    def test_restrictions_in_add_http_client_2(self):
        self.check_restrictions_in_add_http_client("http://1kgenomes.ga4gh.org", datasets=["1kgenomes","anotherOne"], featuresets=["f1","f2"], phenotypeassociationsets=["p1","p2"])
        
    def test_http_client_search_datasets(self):
        clientManager = ClientManager("")
        clientManager.add_http_client("http://1kgenomes.ga4gh.org")
        dataset = clientManager.clientList[0].search_datasets().next()
        self.assertIsNotNone(dataset)
        
    def test_restrict_client(self):
        clientManager = ClientManager("")
        clientManager.add_http_client("http://1kgenomes.ga4gh.org")
        c=clientManager.clientList[0]
        datasets=["d1","d2"]
        featuresets=["f1","f2","f3"]
        phenotypeassociationsets=["p1"]
        clientManager.restrict_client(c,datasets,featuresets,phenotypeassociationsets)
        self.check_restrictions(clientManager, c, datasets, featuresets, phenotypeassociationsets)
        featuresets=["f1"]
        phenotypeassociationsets=["p1","p2"]
        clientManager.restrict_client(c, featuresets=["f1"], phenotypeassociationsets=["p1","p2"])
        self.check_restrictions(clientManager, c, [], featuresets, phenotypeassociationsets)
        
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