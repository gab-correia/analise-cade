# semantic_pipeline.py
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from feature_engine.encoding import RareLabelEncoder
from sentence_transformers import SentenceTransformer
from scipy.cluster.hierarchy import linkage, cut_tree

# Classe SemanticBinner ajustada
class SemanticBinner(BaseEstimator, TransformerMixin):
    def __init__(self, embedding_model, n_clusters):
        self.embedding_model = embedding_model
        self.n_clusters = n_clusters
        self.column_name = None
        
    def fit(self, X, y=None):
        self.column_name = X.columns[0]
        self.embeddings_ = self.embedding_model.encode(X[self.column_name])
        self.linkage_ = linkage(self.embeddings_, 'ward')
        return self
    
    def transform(self, X):
        clusters = cut_tree(self.linkage_, n_clusters=self.n_clusters).flatten()
        return pd.Series(clusters, index=X.index, name='cluster')

def create_pipeline(n):
    return Pipeline([
        ('rare_labels', RareLabelEncoder(tol=0.02, variables=['setor_economico'])),
        ('semantic_clustering', SemanticBinner(
            SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2'),
            n_clusters=n
        ))
    ])
