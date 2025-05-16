import pandas as pd
import joblib
from src.minerals.preprocess import preprocess_data, load_chemical_group_mapping


def predict(
    input_data,
    model_path="model/crystal_model.pkl",
    reference_data_path="data/minerals/minerals.csv",
):

    model = joblib.load(model_path)

    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
    elif isinstance(input_data, list):
        input_data = pd.DataFrame(input_data)
    elif not isinstance(input_data, pd.DataFrame):
        raise ValueError("input_data debe ser un dict, lista de dicts o un DataFrame.")

    chemical_map = load_chemical_group_mapping()
    input_data["Chemical Group"] = input_data["Element"].map(chemical_map)

    input_data = pd.get_dummies(input_data, columns=["Chemical Group"], drop_first=True)

    reference_df = pd.read_csv(reference_data_path)
    X_train, _ = preprocess_data(reference_df)
    expected_cols = X_train.columns

    missing_cols = set(expected_cols) - set(input_data.columns)
    missing_df = pd.DataFrame(0, index=input_data.index, columns=list(missing_cols))
    input_data = pd.concat([input_data, missing_df], axis=1)[expected_cols]

    input_data = input_data[expected_cols]

    return model.predict(input_data)


def get_model_prediction_probas(
    input_data,
    model_path="model/crystal_model.pkl",
    reference_data_path="data/minerals/minerals.csv",
):
    """
    Obtiene las probabilidades de predicción para cada clase posible.
    
    Args:
        input_data: Datos de entrada (dict, lista de dicts o DataFrame)
        model_path: Ruta al modelo guardado
        reference_data_path: Ruta a los datos de referencia
        
    Returns:
        Diccionario donde las claves son los nombres de las clases y los valores son
        las probabilidades para cada clase.
    """
    model = joblib.load(model_path)
    
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
    elif isinstance(input_data, list):
        input_data = pd.DataFrame(input_data)
    elif not isinstance(input_data, pd.DataFrame):
        raise ValueError("input_data debe ser un dict, lista de dicts o un DataFrame.")
    
    chemical_map = load_chemical_group_mapping()
    input_data["Chemical Group"] = input_data["Element"].map(chemical_map)
    
    input_data = pd.get_dummies(input_data, columns=["Chemical Group"], drop_first=True)
    
    reference_df = pd.read_csv(reference_data_path)
    X_train, _ = preprocess_data(reference_df)
    expected_cols = X_train.columns
    
    missing_cols = set(expected_cols) - set(input_data.columns)
    missing_df = pd.DataFrame(0, index=input_data.index, columns=list(missing_cols))
    input_data = pd.concat([input_data, missing_df], axis=1)[expected_cols]
    
    input_data = input_data[expected_cols]
    
    probabilities = model.predict_proba(input_data)[0]
    
    classes = model.classes_
    
    proba_dict = {}
    for i, cls in enumerate(classes):
        proba_dict[str(cls)] = float(probabilities[i])
    
    return proba_dict
