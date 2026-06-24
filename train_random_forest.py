import os
import numpy as np

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import joblib

# Dataset path
DATASET_PATH = r"datasets"

# MobileNetV2 feature extractor
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    pooling='avg'
)

X = []
y = []

class_names = sorted(os.listdir(DATASET_PATH))

for label, folder_name in enumerate(class_names):

    folder_path = os.path.join(
        DATASET_PATH,
        folder_name
    )

    print(f"Processing {folder_name}")

    for file in os.listdir(folder_path):

        img_path = os.path.join(
            folder_path,
            file
        )

        try:

            img = image.load_img(
                img_path,
                target_size=(224,224)
            )

            img_array = image.img_to_array(img)

            img_array = np.expand_dims(
                img_array,
                axis=0
            )

            img_array = preprocess_input(
                img_array
            )

            features = base_model.predict(
                img_array,
                verbose=0
            )

            X.append(features.flatten())

            y.append(label)

        except:
            pass

X = np.array(X)
y = np.array(y)

print("Features Shape:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf_model.fit(
    X_train,
    y_train
)

y_pred = rf_model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nAccuracy:", accuracy)

print(
    classification_report(
        y_test,
        y_pred
    )
)

joblib.dump(
    rf_model,
    "random_forest_model.pkl"
)

print(
    "\nModel saved as random_forest_model.pkl"
)