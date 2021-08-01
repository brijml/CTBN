import numpy as np
import pandas as pd
from scipy.io import arff

from src import CTBN

def get_data_numpy(data_arff):
    df = pd.DataFrame(data_arff[0])
    features, labels = df.columns[:294], df.columns[294:]
    X, Y = df[features].to_numpy(), np.uint8(df[labels].to_numpy())
    return X, Y

train_data = arff.loadarff("data/scene/scene-train.arff")
X_train, Y_train = get_data_numpy(train_data)

test_data = arff.loadarff("data/scene/scene-test.arff")
X_test, Y_test = get_data_numpy(test_data)

def test_model_fitting():
    model = CTBN()
    model.fit(X_train, Y_train)
    model.predict(X_test[0])
    assert True