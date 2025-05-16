from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    balanced_accuracy_score,
    f1_score,
)
from sklearn.metrics import classification_report


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Balanced Accuracy:", balanced_accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print(
        "\nClassification Report:\n",
        classification_report(y_test, y_pred, zero_division=0),
    )
    print("F1 Score (macro):", f1_score(y_test, y_pred, average="macro"))
    print("F1 Score (weighted):", f1_score(y_test, y_pred, average="weighted"))


class_names = [
    "Alkali Metal",
    "Alkaline Earth Metal",
    "Anion",
    "Halogen",
    "Metalloid",
    "Noble Gas",
    "Nonmetal",
    "Other",
    "Transition Metal",
]
