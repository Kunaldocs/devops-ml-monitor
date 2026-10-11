from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_model(random_state: int = 42):
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=random_state,
        stratify=data.target
    )
    model = RandomForestClassifier(n_estimators=50, random_state=random_state)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, {"n_estimators": 50, "random_state": random_state}, {"accuracy": float(accuracy)}
