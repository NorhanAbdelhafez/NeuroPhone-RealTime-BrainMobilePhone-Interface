# NeuroPhone: Real-Time Brain-Mobile Phone Interface

A research project that explores the potential of deep learning models in detecting ERPs (p300) in EEG brain signals. From EDA to modeling, we developed an end-to-end training and evaluation workflow that achieved an average classification accuracy of 98% on the EPFL dataset. We utilized the results we achieved in building a mobile phone communication application (Neurophone) that enables people with motor disabilities to communicate with others through their visual attention. Furthermore, we built a hardware circuit for EEG measurement and eventually used the commercial EMOTIV EPOC X for connecting and integrating with our Neurophone.

It's important to emphasize that we are essentially dealing with a binary classification problem, where we essentially aim to classify whether the EGG brain signal contains a P300 peak or not. It's the core research quest that this project is all about.

Our project was one of the few shortlisted projects that were selected to participate in the prestigious 16th Undergraduate Research Forum and the 4th Egyptian Junior Researcher Competition at Nile University. We were also accepted in 2 Funding programs (The Academy of Scientific Research & Technology (ASRT) & Information Technology Industry Development Agency (ITIDA)), You can find the submitted funding application forms in 'docs/Funding Forms'.

## Repository Information and Structure
This repository houses all the work related to our graduation project, including data, code, and third-party software.

### Where to Find What?
- All analysis, preprocessing, training, and evaluation notebooks are located in the 'research/' directory.
- The Flutter App source code, including all used files and assets, can be found in the 'scr/' directory.
- Our project documentation, including the bachelor thesis, seminar presentations, and funding program application forms, is stored in the 'docs/' directory.

## Project Life Cycle
Our project has undergone several phases:
- Dataset
- Preprocessing
- Modeling
- Interface building (creating Neurophone)
- Application
- Demo

## Dataset
We utilized two datasets for our project. The first is the publicly available EPFL P300 dataset, extensively used in prior research. Additionally, we collected our dataset from a single subject using the EMOTIV EPOC X 14 headset.

#### EPFL P300 dataset
The experimental setup involved users facing a laptop screen displaying six images flashed in random sequences, one image at a time. Each image flash lasted 100 ms, followed by a 300 ms pause, resulting in a 400 ms interstimulus interval (ISI). EEG data was recorded at a 2048 Hz sampling rate from 32 electrodes positioned according to the 10–20 international system. Each subject completed 4 recording sessions, with each session consisting of 6 runs corresponding to the 6 images. For detailed recording protocol information, refer to the "Experimental Schedule" section in the 'docs/hoffmann2008.pdf' paper.

#### Our Collected Dataset
We followed a similar paradigm to the EPFL dataset but presented the user with a (3 x 2) grid containing 6 choices that flashed in random order. Each choice was flashed for 100 ms, followed by a 300 ms pause. The user recorded 6 sessions, each lasting 90 seconds, with a sampling rate of 256 Hz.

## Preprocessing
Our analysis and preprocessing aimed to understand EEG signals, identify deviations, and highlight essential patterns.

For data analysis, we explored the dataset's structure, loaded the data appropriately, and experimented with signal processing techniques.

In the preprocessing phase, we performed the following steps:
1. Segmented the data, each segment containing an event.
2. Referenced the signal using the average signal from the two mastoid electrodes.
3. Filtered the signal using a third-order Butterworth filter to range from 1 to 12 Hz.
4. Downsampled the signal to 64 Hz.
5. Applied signal normalization techniques, including min-max normalization and z-score normalization.
6. Employed windsorizing to replace extreme values with less extreme values while maintaining them within an acceptable range.

