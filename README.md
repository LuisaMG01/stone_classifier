# Crystal Structure Classifier

Este proyecto implementa un modelo de **clasificación de estructuras cristalinas** de minerales usando **propiedades físico-químicas** y la información del **grupo químico principal** de cada compuesto. Está desarrollado con Python, usando scikit-learn, pandas y SMOTE para manejo del desbalance.

---

## Objetivo

El objetivo es predecir la **estructura cristalina** (representada por el grupo químico principal del elemento dominante) de un mineral en base a su composición. Esta predicción puede asistir en investigaciones mineralógicas, cristalográficas o en minería de datos geológicos.

---

## Intuición del Modelo

Cada mineral contiene una mezcla de elementos. Sin embargo, usualmente hay un **elemento dominante** cuya presencia puede influir fuertemente en la forma en que se organiza la red cristalina. Asociando ese elemento a su **grupo químico** (como "Halógeno", "Metal alcalino", "No metal", etc.), el modelo aprende patrones entre la composición y la estructura cristalina.

### ¿Por qué Random Forest?

*  **Maneja bien features categóricos y numéricos**
*  **Robusto frente a outliers**
*  **Ideal para datos desbalanceados** (combinado con SMOTE)
*  **Interpretabilidad** a través de la importancia de atributos

---

##  Cómo funciona

1. **Preprocesamiento**:

   * Se calcula el **elemento dominante** de cada muestra.
   * Se mapea a su **grupo químico**.
   * Se eliminan o agrupan grupos minoritarios (con <10 muestras).
   * Se aplican técnicas de balanceo como **SMOTE** para sintetizar datos de clases minoritarias.

2. **Entrenamiento**:

   * Se entrena un `RandomForestClassifier` con `class_weight='balanced'`.

3. **Evaluación**:

   * Se mide el rendimiento con accuracy, balanced accuracy, matriz de confusión, y F1-score.

---

## Parámetros del modelo

| Parámetro      | Valor                     | Descripción                                     |
| -------------- | ------------------------- | ----------------------------------------------- |
| Modelo         | `RandomForestClassifier`  | Bosque aleatorio de árboles de decisión         |
| `class_weight` | `'balanced'`              | Penaliza errores en clases minoritarias         |
| `random_state` | `42`                      | Para reproducibilidad                           |
| SMOTE          | `k_neighbors = min(5, N)` | Sintetiza muestras si la clase tiene >1 muestra |

---

## Cómo entrenarlo

```bash
# Ejecuta el archivo principal para entrenar
python src/minerals/main.py
```

El script entrenará el modelo, aplicará balanceo con SMOTE, guardará el modelo en `model/crystal_model.pkl` y mostrará métricas de evaluación.

---

## Métricas de rendimiento

A continuación se muestran resultados obtenidos con un conjunto de test (96 muestras):

* **Accuracy**: `86.46%` – proporción total de predicciones correctas.
* **Balanced Accuracy**: `63.60%` – promedio del recall por clase (mejor indicador en clases desbalanceadas).
* **F1 Score (macro)**: `0.69` – promedio del F1-score de cada clase sin pesar por frecuencia.
* **F1 Score (weighted)**: `0.85` – F1-score ponderado por número de muestras por clase.

### Matriz de confusión (resumen)

| Clase        | Precision | Recall | F1-score | Soporte |
| ------------ | --------- | ------ | -------- | ------- |
| Alkali Metal | 1.00      | 0.33   | 0.50     | 3       |
| Anion        | 0.50      | 0.25   | 0.33     | 4       |
| Halogen      | 0.89      | 0.94   | 0.91     | 17      |
| Metalloid    | 1.00      | 0.50   | 0.67     | 2       |
| Noble Gas    | 1.00      | 1.00   | 1.00     | 1       |
| Nonmetal     | 0.88      | 0.98   | 0.93     | 60      |
| Other        | 0.67      | 0.44   | 0.53     | 9       |

>  Se observa que el modelo predice muy bien los **no metales** y **halógenos**, mientras que sigue teniendo dificultades con clases minoritarias como **aniones** o **metaloides**, lo cual es común debido al bajo soporte. El uso de SMOTE y la agrupación en clases "Rare" ayuda a mitigar esto.

---

##  Estructura del proyecto

```
stone_classifier/
├── data/
│   └── minerals/minerals.csv
├── model/
│   └── crystal_model.pkl
├── src/
│   └── minerals/
│       ├── main.py         # Entrenamiento y evaluación
│       ├── train.py        # Lógica de entrenamiento
│       ├── evaluate.py     # Métricas y visualización
│       ├── preprocess.py   # Preprocesamiento de datos
│       └── predict.py      # Predicciones en nuevos datos
```

---

##  Requisitos

* Python 3.9+
* pandas
* scikit-learn
* imbalanced-learn
* joblib

Instalación:

```bash
pip install -r requirements.txt
```

---

