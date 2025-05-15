from train import train_model
from evaluate import evaluate_model
from predict import predict
from utils.roc import plot_roc_pr_curves

if __name__ == "__main__":
    print("Training the model...")
    X_test, y_test, model = train_model()

    print("\nEvaluating the model...")
    evaluate_model(model, X_test, y_test)

    print("\nPrediction example:")
    sample = {
        "Element": "Silicon",
        "Specific Gravity": 2.33,
        "Calculated Density": 2.33,
        "Refractive Index": 3.42,
        "Mohs Hardness": 7,
        "Optical": 1
    }
    pred = predict(sample)
    print("Predicted crystal structure:", pred[0])

    class_names = sorted(y_test.unique())

    plot_roc_pr_curves(model, X_test, y_test, class_names)
