import tensorflow as tf
import numpy as np
import cv2
import sys

def main():
    if(len(sys.argv) != 3):
        sys.exit("Usage: python recognition.py model_directory image")
    category = recognize_image(sys.argv[1], sys.argv[2])
    print("it belongs to category: ",category)

#load saved model
def load_saved_model(folder):
    model = tf.keras.models.load_model('saved_model')
    print(model.evaluate(x,y))
    return model

#recognize image with the trained model
def recognize_image(theModel, image):
    img = cv2.imread(image)
    img.resize(30,30,3)
    ans = load_saved_model(theModel)
    return ans.predict([np.array(img).reshape(1,30,30,3)]).argmax()

if __name__ == "__main__":
    main()