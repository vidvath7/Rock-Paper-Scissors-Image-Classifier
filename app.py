from flask import Flask,render_template,request
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
import os


app=Flask(__name__,template_folder='Templates')

@app.route("/",methods=['GET'])
def home_page():   
    return render_template('index.html')   


@app.route("/",methods=['POST'])
def predict():
    imagefile=request.files['imagefile']
    #imagepath="./images/"+imagefile.filename
    imagepath=os.path.join("./images",imagefile.filename)
    imagefile.save(imagepath)

    image=load_img(imagepath,target_size=(150,150))
    image=img_to_array(image)
    image=np.expand_dims(image,axis=0)
    image=image/255.

    model=tf.keras.models.load_model('model_cnn.hdf5')
    prediction=model.predict(image)
    label=np.argmax(prediction,axis=-1)

    result=' '
    if label==0:
        result="paper"
    elif label==1:
        result="rock"
    else:
        result="scissors"

    return render_template('index.html',output=result)

if __name__ == "__main__":
# app.run(host, port, debug, options)
    app.run(port=3000,debug=True)
	