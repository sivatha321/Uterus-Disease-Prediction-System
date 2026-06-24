import joblib
import numpy as np

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

rf_model = joblib.load("random_forest_model.pkl")

feature_extractor = MobileNetV2(
weights='imagenet',
include_top=False,
pooling='avg'
)

CLASS_NAMES = {
0: "Adenomyosis",
1: "Endometrial Cancer",
2: "Fibroid",
3: "Normal Uterus"
}

def predict_rf(img_path):

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

    features = feature_extractor.predict(
        img_array,
        verbose=0
    )

    prediction = rf_model.predict(
        features
    )

    probabilities = rf_model.predict_proba(
        features
    )

    confidence_score = round(
        float(np.max(probabilities)) * 100,
        2
    )

    predicted_class = CLASS_NAMES[
        int(prediction[0])
    ]

    return predicted_class, confidence_score
