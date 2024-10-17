from utils import bprint

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy 
import scipy.spatial.distance as ssd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer

import os
def getfeat(df, isbin = False):
    potential_binary = (df.nunique() == 2)
    binary_cols = df.loc[:, potential_binary].isin([0,1]).all().index.tolist()

    if isbin:
        return binary_cols
    return list(set(df.columns.tolist()).difference(set(binary_cols)))

def dendro_cluster_cutoff(X: pd.DataFrame, Y:pd.Series, min_clusters:int = 5 , max_num_clusters:int = 5, verbose = 0, plot_savepath = None):
    if verbose:
        bprint("debug")
        bprint("X type:", type(X))
        bprint("Y type:", type(Y))
    df_processed = pd.concat([Y.reset_index(drop = True), df_processed.reset_index(rop= True)], axis = 1).set_index(df_processed.index)

    full_corr_matrix = pd.DataFrame(
        np.corrcoef(df_processed.to_numpy().T),
        columns = df_processed.columns,
        index = df_processed.columns
    )

    feature_corr = full_corr_matrix.iloc[1:, 1:]
    feature_trgt_corr = full_corr_matrix.iloc[0,1:]

    # TODO: line 66+