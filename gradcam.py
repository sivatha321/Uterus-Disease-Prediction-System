import tensorflow as tf
import numpy as np
import cv2
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model("uterus_model.h5")

LAST_CONV_LAYER = "out_relu"


def generate_gradcam(img_path):

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = img_array / 255.0

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [
            model.get_layer(LAST_CONV_LAYER).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(
            img_array
        )

        class_idx = tf.argmax(
            predictions[0]
        )

        loss = predictions[:, class_idx]

    grads = tape.gradient(
        loss,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(
        heatmap
    )

    heatmap = heatmap.numpy()

    heatmap = np.maximum(
        heatmap,
        0
    )

    heatmap = heatmap / np.max(heatmap)

    original_img = cv2.imread(
        img_path
    )

    heatmap = cv2.resize(
    heatmap,
    (
        original_img.shape[1],
        original_img.shape[0]
    )
)

    heatmap = np.uint8(
        255 * heatmap
    )

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    superimposed_img = cv2.addWeighted(
        original_img,
        0.6,
        heatmap,
        0.4,
        0
    )

    filename = os.path.basename(
        img_path
    )

    gradcam_dir = os.path.join(
        "media",
        "gradcam"
    )

    os.makedirs(
        gradcam_dir,
        exist_ok=True
    )

    save_path = os.path.join(
        gradcam_dir,
        f"gradcam_{filename}"
    )

    cv2.imwrite(
        save_path,
        superimposed_img
    )

    return save_path.replace(
        "media\\",
        ""
    ).replace(
        "media/",
        ""
    )