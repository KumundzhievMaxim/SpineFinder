from tensorflow.keras.backend import minimum, abs, sum, cast, equal, round

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, UpSampling2D, MaxPooling2D, concatenate, Activation, BatchNormalization

from tensorflow.keras import optimizers


def identification_unet(kernel_size, filters, learning_rate):

    main_input = Input(shape=(None, None, 8))

    # 80 x 320
    step_down_1 = Conv2D(filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(main_input)
    step_down_1 = BatchNormalization(momentum=0.1)(step_down_1)
    step_down_1 = Activation("relu")(step_down_1)
    step_down_1 = Conv2D(filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_1)
    step_down_1 = BatchNormalization(momentum=0.1)(step_down_1)
    step_down_1 = Activation("relu")(step_down_1)

    # 40 x 160
    step_down_2 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(step_down_1)
    step_down_2 = Conv2D(2 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_2)
    step_down_2 = BatchNormalization(momentum=0.1)(step_down_2)
    step_down_2 = Activation("relu")(step_down_2)
    step_down_2 = Conv2D(2 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_2)
    step_down_2 = BatchNormalization(momentum=0.1)(step_down_2)
    step_down_2 = Activation("relu")(step_down_2)

    # 20 x 80
    step_down_3 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(step_down_2)
    step_down_3 = Conv2D(4 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_3)
    step_down_3 = BatchNormalization(momentum=0.1)(step_down_3)
    step_down_3 = Activation("relu")(step_down_3)
    step_down_3 = Conv2D(4 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_3)
    step_down_3 = BatchNormalization(momentum=0.1)(step_down_3)
    step_down_3 = Activation("relu")(step_down_3)

    # 10 x 40
    step_down_4 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(step_down_3)
    step_down_4 = Conv2D(8 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_4)
    step_down_4 = BatchNormalization(momentum=0.1)(step_down_4)
    step_down_4 = Conv2D(8 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_down_4)
    step_down_4 = BatchNormalization(momentum=0.1)(step_down_4)
    step_down_4 = Activation("relu")(step_down_4)

    # 5 x 20
    floor = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(step_down_4)
    floor = Conv2D(16 * filters, kernel_size=(5, 20), strides=(1, 1), padding="same")(floor)
    floor = BatchNormalization(momentum=0.1)(floor)
    floor = Activation("relu")(floor)
    floor = Conv2D(16 * filters, kernel_size=(5, 20), strides=(1, 1), padding="same")(floor)
    floor = BatchNormalization(momentum=0.1)(floor)
    floor = Activation("relu")(floor)

    # 10 x 40
    step_up_4 = UpSampling2D(size=(2, 2))(floor)
    step_up_4 = concatenate([step_down_4, step_up_4], axis=-1)
    step_up_4 = Conv2D(8 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_4)
    step_up_4 = BatchNormalization(momentum=0.1)(step_up_4)
    step_up_4 = Activation("relu")(step_up_4)
    step_up_4 = Conv2D(8 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_4)
    step_up_4 = BatchNormalization(momentum=0.1)(step_up_4)
    step_up_4 = Activation("relu")(step_up_4)

    # 20 x 80
    step_up_3 = UpSampling2D(size=(2, 2))(step_up_4)
    step_up_3 = concatenate([step_down_3, step_up_3], axis=-1)
    step_up_3 = Conv2D(4 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_3)
    step_up_3 = BatchNormalization(momentum=0.1)(step_up_3)
    step_up_3 = Activation("relu")(step_up_3)
    step_up_3 = Conv2D(4 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_3)
    step_up_3 = BatchNormalization(momentum=0.1)(step_up_3)
    step_up_3 = Activation("relu")(step_up_3)

    # 40 x 160
    step_up_2 = UpSampling2D(size=(2, 2))(step_up_3)
    step_up_2 = concatenate([step_down_2, step_up_2], axis=-1)
    step_up_2 = Conv2D(2 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_2)
    step_up_2 = BatchNormalization(momentum=0.1)(step_up_2)
    step_up_2 = Activation("relu")(step_up_2)
    step_up_2 = Conv2D(2 * filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_2)
    step_up_2 = BatchNormalization(momentum=0.1)(step_up_2)
    step_up_2 = Activation("relu")(step_up_2)

    # 80 x 320
    step_up_1 = UpSampling2D(size=(2, 2))(step_up_2)
    step_up_1 = concatenate([step_down_1, step_up_1], axis=-1)
    step_up_1 = Conv2D(filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_1)
    step_up_1 = BatchNormalization(momentum=0.1)(step_up_1)
    step_up_1 = Activation("relu")(step_up_1)
    step_up_1 = Conv2D(filters, kernel_size=kernel_size, strides=(1, 1), padding="same")(step_up_1)
    step_up_1 = BatchNormalization(momentum=0.1)(step_up_1)
    step_up_1 = Activation("relu")(step_up_1)

    main_output = Conv2D(1, kernel_size=(1, 1), strides=(1, 1), padding="same",
                         activation='relu')(step_up_1)

    model = Model(inputs=main_input, outputs=main_output)

    # define optimizer
    adam = optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=1e-6)

    model.compile(optimizer=adam, loss=ignore_background_loss, metrics=[vertebrae_classification_rate])

    return model


def ignore_background_loss(y_true, y_pred):
    # y_true = maximum(y_true, epsilon())
    dont_cares = minimum(1.0, y_true)
    return sum(abs(y_pred - y_true) * dont_cares) / sum(dont_cares)


def vertebrae_classification_rate(y_true, y_pred):
    # y_true = K.maximum(y_true, K.epsilon())
    dont_cares = minimum(1.0, y_true)
    return sum(cast(equal(round(y_pred), y_true), 'float32') * dont_cares) / sum(dont_cares)