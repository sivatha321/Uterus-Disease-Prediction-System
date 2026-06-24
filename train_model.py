from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam

# ==========================
# DATA PREPARATION
# ==========================

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    'datasets',
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_data = val_datagen.flow_from_directory(
    'datasets',
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='validation'
)

print("Class Mapping:")
print(train_data.class_indices)

# ==========================
# MODEL CREATION
# ==========================

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)

x = Dense(
    128,
    activation='relu'
)(x)

x = Dropout(0.5)(x)

output = Dense(
    4,
    activation='softmax'
)(x)

model = Model(
    inputs=base_model.input,
    outputs=output
)

# ==========================
# COMPILE MODEL
# ==========================

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================
# CALLBACKS
# ==========================

checkpoint = ModelCheckpoint(
    'best_model.keras',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# ==========================
# TRAIN MODEL
# ==========================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=30,
    callbacks=[
        checkpoint,
        early_stop
    ]
)

# ==========================
# SAVE MODEL
# ==========================

model.save('uterus_model.h5')

print("\nTraining Completed Successfully!")
print("Model Saved as uterus_model.h5")