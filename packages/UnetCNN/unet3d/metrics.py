from functools import partial
import numpy as np

from keras import backend as K


# my custom loss function
# https://gist.github.com/wassname/ce364fddfc8a025bfab4348cf5de852d
def weighted_cross_entropy(y_true, y_pred):
    # permute dimensions to make consistent
    y_true_perm = K.permute_dimensions(y_true, (0, 2, 3, 4, 1))
    y_pred_perm = K.permute_dimensions(y_pred, (0, 2, 3, 4, 1))

    weights = np.ones(27)
    weights[0] = 0.01
    weights = weights / np.sum(weights)
    weights = K.variable(weights)
    # clip to prevent NaN's and Inf's
    y_pred_perm = K.clip(y_pred_perm, K.epsilon(), 1 - K.epsilon())
    loss = y_true_perm * K.log(y_pred_perm) * weights
    loss = -K.sum(loss, -1)
    return loss


def dice_coefficient(y_true, y_pred, smooth=1.):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coefficient_loss(y_true, y_pred):
    return -dice_coefficient(y_true, y_pred)


def weighted_dice_coefficient(y_true, y_pred, axis=(-3, -2, -1), smooth=0.00001):
    """
    Weighted dice coefficient. Default axis assumes a "channels first" data structure
    :param smooth:
    :param y_true:
    :param y_pred:
    :param axis:
    :return:
    """
    return K.mean(2. * (K.sum(y_true * y_pred,
                              axis=axis) + smooth/2)/(K.sum(y_true,
                                                            axis=axis) + K.sum(y_pred,
                                                                               axis=axis) + smooth))


def weighted_dice_coefficient_loss(y_true, y_pred):
    return -weighted_dice_coefficient(y_true, y_pred)


def label_wise_dice_coefficient(y_true, y_pred, label_index):
    return dice_coefficient(y_true[:, label_index], y_pred[:, label_index])


def get_label_dice_coefficient_function(label_index):
    f = partial(label_wise_dice_coefficient, label_index=label_index)
    f.__setattr__('__name__', 'label_{0}_dice_coef'.format(label_index))
    return f


dice_coef = dice_coefficient
dice_coef_loss = dice_coefficient_loss