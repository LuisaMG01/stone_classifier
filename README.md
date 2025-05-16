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


# Clasificador de Rocas con Red Neuronal Convolucional (CNN)

##  Objetivo del Proyecto

El objetivo de este proyecto es clasificar imágenes de rocas en tres tipos principales de estructuras geológicas: **Igneous**, **Metamorphic** y **Sedimentary**, utilizando una red neuronal convolucional (CNN). Este modelo puede ser útil para aplicaciones educativas, geológicas o mineras, facilitando la identificación automática de muestras a partir de fotografías.

---

##  Intuición del Modelo

Las rocas tienen **patrones visuales** particulares dependiendo de su origen geológico. Por ejemplo:

* Las **ígneas** tienden a mostrar estructuras cristalinas.
* Las **metamórficas** tienen bandas foliares por presión y calor.
* Las **sedimentarias** presentan capas visibles y textura granular.

Una **CNN** es ideal para capturar estas diferencias gracias a su capacidad de:

* Extraer **características espaciales** jerárquicas.
* Detectar **bordes, formas y texturas** relevantes en las imágenes.

---

## Arquitectura y Entrenamiento

### Modelo Usado

Se utilizó una red **ResNet18** modificada (transfer learning), cargando pesos preentrenados de ImageNet y ajustando la capa final para 3 clases.

```python
model = RockResNet(num_classes=3)
```

### Preprocesamiento

* Redimensionado a 256x256
* Recorte central a 224x224
* Conversión a tensores normalizados

### Entrenamiento

```bash
python main.py
```

* **Optimizer:** Adam
* **Learning rate:** 0.001
* **Epochs:** 20
* **Batch size:** 32
* **Pérdida:** CrossEntropyLoss

Se aplica un `WeightedRandomSampler` para tratar el **desbalance de clases** durante el entrenamiento.

### Guardado del modelo

El modelo se guarda con metadatos (clases y arquitectura) en:

```bash
model/rock_cnn_full.pth
```

---

##  Predicción de Nuevas Imágenes

Puedes predecir la clase de una nueva imagen usando:

```bash
python predict.py imagen.jpg
```

El script usa la ruta al modelo entrenado y devuelve:

* Clase predicha
* Probabilidades por clase

---

##  Métricas de Rendimiento

| Clase       | Precision | Recall | F1-Score | Support |
| ----------- | --------- | ------ | -------- | ------- |
| Igneous     | 0.58      | 0.66   | 0.61     | 29      |
| Metamorphic | 0.86      | 0.81   | 0.83     | 121     |
| Sedimentary | 0.85      | 0.86   | 0.86     | 162     |

* **Accuracy total:** 82%
* **Macro F1-score:** 0.77 (media uniforme por clase)
* **Weighted F1-score:** 0.83 (ajustado al número de muestras)

### Interpretación:

* El modelo se desempeña bien en clases balanceadas (**Metamorphic**, **Sedimentary**).
* **Igneous** tiene menor performance, posiblemente por menor número de ejemplos (sólo 29).
* El uso de **data augmentation** o recolección de más datos ígneos podría mejorar el rendimiento.

---

##  Extensiones Futuras

* Usar otras arquitecturas como EfficientNet.
* Aumentar el dataset con técnicas de data augmentation.
* Crear una interfaz web o app para subir imágenes y obtener predicciones.

---

##  Estructura del Proyecto

```
rock_classifier/
├── data/rocks/train, val, test
├── model/
│   └── rock_cnn_full.pth
├── src/
│   ├── main.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── model.py
│   └── utils.py
```

---

##  Requisitos

* Python >= 3.8
* torch, torchvision
* scikit-learn
* PIL
* numpy

Instalar con:

```bash
pip install -r requirements.txt
```

---


