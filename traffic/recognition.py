import tensorflow as tf
import numpy as np
import cv2
import sys

signDict = {0: 'stop', 1: 'straight or left', 2:'speed limit'}

def main():
    if(len(sys.argv) != 3):
        sys.exit("Usage: python recognition.py model_directory image")
    category = recognize_image(sys.argv[1], sys.argv[2])
    print("I think it's ",category," sign")

#load saved model
def load_saved_model(folder):
    model = tf.keras.models.load_model('saved_model')
    # print(model.evaluate(x,y))
    return model

#recognize image with the trained model
def recognize_image(theModel, image):
    img = cv2.imread(image)
    img.resize(30,30,3)
    img = img/255
    ans = load_saved_model(theModel)
    ans.summary()
    arr = ans.predict([np.array(img).reshape(1,30,30,3)])
    print([float(i) for i in arr[0]])
    return signDict[ans.predict([np.array(img).reshape(1,30,30,3)]).argmax()]

if __name__ == "__main__":
    main()