## Modeling
Our modeling phase initially explored traditional machine learning approaches with wavelet transform for feature extraction. Later, we transitioned to deep learning architectures. We trained and evaluated various deep learning models, including Chrononet, EEGNet, DCRNN, CNNs, RNNs, and CNN-LSTMs. The Convolutional Neural Networks (CNNs) with K-fold and weighted class models emerged as the best-performing model, achieving an impressive average classification accuracy of 98% from a single trial, outperforming other state-of-the-art models.

Our Best Performing CNN Model:
CNNs are known for their effectiveness in EEG analysis, capable of extracting spatial features from EEG signals. They excel in tasks such as motor imagery classification, emotion recognition, and seizure detection. In our P300 detection task, CNNs outperformed other models. Refer to the architecture used for our network in the provided image.

![image](https://github.com/NorhanAbdelhafez/NeuroPhone-RealTime-BrainMobilePhone-Interface/assets/62456227/6c70bda6-dd79-4ba3-af41-3f8996ad6f56)

## Interface building
To create the final interface, we integrated the Emotiv headset with its accompanying software, connecting it to our mobile application. The Emotiv headset communicates with EmotivPro software through a PC, either via Bluetooth or a dongle, to visualize the EEG signal. We utilized the Lab Streaming Layer (LSL) option within EmotivPro to stream the EEG signal to our application in real-time.

![image](https://github.com/NorhanAbdelhafez/NeuroPhone-RealTime-BrainMobilePhone-Interface/assets/62456227/6797660e-5b83-440c-99da-8fb7037eceaa)


Lab Streaming Layer (LSL) is a versatile software framework that facilitates data acquisition, synchronization, and sharing from various sensors. LSL is platform-independent and compatible with a wide range of devices, including EEG headsets, eye trackers, and motion sensors. It establishes a network of data streams, each identified by a unique name and containing a time series of data points. These data points can encompass any numerical value, such as voltage, acceleration, or temperature. For more information on Emotiv software and Lab Streaming Layer, watch our recorded video [here](https://drive.google.com/file/d/1knvs0iG5Ho1RGqegf9wdyhoy7e6SobmJ/view?usp=sharing).


## Application
The NeuroPhone application's purpose is to enable individuals with disabilities to use mobile phones by solely relying on brain signals. It primarily relies on EEG signals and the detection of the P300 peak. The application employs a grid system where each grid flashes randomly. Each grid flash lasts for 100 milliseconds, followed by a 300-millisecond pause. This design allows us to detect the presence of a P300 peak in the EEG signal.

Our project workflow involves connecting an Emotiv headset with a dongle to a PC and linking it to the EmotivPro application. Data streaming is initiated through the Lab Streaming Layer option within the application.

We've developed an API using the Flask library in Python. This API receives real-time raw EEG signals sent via Lab Streaming Layer from the Emotiv headset. The API operates continuously without interruption, with a sampling rate of 256 Hz.

Additionally, we've created another API that our Flutter application uses to transmit the timing and index of each flash. This enables us to synchronize the flashing sequence with the EEG signal received from the Emotiv headset. Upon receiving the raw EEG signal, we segment it into 1000ms segments, preprocess the segments to reduce noise, and prepare them for input into our model. The model provides a label, either 0 (no P300 peak in the segment) or 1 (P300 peak present).

We've established a JSON file to store the model's results and the corresponding grid index synchronized with the signal triggering the P300 peak. This information is crucial for alerting the application and activating the user's intended choice, which triggered the appearance of the P300 peak.

To achieve this, we've created an additional API that the mobile application accesses to determine if a peak has occurred and to trigger the choice associated with the index recorded in the JSON file when the peak result is 1.

![image](https://github.com/NorhanAbdelhafez/NeuroPhone-RealTime-BrainMobilePhone-Interface/assets/62456227/29cdbe99-c22c-428e-bc5c-c3768c881046)


## Demo

<video width="400" height="300" controls>
  <source src="https://github.com/NorhanAbdelhafez/NeuroPhone-RealTime-BrainMobilePhone-Interface/blob/main/docs/demo.mp4">
</video>
