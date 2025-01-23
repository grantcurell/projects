# Aircraft Detection

- [Aircraft Detection](#aircraft-detection)
  - [How the Code Works](#how-the-code-works)
    - [Dataset](#dataset)
    - [Key Points](#key-points)
    - [`prepare_data` Function](#prepare_data-function)
      - [Explanation:](#explanation)
    - [`split_data` Function](#split_data-function)
      - [Explanation:](#explanation-1)
    - [`create_generators` Function](#create_generators-function)
      - [Explanation:](#explanation-2)
    - [`build_model` Function](#build_model-function)
      - [Explanation:](#explanation-3)
    - [`train_model` Function](#train_model-function)
      - [Explanation:](#explanation-4)
    - [6. Main Script](#6-main-script)
  - [How the Math Works](#how-the-math-works)
    - [EfficientNetB3 as the Base Model](#efficientnetb3-as-the-base-model)
      - [Input Shape](#input-shape)
      - [Convolution Operation](#convolution-operation)
      - [Activation Function (ReLU)](#activation-function-relu)
      - [Strided Convolutions (Downsampling)](#strided-convolutions-downsampling)
    - [Global Max Pooling](#global-max-pooling)
    - [Fully Connected Layers](#fully-connected-layers)
      - [Batch Normalization](#batch-normalization)
      - [Dense Layer (256 Units)](#dense-layer-256-units)
      - [Dropout](#dropout)
      - [Dense Layer with Softmax (Output Layer)](#dense-layer-with-softmax-output-layer)
    - [Compilation](#compilation)
      - [Categorical Cross-Entropy Loss](#categorical-cross-entropy-loss)
      - [Adamax Optimizer](#adamax-optimizer)
    - [Understanding Kernels (Filters) in Convolution](#understanding-kernels-filters-in-convolution)
      - [Kernel Shape](#kernel-shape)
      - [Convolution Operation](#convolution-operation-1)
      - [Sliding the Kernel Across the Image](#sliding-the-kernel-across-the-image)
    - [Example: $3 \\times 3$ Kernel on a Grayscale Image](#example-3-times-3-kernel-on-a-grayscale-image)
      - [Input Image](#input-image)
      - [Kernel](#kernel)
      - [Receptive Field at $(1, 1)$](#receptive-field-at-1-1)
      - [Element-wise Multiplication and Summation](#element-wise-multiplication-and-summation)
    - [Output Dimensions](#output-dimensions)
    - [ReLU Activation Function and Non-Linearity](#relu-activation-function-and-non-linearity)
    - [Step-by-Step Explanation](#step-by-step-explanation)
    - [Why ReLU is Preferred Over Other Activations](#why-relu-is-preferred-over-other-activations)
    - [Example of ReLU in Action](#example-of-relu-in-action)
    - [Impact of ReLU on Feature Maps](#impact-of-relu-on-feature-maps)
    - [Global Max Pooling: Reducing a 3D Tensor to a 1D Vector](#global-max-pooling-reducing-a-3d-tensor-to-a-1d-vector)
    - [The Math of Global Max Pooling](#the-math-of-global-max-pooling)
      - [Step-by-Step Explanation of Global Max Pooling](#step-by-step-explanation-of-global-max-pooling)
      - [Why Use Global Max Pooling?](#why-use-global-max-pooling)
      - [Example](#example)
      - [Impact of Global Max Pooling](#impact-of-global-max-pooling)

## Code

- Training program is [main.py](./main.py)
- To test a trained model I used [f16_test_model.py](./f16_test_model.py)

## Test Results Against F16s

This isn't the most robust of tests, but I pulled a few dozen F16 images and ran a test against them using [f16_test_model.py](./f16_test_model.py). These images varied pretty widely and I picked the F16 on purpose because the conformal fuel tanks make it a bit harder to recognize. The pictures were all different sizes, different angles, different weather, etc so I made it pretty difficult. The model still did ok in that despite a lot of noise it got 3/4 correct. Here is what I noticed tripped it up:

1. Multiple different aircraft in the same picture (this one makes sense and would be hard to train out without using a different model)
2. Shock condensation was present
3. The color scheme was significantly different. Ex: some of the images had a desert paint scheme and it missed all of those

| Image Name                                             | Predicted | Confidence | Correct |
|--------------------------------------------------------|-----------|------------|---------|
| -1x-1.webp                                             | F16       | 0.99       | Yes     |
| 05frontirusukr2903202405-696x374.png                   | F16       | 1.00       | Yes     |
| 0x0 (1).webp                                           | F16       | 1.00       | Yes     |
| 0x0 (2).webp                                           | F16       | 1.00       | Yes     |
| 0x0 (3).webp                                           | F16       | 0.97       | Yes     |
| 0x0.webp                                               | B1        | 0.56       | No      |
| 1000w_q95 (1).webp                                     | F16       | 0.83       | Yes     |
| 1000w_q95.webp                                         | Su34      | 0.93       | No      |
| 1200x675_336905.webp                                   | F16       | 1.00       | Yes     |
| 63d560d4c00db.jpeg                                     | F16       | 1.00       | Yes     |
| 646752a44e3fe1148c5cacea.webp                          | F16       | 1.00       | Yes     |
| 64c7a25a4e3fe0112c582728.webp                          | F16       | 1.00       | Yes     |
| 6762-01.webp                                           | F16       | 1.00       | Yes     |
| 160824-F-QJ658-404-scaled.webp                         | F16       | 0.84       | Yes     |
| 1685548869503.jpeg                                     | Tornado   | 0.43       | No      |
| 1720619878283.webp                                     | Y20       | 0.54       | No      |
| 9eea165897293b9d3cff2d36736d.webp                      | F16       | 0.96       | Yes     |
| 2376e84a-b65c-4bb4-8884-59f70b84c4f1_16x9_1200x676.webp| F35       | 1.00       | No      |
| 240709-F-XO977-1093-900x600.jpeg                       | F16       | 0.97       | Yes     |
| 5633.webp                                              | F16       | 1.00       | Yes     |
| 6e588e65af644a5933ab301f075f2cdc.webp                  | F16       | 0.36       | Yes     |
| belgian-air-force-f-16b.webp                           | F16       | 1.00       | Yes     |
| do-you-think-that-the-f-16-will-still-be-in-service-past-v0-8rwx3k9176jc1.webp | F16 | 1.00 | Yes |
| F-16-AIM-missile.webp                                  | F16       | 1.00       | Yes     |
| f16-preparing-for-flight.webp                          | U2        | 0.78       | No      |
| f16s-turkey-1.webp                                     | U2        | 0.81       | No      |
| GUJWOKLWkAAnCOn.jpeg                                   | Tu160     | 0.98       | No      |
| IMG_7849web.webp                                       | F16       | 1.00       | Yes     |
| TopAces_F16_5.webp                                     | F16       | 1.00       | Yes     |
| 400_0_1651495143-4194.webp                             | F16       | 1.00       | Yes     |
| 41_2024-638559731785460659-546.jpeg                    | JAS39     | 1.00       | No      |
| 240709-F-XO977-1124-1024x681.jpeg                      | F16       | 1.00       | Yes     |
| 29771645698247cc1ae4fefc4c538b6f.webp                  | F16       | 1.00       | Yes     |
| airshow-aircraft-fighter-f-16-public-domain.webp       | F15       | 0.47       | No      |
| AP-F16.webp                                            | JAS39     | 0.92       | No      |
| article_5c8845dd9872a9_06637956.png                   | F16       | 1.00       | Yes     |
| dd2e8f1ae29ccfc4df715e884489aefc.webp                  | F16       | 0.97       | Yes     |
| F-16 Fighting Falcon_0 (1).webp                        | F16       | 0.56       | Yes     |
| F-16 Fighting Falcon_0 (2).webp                        | F16       | 0.56       | Yes     |
| F-16 Fighting Falcon_0 (3).webp                        | F16       | 0.56       | Yes     |
| F-16 Fighting Falcon_0.webp                            | F16       | 0.56       | Yes     |
| F-16-5-4119155481.webp                                 | F16       | 1.00       | Yes     |
| f16-1.webp                                             | F16       | 1.00       | Yes     |
| f16-fighting-falcon-fighter-jet-260nw-2460648719.webp  | F16       | 0.51       | Yes     |
| f-16-credit-hellenic-air-force.webp                    | F16       | 1.00       | Yes     |
| f-16-deal-with-pakistan-will-affect-aspects-of-indo-us-ties-pacific-command.webp | F16 | 1.00 | Yes |
| F-16-Viper-at-NAS-Fallon.webp                          | F16       | 0.98       | Yes     |
| F16-Ukraine-1.webp                                     | Tu95      | 0.97       | No      |
| f16.png                                                | F16       | 1.00       | Yes     |
| F16.webp                                               | F16       | 0.38       | Yes     |
| F16_drawing.png                                        | F16       | 1.00       | Yes     |
| final_airtoairloadout_steveotte_lowreswithchute.webp   | F16       | 1.00       | Yes     |
| fully-loaded-f16-fighting-falcon-at-the-us-air-force-v0-gjl2nx950hjb1.webp | F16 | 1.00 | Yes |
| FVccLyeWUAADiXk-1024x620.jpeg.webp                     | JH7       | 0.40       | No      |
| iraqi-f-16s-ukraine-war-fall-out (1).webp              | F16       | 1.00       | Yes     |
| iraqi-f-16s-ukraine-war-fall-out.webp                  | F16       | 1.00       | Yes     |
| mitsubishi-f2-pack-sc-designs-f16-413107-1705487401-AdC1c.webp | F16 | 0.54 | Yes |
| PAF-F-16-2.png                                         | F16       | 0.70       | Yes     |
| Spandahlem_F-16_Poland-01.jpeg                         | F16       | 1.00       | Yes     |
| TopAces_F16_6.webp                                     | F35       | 0.95       | No      |
| TopAces_F16_7.webp                                     | B1        | 0.49       | No      |
| TOPGUN-F-16-Navy.webp                                  | Su34      | 0.97       | No      |
| ukrainian-f-16-ew-system-reprogramming.webp            | F16       | 1.00       | Yes     |
| US-Air-Force-formation-F-16-Fighting-Falcons.webp      | F16       | 0.65       | Yes     |
| why-do-f16s-carry-aim-120s-at-the-wingtips-and-aim-9s-under-v0-mg56by8jttnb1.png | F16 | 1.00 | Yes |
| will-the-f16s-be-able-to-challenge-russian-fighters-v0-qjh36rynqvvb1.webp | F16 | 1.00 | Yes |


Total Images: 66, Correctly Identified F-16s: 50, Accuracy: 75.76%

## How the Code Works

### Dataset

The code was designed to work with the [Military Aircraft Detection Dataset](https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset)

### Key Points

- This program trains a classifier to identify military aircraft types using a dataset of images. It utilizes EfficientNetB3, a pre-trained deep learning model, for feature extraction.
- The program expects the dataset to be organized into subdirectories, where each subdirectory corresponds to a specific aircraft class. The `prepare_data` function iterates through these subdirectories to create a pandas DataFrame containing file paths and their corresponding labels.
- The `split_data` function splits the DataFrame into training, validation, and test sets. Stratified splitting ensures that each set maintains the same ratio of aircraft from the original dataset to the training, validation, and test data sets
- The `create_generators` function uses `ImageDataGenerator` to create generators for training, validation, and testing. The data is preprocessed using EfficientNetB3's specific preprocessing function. Training and validation data are shuffled, while test data is not.
- The `build_model` function constructs a deep learning model:
  - EfficientNetB3 (pre-trained on ImageNet) is used as the base for feature extraction.
  - Additional layers include batch normalization, a dense layer with 256 neurons, dropout, and a softmax output layer.
  - The model is compiled with the Adamax optimizer, categorical cross-entropy loss, and accuracy as a metric.
- The `train_model` function trains the model using the training and validation generators.
  - Two callbacks are used:
    - Early stopping halts training if validation loss does not improve for three consecutive epochs.
    - Learning rate reduction decreases the learning rate if validation loss stagnates for two epochs.
- Training history, including accuracy and loss for both training and validation, is plotted using `matplotlib`.
- After training, the model is saved to a file specified by the `--output` argument.
- The program accepts user-defined parameters via command-line arguments:
  - `--dataset`: Path to the dataset directory.
  - `--batch_size`: Number of samples per batch (default: 32).
  - `--epochs`: Number of epochs for training (default: 20).
  - `--output`: File name for saving the trained model (default: 'aircraft_classifier.h5').
- The program workflow involves:
  - Parsing arguments to configure the dataset, training parameters, and output file.
  - Preparing the dataset and splitting it into training, validation, and test sets.
  - Creating data generators for preprocessing and loading images in batches.
  - Building and training the model using the specified parameters and callbacks.
  - Visualizing training performance.
  - Saving the trained model. 


### `prepare_data` Function

This function creates a DataFrame from the `crop` directory, where each subdirectory corresponds to a class, and files inside are individual data points.

```python
def prepare_data(crop_dir):
    filepaths = []
    labels = []
    for class_name in os.listdir(crop_dir):
        class_dir = os.path.join(crop_dir, class_name)
        if os.path.isdir(class_dir):
            for file in os.listdir(class_dir):
                filepaths.append(os.path.join(class_dir, file))
                labels.append(class_name)
    return pd.DataFrame({"filepaths": filepaths, "labels": labels})
```

#### Explanation:

1. `filepaths = []` and `labels = []`:
   - Initialize empty lists to store file paths and their corresponding labels.

2. `for class_name in os.listdir(crop_dir):`:
   - Iterate over each subdirectory in `crop_dir`. Each subdirectory represents a class (e.g., `F16`, `B52`).

3. `class_dir = os.path.join(crop_dir, class_name)`:
   - Construct the full path to the subdirectory.

4. `if os.path.isdir(class_dir):`:
   - Check if the path is a directory (avoiding non-directory files).

5. `for file in os.listdir(class_dir):`:
   - Iterate over each file in the subdirectory.

6. `filepaths.append(os.path.join(class_dir, file))`:
   - Append the full path of the file to the `filepaths` list.

7. `labels.append(class_name)`:
   - Append the class name (subdirectory name) to the `labels` list.

8. `return pd.DataFrame({"filepaths": filepaths, "labels": labels})`:
   - Combine `filepaths` and `labels` into a DataFrame with columns `filepaths` and `labels`.

---

### `split_data` Function

This function splits the dataset into training, validation, and test sets.

```python
def split_data(df, test_size=0.2, val_size=0.1):
    train_df, test_df = train_test_split(df, test_size=test_size, stratify=df['labels'])
    train_df, val_df = train_test_split(train_df, test_size=val_size, stratify=train_df['labels'])
    return train_df, val_df, test_df
```

#### Explanation:
1. `train_test_split(df, test_size=test_size, stratify=df['labels'])`:
   - Split the dataset `df` into `train_df` (80%) and `test_df` (20%).
   - Stratify ensures each split maintains the proportion of classes as in the original dataset.

2. `train_test_split(train_df, test_size=val_size, stratify=train_df['labels'])`:
   - Further split `train_df` into `train_df` (90% of train set) and `val_df` (10% of train set).
   - Stratify again ensures class proportions are preserved.

3. `return train_df, val_df, test_df`:
   - Return the three splits as DataFrames.

---

### `create_generators` Function

This function creates data generators for training, validation, and testing using `ImageDataGenerator`.

```python
def create_generators(train_df, val_df, test_df, batch_size, img_size=(224, 224)):
    datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.efficientnet.preprocess_input)

    train_gen = datagen.flow_from_dataframe(
        train_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=True
    )
    val_gen = datagen.flow_from_dataframe(
        val_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=True
    )
    test_gen = datagen.flow_from_dataframe(
        test_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=False
    )
    return train_gen, val_gen, test_gen
```

#### Explanation:
1. `datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.efficientnet.preprocess_input)`:
   - Create a data generator with preprocessing specific to EfficientNet models.

2. `datagen.flow_from_dataframe(...)`:
   - Convert a DataFrame into a generator that yields batches of images and labels.
   - `x_col`: Column containing file paths.
   - `y_col`: Column containing class labels.
   - `target_size`: Resize images to 224x224 pixels.
   - `class_mode`: Use categorical mode for multi-class classification.
   - `shuffle`: Randomize the data for training but not for testing.

3. Return:
   - `train_gen`, `val_gen`, and `test_gen` are the generators for training, validation, and testing.

---

### `build_model` Function

This function builds and compiles the deep learning model.

```python
def build_model(num_classes, input_shape=(224, 224, 3)):
    base_model = tf.keras.applications.EfficientNetB3(include_top=False, weights='imagenet', pooling='max', input_shape=input_shape)

    model = Sequential([
        base_model,
        BatchNormalization(),
        Dense(256, kernel_regularizer=regularizers.l2(0.016), activation='relu'),
        Dropout(0.45),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model
```

#### Explanation:
1. `base_model`:
   - Load the EfficientNetB3 model pre-trained on ImageNet.
   - Exclude the top classification layer (`include_top=False`).
   - Use global max pooling on the feature maps (`pooling='max'`).

2. `BatchNormalization()`:
   - Normalize activations to stabilize and speed up training.

3. `Dense(256, ...)`:
   - Fully connected layer with 256 neurons and L2 regularization to prevent overfitting.

4. `Dropout(0.45)`:
   - Randomly drop 45% of neurons during training to reduce overfitting.

5. `Dense(num_classes, activation='softmax')`:
   - Output layer with `num_classes` neurons for classification using the softmax function.

6. `model.compile(...)`:
   - Compile the model with:
     - `Adamax` optimizer (variant of Adam).
     - Categorical cross-entropy loss for multi-class classification.
     - `accuracy` as a performance metric.

---

### `train_model` Function

This function trains the model using the training and validation generators.

```python
def train_model(model, train_gen, val_gen, epochs, callbacks):
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=callbacks)
    return history
```

#### Explanation:
1. `model.fit(...)`:
   - Train the model on `train_gen` and validate on `val_gen`.
   - Run for a specified number of `epochs`.
   - Use `callbacks` to monitor and adjust the training process dynamically (e.g., early stopping).

2. Return:
   - `history` contains training and validation metrics (e.g., loss, accuracy) for each epoch.

---

### 6. Main Script

This is the entry point for the script, handling argument parsing and calling the functions in sequence.

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()

    df = prepare_data(args.dataset)
    train_df, val_df, test_df = split_data(df)
    train_gen, val_gen, test_gen = create_generators(train_df, val_df, test_df, args.batch_size)
    num_classes = len(train_gen.class_indices)
    model = build_model(num_classes)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)
    ]

    history = train_model(model, train_gen, val_gen, args.epochs, callbacks)

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.show()

    model.save(args.output)
```

## How the Math Works

### EfficientNetB3 as the Base Model

#### Input Shape

The input tensor to the model is:

$$
I \in \mathbb{R}^{224 \times 224 \times 3}
$$

where:
- $(224 \times 224)$: Spatial dimensions (height and width).
- $(3)$: Channels (RGB).

---

#### [Convolution Operation](#understanding-kernels-filters-in-convolution)

For more information on how the kernel functions, see [Understanding Kernel Filters in Convolution](#understanding-kernels-filters-in-convolution)

For a kernel (filter) $W$ of size $k \times k$, the convolution is defined as:

$$
z_{ij}^k = \sum_{m=1}^{k} \sum_{n=1}^{k} W_{mn}^k \cdot x_{(i+m)(j+n)} + b^k
$$

where:
- $z_{ij}^k$: The output (feature map) value at position $(i, j)$ in the $k$-th channel.
- $W_{mn}^k$: The weights of the $k$-th filter.
- $x_{(i+m)(j+n)}$: The input pixel values in the receptive field.
- $b^k$: The bias term for the $k$-th filter.

---

#### [Activation Function (ReLU)](#relu-activation-function-and-non-linearity)

After the convolution, a [**ReLU activation**](#relu-activation-function-and-non-linearity) introduces non-linearity:

$$
a_{ij}^k = \max(0, z_{ij}^k)
$$

This ensures the network can model complex patterns.

---

#### Strided Convolutions (Downsampling)

To reduce the spatial dimensions, EfficientNetB3 applies **strided convolutions**. With stride $s$, the output dimensions are calculated as:

$$
h' = \frac{h - k + 2p}{s} + 1, \quad w' = \frac{w - k + 2p}{s} + 1
$$

where:
- $h, w$: Input height and width.
- $h', w'$: Output height and width.
- $k$: Kernel size.
- $p$: Padding size.

---

### [Global Max Pooling](#the-math-of-global-max-pooling)

The model reduces the output of convolutional layers (a 3D tensor $T$) into a 1D vector using [**global max pooling**](#the-math-of-global-max-pooling):

$$
v_k = \max_{i,j} T_{ijk}, \quad \forall k \in [1, c]
$$

where:
- $T_{ijk}$: The value at position $(i, j)$ in the $k$-th channel.
- $c$: The number of channels (1536 for EfficientNetB3).

The resulting vector:

$$
v \in \mathbb{R}^{c}
$$

---

### Fully Connected Layers

#### Batch Normalization

Batch normalization stabilizes and speeds up training by normalizing activations. For each dimension $i$:

$$
\hat{v}_i = \frac{v_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

where:
- $(\mu)$: Mean of the activations in the batch.
- $(\sigma^2)$: Variance of the activations.
- $(\epsilon)$: A small constant to prevent division by zero.

---

#### Dense Layer (256 Units)

A dense (fully connected) layer applies the following operation:

$$
z_i = W_i \cdot \hat{v} + b_i
$$

where:
- $W_i$: Weight vector for the $i$-th neuron.
- $\hat{v}$: Input feature vector.
- $b_i$: Bias term.

Then, the **ReLU activation** is applied:

$$
a_i = \max(0, z_i)
$$

---

#### Dropout

Dropout prevents overfitting by randomly setting a fraction of neurons to zero during training. For each neuron $i$, the output is:

$$
a'_i =
\begin{cases} 
a_i, & \text{with probability } (1-p) \\
0, & \text{with probability } p
\end{cases}
$$

where $p = 0.45$.

---

#### Dense Layer with Softmax (Output Layer)

The final dense layer maps the feature vector to class probabilities using the **softmax activation function**. For the $k$-th class:

$$
p_k = \frac{\exp(z_k)}{\sum_{j=1}^C \exp(z_j)}
$$

where:
- $z_k$: Logit (pre-softmax activation) for class $k$.
- $C$: Total number of classes.
- $p_k$: Predicted probability of class $k$.

---

### Compilation

#### Categorical Cross-Entropy Loss

The loss measures the divergence between the predicted probabilities $\hat{y}$ and true labels $y$:

$$
\mathcal{L} = -\sum_{k=1}^C y_k \log(\hat{y}_k)
$$

where:
- $y_k$: True label for class $k$ (one-hot encoded: 1 for the correct class, 0 otherwise).
- $\hat{y}_k$: Predicted probability for class $k$.

---

#### Adamax Optimizer

Adamax is a variant of Adam that uses the infinity norm for scaling gradients. For a parameter $w_t$ at time $t$:

1. Compute the biased first moment estimate:

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t
$$

2. Compute the infinity norm for gradient scaling:

$$
v_t = \max(\beta_2 v_{t-1}, |g_t|)
$$

3. Update the parameter:

$$
w_{t+1} = w_t - \eta \frac{m_t}{v_t}
$$

where:
- $g_t$: Gradient at time $t$.
- $\eta$: Learning rate.
- $\beta_1, \beta_2$: Decay rates for the moving averages.

### Understanding Kernels (Filters) in Convolution

A **kernel** (or **filter**) is a small matrix that extracts features from an image. The operation involves sliding the kernel over the input image, multiplying its values with the corresponding region of the image (receptive field), summing the results, and optionally adding a bias.

#### Kernel Shape

A kernel $W$ of size $k \times k$ (e.g., $3 \times 3$) is a matrix of weights:

$$
W =
\begin{bmatrix}
w_{11} & w_{12} & w_{13} \\
w_{21} & w_{22} & w_{23} \\
w_{31} & w_{32} & w_{33}
\end{bmatrix}
$$

Each weight $w_{mn}$ is learned during training. For simplicity, let’s assume we are using a single-channel grayscale image (i.e., no RGB).

---

#### Convolution Operation

Given an input image $x$ of size $H \times W$, the kernel slides across the image, stopping at every valid position. At each stop, the kernel performs the following steps:

1. **Element-wise Multiplication**  
   For a given kernel position $(i, j)$, the kernel overlaps a $k \times k$ patch of the image, called the receptive field. The kernel’s values are multiplied with the corresponding values in the receptive field. Mathematically:

   $$
   z_{ij}^k = \sum_{m=1}^{k} \sum_{n=1}^{k} W_{mn}^k \cdot x_{(i+m)(j+n)}
   $$

   Here:
   - $z_{ij}^k$ is the output value at position $(i, j)$ for the $k$-th kernel.
   - $W_{mn}^k$ is the weight at position $(m, n)$ in the kernel.
   - $x_{(i+m)(j+n)}$ is the pixel value in the receptive field of the input image.

2. **Summation**  
   After performing the element-wise multiplication, the results are summed to obtain a single scalar value.

3. **Adding Bias**  
   A bias term $b^k$ (specific to the kernel) is added to the summation:

   $$
   z_{ij}^k = \sum_{m=1}^{k} \sum_{n=1}^{k} W_{mn}^k \cdot x_{(i+m)(j+n)} + b^k
   $$

   This forms the final output value at position $(i, j)$.

---

#### Sliding the Kernel Across the Image

- The kernel starts at the top-left corner of the image.
- It slides horizontally and vertically across the image with a step size called the **stride** ($s$). If $s = 1$, the kernel moves one pixel at a time.

For each valid position, the kernel computes one output value. The collection of all output values forms the **feature map**.

---

### Example: $3 \times 3$ Kernel on a Grayscale Image

#### Input Image

Consider a simple $4 \times 4$ grayscale image:

$$
x =
\begin{bmatrix}
1 & 2 & 3 & 4 \\
5 & 6 & 7 & 8 \\
9 & 10 & 11 & 12 \\
13 & 14 & 15 & 16
\end{bmatrix}
$$

#### Kernel

A $3 \times 3$ kernel:

$$
W =
\begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix}
$$

#### Receptive Field at $(1, 1)$

The receptive field is the top-left $3 \times 3$ submatrix of the input image:

$$
\text{Receptive Field} =
\begin{bmatrix}
1 & 2 & 3 \\
5 & 6 & 7 \\
9 & 10 & 11
\end{bmatrix}
$$

#### Element-wise Multiplication and Summation

Multiply each element of the kernel with the corresponding element in the receptive field:

$$
\begin{aligned}
z_{11} &= (-1)(1) + (0)(2) + (1)(3) + (-2)(5) + (0)(6) + (2)(7) + (-1)(9) + (0)(10) + (1)(11) \\
&= -1 + 0 + 3 - 10 + 0 + 14 - 9 + 0 + 11 \\
&= 8
\end{aligned}
$$

---

### Output Dimensions

The size of the output feature map depends on:
- Input dimensions $(H, W)$.
- Kernel size $k$.
- Stride $s$.
- Padding $p$ (extra pixels added around the edges).

The output height and width are given by:

$$
H' = \frac{H - k + 2p}{s} + 1, \quad W' = \frac{W - k + 2p}{s} + 1
$$

If no padding is applied ($p = 0$) and stride is $1$, the output size for the example would be:

$$
H' = \frac{4 - 3 + 0}{1} + 1 = 2, \quad W' = \frac{4 - 3 + 0}{1} + 1 = 2
$$

Thus, the output feature map is $2 \times 2$.

### ReLU Activation Function and Non-Linearity

ReLU (Rectified Linear Unit) is an activation function applied after the convolution operation. Its purpose is to introduce non-linearity into the network, enabling it to model complex patterns and relationships in data.

For a given output value $z_{ij}^k$ from the convolution at position $(i, j)$ in the $k$-th feature map, the ReLU activation is defined as:

$$
a_{ij}^k = \max(0, z_{ij}^k)
$$

Where:
- $z_{ij}^k$: The raw output from the convolution operation (before activation).
- $a_{ij}^k$: The activated value after applying ReLU.

---

### Step-by-Step Explanation

1. **Input to ReLU**: 
   The input $z_{ij}^k$ can be any real number, positive or negative. This raw value is the result of:
   - Convolution between the kernel and the input image region.
   - Adding a bias term $b^k$.

2. **Non-Linearity Introduction**:
   - If $z_{ij}^k > 0$, then $a_{ij}^k = z_{ij}^k$ (pass the value through unchanged).
   - If $z_{ij}^k \leq 0$, then $a_{ij}^k = 0$ (set the value to zero).
   - This introduces sparsity because negative values are effectively "turned off" in the output.

3. **Purpose of ReLU**:
   - Without ReLU (or other activation functions), the convolution would remain a linear operation. Stacking linear operations leads to a linear transformation, limiting the network's ability to learn complex, non-linear patterns.
   - ReLU ensures that the network can approximate non-linear functions, which are crucial for tasks like image recognition.

---

### Why ReLU is Preferred Over Other Activations

1. **Efficiency**:
   - ReLU is computationally efficient because it involves simple thresholding ($\max(0, z)$).
   - Unlike sigmoid or tanh, it does not require expensive exponential calculations.

2. **Sparsity**:
   - ReLU sets many values to zero, leading to sparse activations. This can improve computational efficiency and reduce overfitting.

3. **Mitigating Vanishing Gradients**:
   - Sigmoid and tanh activations can suffer from vanishing gradients when gradients become extremely small during backpropagation. ReLU avoids this issue for positive values.

---

### Example of ReLU in Action

Suppose a convolution produces the following feature map:

$$
Z =
\begin{bmatrix}
2 & -3 & 4 \\
-1 & 0 & 5 \\
3 & -2 & -4
\end{bmatrix}
$$

After applying ReLU, the activated feature map $A$ is:

$$
A =
\begin{bmatrix}
2 & 0 & 4 \\
0 & 0 & 5 \\
3 & 0 & 0
\end{bmatrix}
$$

---

### Impact of ReLU on Feature Maps

1. **Positive Values are Retained**:
   - Values greater than zero remain unchanged, preserving useful information.

2. **Negative Values are Suppressed**:
   - Negative values are clamped to zero, which introduces sparsity in the feature map.

3. **Interpretation**:
   - The resulting feature map highlights regions where the kernel detected strong positive features, while ignoring irrelevant or negatively correlated features.

### Global Max Pooling: Reducing a 3D Tensor to a 1D Vector

Global max pooling is a down-sampling technique used to summarize the information in a feature map. It reduces the output of convolutional layers (a 3D tensor) into a compact 1D vector by selecting the maximum value from each channel of the tensor.

---

### The Math of Global Max Pooling

Let the output of the convolutional layers be represented as a 3D tensor $T$ of size $h \times w \times c$, where:
- $h$: Height of the feature map.
- $w$: Width of the feature map.
- $c$: Number of channels (features) in the feature map.

The global max pooling operation computes:

$$
v_k = \max_{i,j} T_{ijk}, \quad \forall k \in [1, c]
$$

Where:
- $T_{ijk}$ is the value at position $(i, j)$ in the $k$-th channel of the tensor.
- $\max_{i,j} T_{ijk}$ finds the maximum value in the entire $h \times w$ grid for the $k$-th channel.
- $v_k$ is the resulting value for the $k$-th channel.

The output is a vector $v \in \mathbb{R}^{c}$, where $c$ is the number of channels. For EfficientNetB3, $c = 1536$, so the output vector has 1536 elements.

---

#### Step-by-Step Explanation of Global Max Pooling

1. **Input Tensor**: 
   The input tensor $T$ represents the feature maps after the convolutional layers. For example, if $T$ is of shape $7 \times 7 \times 1536$:
   - There are 1536 channels.
   - Each channel is a $7 \times 7$ matrix of feature values.

2. **Finding Maximum Values**:
   - For each channel $k$, the operation $\max_{i,j} T_{ijk}$ scans the entire $7 \times 7$ grid.
   - It picks the largest value in the grid and assigns it to $v_k$.

3. **Generating the 1D Vector**:
   - After computing the maximum value for all 1536 channels, the result is a 1D vector:
     $$
     v = [v_1, v_2, \dots, v_{1536}]
     $$

---

#### Why Use Global Max Pooling?

1. **Dimensionality Reduction**:
   - It reduces the spatial dimensions ($h \times w$) of the feature maps to a single value per channel.
   - For example, a $7 \times 7 \times 1536$ tensor becomes a $1 \times 1536$ vector.

2. **Retains Salient Features**:
   - By keeping only the maximum value from each channel, it captures the most significant feature activation in that channel.

3. **Parameter-Free**:
   - Unlike fully connected layers, global max pooling does not add any learnable parameters.

4. **Translation Invariance**:
   - It focuses on the presence of a feature rather than its exact location, making the network more robust to spatial translations in the input.

---

#### Example

Suppose a single channel of the feature map $T_k$ (size $3 \times 3$) looks like this:

$$
T_k =
\begin{bmatrix}
0.1 & 0.5 & 0.3 \\
0.7 & 0.2 & 0.4 \\
0.8 & 0.6 & 0.9
\end{bmatrix}
$$

The global max pooling operation computes:

$$
v_k = \max_{i,j} T_{ijk} = \max(0.1, 0.5, 0.3, 0.7, 0.2, 0.4, 0.8, 0.6, 0.9) = 0.9
$$

For all channels, this process repeats, resulting in the final 1D vector $v$.

---

#### Impact of Global Max Pooling

- **Compact Representation**:
  - Converts large, high-dimensional feature maps into small vectors while preserving the most salient features.
  
- **Efficient Computation**:
  - Reduces the computational cost by collapsing spatial dimensions.

- **Simplifies Final Layers**:
  - The resulting vector $v \in \mathbb{R}^{c}$ can directly feed into dense layers for classification.
