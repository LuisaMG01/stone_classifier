import pandas as pd
import json

def load_chemical_group_mapping(json_path="data/minerals/chemical_groups.json"):
    with open(json_path, 'r') as f:
        return json.load(f)

def get_main_element(row, element_columns):
    max_value = -1
    main_element = None
    for col in element_columns:
        if row[col] > max_value:
            max_value = row[col]
            main_element = col
    return main_element

def filter_classes(df, target_col='Chemical Group', min_samples=10):

    df = df[~df['Chemical Group'].isin(['Alkaline Earth Metal', 'Transition Metal'])]

    print(df['Chemical Group'].value_counts())


    counts = df[target_col].value_counts()
    keep_classes = counts[counts >= min_samples].index
    filtered_df = df[df[target_col].isin(keep_classes)].copy()
    return filtered_df

def preprocess_data(df, json_path="data/minerals/chemical_groups.json"):

    chemical_group_map = load_chemical_group_mapping(json_path)
    element_columns = list(chemical_group_map.keys())

    df['Element'] = df[element_columns].apply(lambda row: get_main_element(row, element_columns), axis=1)

    df['Chemical Group'] = df['Element'].map(chemical_group_map)

    feature_columns = df.select_dtypes(include=['number']).columns.difference(['count'])
    X = df[feature_columns]
    y = df['Chemical Group']

    return X, y
