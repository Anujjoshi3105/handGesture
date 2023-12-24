import cv2
import pickle
import mediapipe as mp
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def hand_gesture(frame):
    hands = mp.solutions.hands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=1)
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    data = []

    if results.multi_hand_landmarks:
        x_min, y_min = float('inf'), float('inf')
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x, y = landmark.x, landmark.y
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                data.extend([x - x_min, y - y_min])

    hands.close()
    return data

def process_data(imgList, directory, filename):
    data = {'data': [], 'labels': []}

    for img in imgList:
        frame = cv2.imread(img)
        label = img.split('/')[-1].split('_')[0]
        feature = hand_gesture(frame)

        if feature:
            data['data'].append(feature)
            data['labels'].append(label)

    with open(f'{directory}/{filename}', 'wb') as f:
        pickle.dump(data, f)


def train_model(directory, filename):
    try:
        with open(f'{directory}/{filename}', 'rb') as data_file:
            data_dict = pickle.load(data_file)
    except (FileNotFoundError, EOFError):
        print("DATASET NOT PROCESSED")
        return

    data = data_dict['data']
    labels = data_dict['labels']

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, shuffle=True, stratify=labels)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    y_predict = model.predict(x_test)
    score = accuracy_score(y_predict, y_test) * 100

    with open(f'{directory}/{filename}.p', 'wb') as f:
        pickle.dump({'model': model}, f)

    return score