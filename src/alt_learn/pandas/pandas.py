import pandas as pd
from sklearn.preprocessing import _BaseEncoder

pd.Data

class OneHotEncoder(_BaseEncoder):
    def fit(self,X:pd.DataFrame, y:pd.DataFrame = None):
        return pd.get_dummies(X, drop_first = True)
    

class DateFieldExtractor(Object):
    def fit(self, X:pd.DataFrame, y:pd.DataFrame = None):
        pass