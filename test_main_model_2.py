from keras.models import load_model
import numpy as np
from utility_functions import opening_files
import matplotlib.pyplot as plt

model = load_model('main-model.h5')

volume = opening_files.read_nii("datasets/spine-1/patient0023/4542094/4542094.nii.gz")
volume = volume.reshape(1, 512, 512, 186, 1)

result = model.predict(volume).reshape(3)

np.save("histogram", result)