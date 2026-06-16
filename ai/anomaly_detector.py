from sklearn.ensemble import IsolationForest

import numpy as np


# Training data
normal_data = np.array([

    [35000, 820],
    [36000, 830],
    [37000, 840],
    [35500, 810],
    [36500, 850],
    [38000, 870],
    [34000, 800],
    [39000, 890]

])


# Train model
model = IsolationForest(

    contamination=0.1,

    random_state=42
)

model.fit(normal_data)


def detect_anomaly(

    altitude,

    speed
):

    test = np.array([
        [altitude, speed]
    ])

    prediction = model.predict(test)

    return prediction[0]