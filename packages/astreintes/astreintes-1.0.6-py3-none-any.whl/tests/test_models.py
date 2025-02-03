import unittest
from astreintes import models


class TestModeles(unittest.TestCase):
    def test_params(self):
        params = models.Parametres(seed=1234)
        self.assertTrue(params.max_astreintes == 13)

    def test_sites(self):
        import pandas as pd

        df_sites = models.Sites(
            pd.DataFrame(dict(nom=['Bourges', 'Tours'], aga=[0, 5], respi=[8, 8], rotations=[1, 2])),
        )
        self.assertTrue(df_sites.shape == (2, 4))
