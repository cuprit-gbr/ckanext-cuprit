from ckanext.dcat.profiles import RDFProfile
from rdflib import Namespace, Literal, URIRef
from rdflib.namespace import RDF, DCTERMS
from ckanext.dcat.utils import dataset_uri

MYVOCAB = Namespace("http://dainst.org/ns/dcat#")

class DAIDCATProfile(RDFProfile):
    '''
    A custom DCAT profile that adds a DOI field to the dataset.
    '''

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        '''
        Adds the DOI to the RDF graph generated from a CKAN dataset dict.
        '''
        # First, call the super method to ensure all base graphing happens
        super(DAIDCATProfile, self).graph_from_dataset(dataset_dict, dataset_ref)


        self.g.bind("dai-custom", MYVOCAB)

        # Then, add your custom graphing logic
        doi = dataset_dict.get('doi')
        if doi:
            self.g.add((dataset_ref, MYVOCAB.doi, Literal(doi)))

