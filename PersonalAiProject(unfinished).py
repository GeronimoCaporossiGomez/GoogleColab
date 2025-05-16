# Importar librerías necesarias
import numpy as np
import pandas as pd
import os
import zipfile
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

# Rutas de los archivos ZIP
zip_files = [
    '/mitbih_train.csv.zip',
    '/mitbih_test.csv.zip',
    '/ptbdb_abnormal.csv.zip',
    '/ptbdb_normal.csv.zip'
]

# Carpeta para descomprimir
extract_path = '/content/'

# Descomprimir cada archivo ZIP
for zip_path in zip_files:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"Descomprimido: {zip_path}")

# Verificar los archivos descomprimidos
print("Archivos descomprimidos:", os.listdir(extract_path))

# Cargar los archivos CSV
mitbih_train = pd.read_csv('/content/mitbih_train.csv', header=None)
mitbih_test = pd.read_csv('/content/mitbih_test.csv', header=None)
ptbdb_normal = pd.read_csv('/content/ptbdb_normal.csv', header=None)
ptbdb_abnormal = pd.read_csv('/content/ptbdb_abnormal.csv', header=None)

# Mostrar información básica de los datasets
print("MITBIH Train Shape:", mitbih_train.shape)
print("MITBIH Test Shape:", mitbih_test.shape)
print("PTBDB Normal Shape:", ptbdb_normal.shape)
print("PTBDB Abnormal Shape:", ptbdb_abnormal.shape)

# Combinar los datasets PTBDB (normal y abnormal)
ptbdb_data = pd.concat([ptbdb_normal, ptbdb_abnormal])
print("PTBDB Combined Shape:", ptbdb_data.shape)

# Separar características (X) y etiquetas (y) para cada dataset
X_mitbih_train = mitbih_train.iloc[:, :-1].values
y_mitbih_train = mitbih_train.iloc[:, -1].values
X_mitbih_test = mitbih_test.iloc[:, :-1].values
y_mitbih_test = mitbih_test.iloc[:, -1].values

X_ptbdb = ptbdb_data.iloc[:, :-1].values
y_ptbdb = ptbdb_data.iloc[:, -1].values

# Normalizar los datos
X_mitbih_train = X_mitbih_train / 255.0
X_mitbih_test = X_mitbih_test / 255.0
X_ptbdb = X_ptbdb / 255.0

# Convertir las etiquetas PTBDB a categorías binarias
y_ptbdb = to_categorical(y_ptbdb, num_classes=2)

# Dividir PTBDB en datos de entrenamiento y prueba
X_ptbdb_train, X_ptbdb_test, y_ptbdb_train, y_ptbdb_test = train_test_split(
    X_ptbdb, y_ptbdb, test_size=0.2, random_state=42
)

# Crear el modelo CNN
model = Sequential()
model.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_mitbih_train.shape[1], 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.3))
model.add(Conv1D(64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(5, activation='softmax'))  # 5 clases para MITBIH

# Compilar el modelo
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Configurar un callback para detener el entrenamiento si no hay mejora
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Entrenar el modelo con MITBIH
X_mitbih_train = np.expand_dims(X_mitbih_train, axis=2)
X_mitbih_test = np.expand_dims(X_mitbih_test, axis=2)

history = model.fit(
    X_mitbih_train, y_mitbih_train,
    validation_data=(X_mitbih_test, y_mitbih_test),
    epochs=20,
    batch_size=64,
    callbacks=[early_stopping]
)

# Evaluar el modelo
loss, accuracy = model.evaluate(X_mitbih_test, y_mitbih_test)
print(f"Precisión en datos de prueba (MITBIH): {accuracy * 100:.2f}%")

# Mostrar gráfico de precisión por época para MITBIH
plt.plot(history.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(history.history['val_accuracy'], label='Precisión de validación')
plt.title('Precisión por época (MITBIH)')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

# Guardar el modelo entrenado
model.save('/content/mitbih_model.h5')
print("Modelo guardado exitosamente en '/content/mitbih_model.h5'")

# Descargar el modelo guardado
from google.colab import files
files.download('/content/mitbih_model.h5')

# Entrenar un modelo separado para PTBDB (opcional)
ptbdb_model = Sequential()
ptbdb_model.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_ptbdb_train.shape[1], 1)))
ptbdb_model.add(MaxPooling1D(pool_size=2))
ptbdb_model.add(Dropout(0.3))
ptbdb_model.add(Conv1D(64, kernel_size=3, activation='relu'))
ptbdb_model.add(MaxPooling1D(pool_size=2))
ptbdb_model.add(Dropout(0.3))
ptbdb_model.add(Flatten())
ptbdb_model.add(Dense(128, activation='relu'))
ptbdb_model.add(Dropout(0.3))
ptbdb_model.add(Dense(2, activation='softmax'))  # 2 clases para PTBDB

ptbdb_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

history_ptbdb = ptbdb_model.fit(
    np.expand_dims(X_ptbdb_train, axis=2), y_ptbdb_train,
    validation_data=(np.expand_dims(X_ptbdb_test, axis=2), y_ptbdb_test),
    epochs=20,
    batch_size=64,
    callbacks=[early_stopping]
)

# Evaluar el modelo
loss_ptbdb, accuracy_ptbdb = ptbdb_model.evaluate(np.expand_dims(X_ptbdb_test, axis=2), y_ptbdb_test)
print(f"Precisión en datos de prueba (PTBDB): {accuracy_ptbdb * 100:.2f}%")

# Mostrar gráfico de precisión por época para PTBDB
plt.plot(history_ptbdb.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(history_ptbdb.history['val_accuracy'], label='Precisión de validación')
plt.title('Precisión por época (PTBDB)')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

# Guardar el modelo PTBDB
ptbdb_model.save('/content/ptbdb_model.h5')
print("Modelo PTBDB guardado exitosamente en '/content/ptbdb_model.h5'")

files.download('/content/ptbdb_model.h5')
