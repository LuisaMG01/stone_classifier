import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from preprocess import (
    preprocess_data,
    load_chemical_group_mapping,
    filter_classes,
    get_main_element,
)


def train_model(
    data_path="data/minerals/minerals.csv", model_path="model/crystal_model.pkl"
):
    df = pd.read_csv(data_path)
    chemical_group_map = load_chemical_group_mapping()

    element_columns = list(chemical_group_map.keys())

    df["Element"] = df[element_columns].apply(
        lambda row: get_main_element(row, element_columns), axis=1
    )

    df["Chemical Group"] = df["Element"].map(chemical_group_map)

    df = df[~df["Chemical Group"].isin(["Alkaline Earth Metal", "Transition Metal"])]

    group_counts = df["Chemical Group"].value_counts()
    rare_groups = group_counts[group_counts < 10].index
    df["Chemical Group"] = df["Chemical Group"].apply(
        lambda x: "Rare" if x in rare_groups else x
    )

    df_nonmetal = df[df["Chemical Group"] == "Nonmetal"].sample(n=300, random_state=42)
    df_rest = df[df["Chemical Group"] != "Nonmetal"]
    df = pd.concat([df_nonmetal, df_rest], ignore_index=True)

    df = filter_classes(df, target_col="Chemical Group", min_samples=10)

    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    min_class_size = y_train.value_counts().min()
    if min_class_size > 1:
        k_neighbors = min(5, min_class_size - 1)
        print(f"Using SMOTE with k_neighbors={k_neighbors}")
        smote = SMOTE(k_neighbors=k_neighbors, random_state=42)
        X_train, y_train = smote.fit_resample(X_train, y_train)
    else:
        print("One class has only 1 sample. SMOTE disabled.")

    model = RandomForestClassifier(class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, model_path)
    print(f"Model saved at {model_path}")

    return X_test, y_test, model
