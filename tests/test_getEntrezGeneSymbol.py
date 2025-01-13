import unittest
from app.dataloader import getEntrezGeneSymbol  

class TestgetEntrezGeneSymbol(unittest.TestCase):

    def test_getEntrezGeneSymbol_geneid(self):
        # Test geneID = 1415 correspond to GeneSymbol =CRYBB2
        self.assertEqual(getEntrezGeneSymbol('EntrezGeneID','1415'), 'CRYBB2')

        # Test that GeneSymbol gives back the same GeneSymbol
        self.assertEqual(getEntrezGeneSymbol('EntrezGeneSymbol','GUCA1A'), 'GUCA1A')

        # Test with targetFullName
        self.assertEqual(getEntrezGeneSymbol('TargetFullName','Beclin-1'), 'BECN1')

        


   
