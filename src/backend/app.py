import multiprocessing
import time
from flask import Flask, jsonify, request
from pylsl import StreamInlet, resolve_stream
from keras.models import load_model
import json
import numpy as np
import pandas as pd
import scipy
from scipy.signal import filtfilt


sliced_list = []
sample = []
segments = []
fireIndex = -1
gridSize = 0
start_index = -1
counter = 0
startPage = 0
indexSend = -1
first_index = -1
end_index = -1
ind = -1
Model = load_model("CNN_EEG_checkpoint_5.h5")
print(type(Model))
app = Flask(__name__)


@app.route('/streamer', methods=['GET'])
def streamer():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    global sample
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        row, timestamp = inlet.pull_sample()
        row[0] = round(float(row[0]), 2)
        row = row[:1] + row[3:-2]
        sample.append(row)


@app.route('/sendgridsize', methods=['POST'])
def postGride():
    global gridSize
    global startPage
    global indexSend
    indexSend = -1
    gridSize = request.data
    gridSize = int(gridSize.decode())
    startPage = 1
    print(" "+str(gridSize))
    return "got grid size!"


counter = 0


@app.route('/getindex', methods=['GET'])
def getJson():
    global indexSend
    global ind
    ind = indexSend
    indexSend = -1
    return str(ind)


@app.route('/sendtimestamp', methods=['POST'])
def post_string():
    global Model
    global start_index
    global sliced_list
    global sample
    global fireIndex
    global counter
    global gridSize
    global startPage
    global indexSend
    global first_index
    global end_index
    # if startPage == 1:
    string = request.data
    numbers = string.decode().split(', ')
    print(numbers)
    result = [float(numbers[0]), int(numbers[1])]
    print(result)
    for i, sublist in enumerate(sample):
        if sublist[0] == result[0]:
            first_index = i
            end_index = first_index + 256
            break

    sliced_list = sample[first_index:end_index]
    sliced_list = [sublist[1:] for sublist in sliced_list]
    numbyArray = np.array(sliced_list)
    numbyArray = numbyArray.reshape(256, 14)
    prepproccessedSegment = preprocess(numbyArray)
    prepproccessedSegment = np.reshape(prepproccessedSegment, (-1, 14, 32, 1))
    ModelResult = Model.predict(prepproccessedSegment)
    print(f"Model Result : {ModelResult}")
    res = ModelResult[0][0].round()
    res = int(res)
    print(f"result after rounded: {res}")
    # and ModelResult[0][0]>0.8
    if res == 1:
        fireIndex = result[1]
        startPage = 0
        indexSend = str(fireIndex)
        res = 0
    else:
        indexSend = -1
    print("index: " + str(indexSend)+"\n")

    return 'String posted successfully'


def preprocess(segment):
    filterorder = 3
    filtercutoff = [1/128, 12/128]
    f_b, f_a = scipy.signal.butter(filterorder, filtercutoff, btype='bandpass')

    decimation = 8

    filtered_array = np.empty_like(segment)
    downsampled_array = np.empty((32, 14))
    final_array = np.empty((32, 14))

    for column in range(segment.shape[1]):
        column_data = segment[:, column]
        filtered_array[:, column] = filtfilt(f_b, f_a, column_data)

        downsampled_array[:, column] = filtered_array[:, column][::8]

        clmn_data = downsampled_array[:, column]
        lower_limit = np.percentile(clmn_data, 10)
        upper_limit = np.percentile(clmn_data, 90)

        windsorized_data = np.clip(clmn_data, lower_limit, upper_limit)

        # Calculate the mean and standard deviation of the signal
        mean = np.mean(windsorized_data)
        std = np.std(windsorized_data)

        # Normalize the signal using Z-score
        normalized_signal = (windsorized_data - mean) / std

        final_array[:, column] = normalized_signal

    return final_array


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
