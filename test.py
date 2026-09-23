from roboflow import Roboflow
import cv2
import numpy as np
rf = Roboflow(api_key="BSxCq35rmLUE7MNVOUpx")
project = rf.workspace("dataset-urrjn").project("dataset1-czkg7")
model = project.version(5).model
# infer on a local image
image_path="images/img1.png"
image = cv2.imread(image_path)
print(model.predict("images/img1.png", confidence=40, overlap=30).json())
predictions = model.predict(image_path, confidence=40, overlap=30).json()
# Draw bounding boxes on the image
for prediction in predictions['predictions']:
    x1 = prediction['x'] - prediction['width'] / 2
    y1 = prediction['y'] - prediction['height'] / 2
    x2 = prediction['x'] + prediction['width'] / 2
    y2 = prediction['y'] + prediction['height'] / 2
    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(image, f"{prediction['class']}: {prediction['confidence']:.2f}",(int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
# Display the image
cv2.imwrite("image_with_bounding_boxes.jpg", image)