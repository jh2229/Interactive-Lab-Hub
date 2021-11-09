# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***
Contours Detection Screenshot
![1 - Contours](https://user-images.githubusercontent.com/89954387/140847951-ae4b7085-093d-41a9-8e6a-ec9a2b0efe8c.jpg)
The contour detection may be useful for a mobile app that filters the image being filmed so that only the silhouette appears. The silhouette or the contour lines are useful for measuring geometric aesthetics (i.e. distances and angles between features in the face such as the eyes to the nose, nose to the mouth etc.)

Face Detection Screenshot
![2 - Face Detection](https://user-images.githubusercontent.com/89954387/140848002-e84a8c01-0ae2-48a3-ac4d-2fbb2efafba1.jpg)
The face detection is useful for processing through videos to categorize videos according to the number of people that appear in the video. For example, just like Facebook/Instagram has a feature of auto-tagging people, it may be useful to automatically or manually tag other influencers or people with profiles within the platform. That way, people can search videos of influencers that they like according to the name tags.

Flow Detection Screenshot
![3 - Flow Detection](https://user-images.githubusercontent.com/89954387/140848018-4616a62d-a853-48e9-89e0-491201053c3a.jpg)
With more precision, this tool could be used to track body movements when testing UX with interactive media (i.e. games, films). A more focused person would move less than a less focused person, and this tool would be able to track this and interpreted as a measure of immersive story telling of the media.

Object Detection Screenshot
![4 - Object Detection](https://user-images.githubusercontent.com/89954387/140848088-6b2c2c11-e82a-4c92-81b5-6627f2cdebe3.jpg)
This tool may be useful in quick count of objects, such as in an assemblyline of a factory. A quick check of the number of people in certain rooms or the number of items on a given set may help quality and safety management for production.


#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)

Hand Pose Detection
![6 - Hand Pose](https://user-images.githubusercontent.com/89954387/140848216-43fbc824-4125-4359-a1e7-b1c268b9619f.jpg)
With high-calibre cameras, I can see this being used in stadiums by professional baseball teams to analyze and interpret the hand gestures signalling baseball tactics by other teams' coaches at the dugout.



#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***

Teachable Machine Screenshots
![6 - Hand Pose](https://user-images.githubusercontent.com/89954387/140848334-50f770d3-2bee-4fa0-b805-d930898fbcf3.jpg)
![No Smile](https://user-images.githubusercontent.com/89954387/140848354-4c1e4a6b-aab3-4aca-9ebf-2ca8b2181567.jpg)
![Smile](https://user-images.githubusercontent.com/89954387/140848369-d005a90a-01e2-4c8f-a447-1c525f964158.jpg)
Comedy is an area where it can be very hit-and-miss and often the quality of comedy is often judged by how well the audience responds to the comedy content by smiling or laughing. I think directors/producers/actors or even stand-up comedians can make use of this to sharpen their comedy by pre-testing their comedy content in a similar way game developpers pre-test their game UX with participants.
The Teachable Machine tool adds much flexibility in that anybody can train models to detect for whatever element. The OpenCV or MediaPipe tool feels more rigid pre-defined in the elements that it detects.


*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***
![image](https://user-images.githubusercontent.com/89954387/140863997-b8bab20f-c78a-4909-be74-d1df001d0d82.png)
![No Smile](https://user-images.githubusercontent.com/89954387/140864112-ee7150f0-0245-45de-b052-1aef505b05f7.jpg)
![Smile](https://user-images.githubusercontent.com/89954387/140864128-9ef168c9-2f96-41ac-87ef-d287574cdbfc.jpg)
I'm having to record at different angles and lightings and distances. Otherwise, the Teachable Machine tool is not able to sufficiently train to catch for all the idiosyncratic ways a human expresses emotions.

For example, my facial expressions at that distance (from the picture shown) are classified correctly. However, if I moved just a bit further or closer from that distance, the model misclassifies my expression as a smile. Maybe it's just that I am terrible at smiling, which is very possible, in which case, my trained model would have learned my human error.
Assuming that I am a sufficiently good enough "model" for training my model, then by recording from different angles, lightings, and turns of the visage, the model will be more prepared to detect those 'edge cases'.

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do? The model is intended to detect a smile on a face.
1. When does it fail? It fails if the face is not properly lit or if the face is not at the proper distance from the camera.
1. When it fails, why does it fail? The model may not be sufficiently trained and/or the quality of the webcam does not allow for more detailed cues to be picked up for training. Since the silhouette of a smiling face is harder to delineate against a silhouette of a resting face, the expression is harder to train for, especially with the quality of an ordinary webcam.
1. Based on the behavior you have seen, what other scenarios could cause problems? 
If another person or hand features in the screen, the model breaks sometimes, since the model is only trained with my facial expressions.

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system? No, they would initially not be aware of the uncertainties. They would fully expect the system to work. Ideally, the partcipant would not be made aware of the system, so that their true emotions are displayed.
1. How bad would they be impacted by a miss classification? This would hurt the meaning of the data being gathered. A film director may mistake the entertainment value of of his/her film based on inaccurate classifcations.
1. How could change your interactive system to address this? A better trained model may address this. However, a more effective method would be to implement a sensor to measure heart rate or an eye tracking device to gauge the engagement level of the participant with the content being consumed.
1. Are there optimizations you can try to do on your sense-making algorithm? More background settings, more diverse faces, different angles and lighting. An initial calibration with each participant's resting face would make it easier to detect changes in the facial expressions. Also, a scale of expression intensity may be helpful in order to detect semi-clear expressions such as a grin or a smirk, which are not quite smiles, but still indicators of emotion.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for? Use X to detect smiles to judge the comedy value of a content (i.e. audio, video, webtoon).
* What is a good environment for X? Good lightning with clear and contrasting background to the face, preferrably similar to the training environment.
* What is a bad environment for X? Dark lighting and poor contrast to the face.
* When will X break? When the participant is too far or at an awkward angle away from the camera, such that the camera does not have sufficient cues to classify the expression, or when the participant's physical features are not trained for.
* When it breaks how will X break? Misclassification of the expression
* What are other properties/behaviors of X? The model will require training of more edge cases, often unexpected.
* How does X feel? Hopefully all smiles when the participant smiles

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***
https://drive.google.com/file/d/1Y7tzryWuQJhexR7hA7IYmPTbATwwTosM/view?usp=sharing

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
https://drive.google.com/file/d/1LZO-q7IUpEY-Tlytw00G1quqvTp233gY/view?usp=sharing
