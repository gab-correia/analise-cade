"""Inferential modeling utilities."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def train_logistic_regression(df: pd.DataFrame, features: list[str], target: str = 'condenacao') -> LogisticRegression:
    """Train a simple logistic regression model."""
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    report = classification_report(y_test, preds)
    print(report)

    return model
