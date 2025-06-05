"""Rotinas de modelagem inferencial."""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def treinar_logistica(df: pd.DataFrame, variaveis: list[str], alvo: str = "condenacao") -> LogisticRegression:
    """Treina uma regressão logística simples."""

    X = df[variaveis]
    y = df[alvo]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    previsoes = modelo.predict(X_test)
    relatorio = classification_report(y_test, previsoes)
    print(relatorio)

    return modelo
