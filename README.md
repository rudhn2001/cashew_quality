# Cashew Quality Detection System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Dataset](#dataset)
5. [Model Architecture - YOLOv5](#model-architecture)
6. [Installation and Setup](#installation-and-setup)
7. [Testing and Validation](#testing-and-validation)
8. [Running the Project](#running-the-project)
9. [Results and graphs](#results-and-graphs)
---

### 1. Project Overview
The **Cashew Quality Detection System** is a machine learning-based project aimed at automating the classification of cashew quality using image detection techniques. The project uses the **YOLOv5 (You Only Look Once)** object detection algorithm, which is well-suited for real-time object detection tasks. This system aims to help in identifying different quality categories of cashews, providing a fast, efficient, and scalable solution to enhance the manual quality sorting process traditionally used in the cashew industry.

This solution can be expanded for industrial-scale implementations where large volumes of cashews need to be sorted, reducing human effort and increasing accuracy in quality detection.

### 2. Features
- **Cashew Quality Detection**: The system detects and classifies cashew quality into predefined classes based on visual data.
- **Real-Time Processing**: YOLOv5 allows for real-time detection, ensuring that large datasets can be processed efficiently.
- **Customizable Model**: The system can be fine-tuned with additional datasets for further customization, depending on user requirements.
- **High Accuracy**: Leveraging YOLOv5’s architecture, the system can provide high accuracy across multiple cashew quality categories.

### 3. System Architecture
The Cashew Quality Detection System is structured in a modular fashion:
- **Input Data**: The input is provided in the form of cashew images, divided into training, validation, and testing sets.
- **YOLOv5 Detection Model**: The core of the system is a YOLOv5 model that has been trained to recognize and classify cashew images into different quality grades.
- **Output**: The model outputs predictions in the form of bounding boxes and labels, indicating the detected quality of the cashew in the image.
  
The system pipeline includes data preprocessing, model training, validation, and testing phases, all aimed at achieving optimal performance for quality classification.

### 4. Dataset
The dataset used for this project consists of cashew images categorized into four distinct quality classes. The data is divided as follows:
- **Training Set**: Contains 1613 images used to train the YOLOv5 model.
- **Validation Set**: Comprises 149 images for evaluating model performance during training.
- **Test Set**: Consists of 75 images to test the final model.

Each image is labeled appropriately using a bounding box format, as required by YOLOv5. The dataset was processed and augmented using **Roboflow** to ensure better performance and generalization during training.

### 5. Model Architecture - YOLOv5
The core of the system relies on the YOLOv5 object detection architecture. YOLOv5 is well-known for its speed and accuracy in detecting objects in real-time. The model performs image detection and classification simultaneously, making it highly efficient for large-scale cashew quality detection.

#### Key Features of YOLOv5:
- **Single Forward Pass**: YOLOv5 predicts bounding boxes and class probabilities in one go, speeding up the detection process.
- **Anchors and Grids**: The architecture divides the image into grids and uses anchor boxes to detect objects, ensuring precise localization of cashew quality regions.
- **Pretrained Weights**: The system was fine-tuned using pretrained YOLOv5 weights to enhance its initial accuracy and reduce the training time.

Training was conducted over 20–25 epochs, which was found to provide a good balance between accuracy and computational efficiency on the available dataset.

### 6. Installation and Setup
To install this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/rudhn2001/cashew_quality.git
   ```
2. go to yolo directory

   ```bash
   cd yolo
   ```
3. Install the requirements
   ```bash
   pip install -r requirements.txt
   ```

 ### 7. Installation and Setup  
-  Since the model is already trained, you can validate the model using val command. The model is stored in the weights as exp_19.pt and the yaml file is stored in data folder
   ```bash
   python val.py --weights weights/exp_19.pt --data data/cashew.yaml
   ```
the results will be stored in runs folder

### 8. Running the project

- Using the weights trained you can run the model. 
- You have three options : Run the process using the interface, Run the project using webcam, run the model by storing the pictures or videos in the directory
1. If using Interface, then the commands are pre inserted in the interface.py file. However this method is not working fully as there are some bugs present in it, but the code will run and the camera will detect images.One of the good features is that this process after detection part will save the detected images into a zip file and then store that into "Downloads" folder. To use this process, run the command : 

```bash 
python interface.py
```
2. If using Images or Videos method, store the files in pic directory and run the command : 

```bash 
python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source pics/
```
3. if using the webcam, you will have to mention it in placeholder of --source as 0 or 1. 0 will turn on the default webcam of laptop and 1 will run the external webcam connected to laptop. Run the command :  

```bash 
python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source 1
```

- python detect.py: Runs the detection script provided by YOLOv5, which uses a trained model to make predictions on images or videos.
- --weights weights/exp_19.pt: Specifies the path to the trained model weights. In this case, it points to the exp_19.pt file generated after training.
- --img 640: Sets the input image size to 640x640 pixels. YOLOv5 will resize all images to this size for detection. You can adjust this depending on your hardware and accuracy requirements.
- --conf 0.4: Sets the confidence threshold for predictions. The model will only display detections with a confidence score above 0.4 (or 40%). This value can be increased for stricter detections or decreased to allow more potential detections.
- --source pics/: Defines the source of images or videos for detection. In this case, it points to the pics/ folder, which contains the images you want to run detection on. You can also specify a video file or a camera stream (e.g., 0 for a webcam).

### 9. Results and Graphs

- Since the model has been trained, the results and graphs are stored in exp19 directory:
```bash 
cd exp19
```