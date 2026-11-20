# Clasificador Forward — Random Forest

Prototipo académico. No debe usarse para diagnóstico ni recomendaciones médicas.

## Archivos

- `app.py`: interfaz original adaptada al clasificador Random Forest.
- `modelo_5genes.pkl`: Random Forest entrenado, con MinMaxScaler integrado.
- `genes_5.json`: nombres y orden de los cinco genes Forward.
- `requirements.txt`: bibliotecas necesarias.
- `verificacion_modelo.json`: resultados de la comprobación contra las 22 muestras originales.

## Ejecutar en Windows

Desde la carpeta de la aplicación:

```bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Datos requeridos

Ingresar los valores de expresión de `SOSTDC1`, `SPP1`, `WIF1`, `SCGB1A1` y `FABP4`, con la misma plataforma y tratamiento de normalización compatibles con los archivos Forward de entrenamiento. Los valores no son datos clínicos generales; son expresión génica procesada.

## Reconstrucción

El modelo se reconstruyó con las 88 muestras suministradas, usando `MinMaxScaler` y `RandomForestClassifier` (`n_estimators=500`, `max_depth=3`, `criterion=gini`, `min_samples_leaf=1`, `min_samples_split=2`, `class_weight=balanced`, `random_state=42`).

Sobre las 22 muestras de prueba: 20 aciertos, 2 errores, exactitud de 0.9091, AUC de 0.9896. El modelo clasifica erróneamente las muestras `GSM1062806` y `GSM1062810`, igual que el cuaderno de Colab entregado.

La barra y sus colores se conservaron como representación visual de la puntuación, sin interpretación de riesgo o prioridad clínica.
