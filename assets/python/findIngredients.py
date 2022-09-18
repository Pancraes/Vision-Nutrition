from keras.models import load_model
from PIL import Image, ImageOps, ImageDraw
import numpy as np

# Load the model
model = load_model('Vision-Nutrition/assets/python/keras_model.h5')

# edit this to fit the model
ind=['cucumber','potato','onion','tomato','lettuce','cabbage','carrot','mushroom','peas','beans','beef','chicken','spinach','cheese']

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
# Replace this with the path to your image
im = Image.open('Vision-Nutrition/test/cucumber.jpg')
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
width, height = im.size

ingredients=set()

resultImage=im

for i in range(1, 4):
    subSize=i

    for xi in range(0, subSize*2):
        for yi in range(0, subSize*2):
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            x=xi*width//(subSize*2)
            y=yi*height//(subSize*2)
            image=im.crop((x, y, x+width//subSize, y+height//subSize))

            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            #turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
            prediction = model.predict(data)
            for i in range(len(prediction[0])):
                cur = prediction[0][i]
                if (cur>=0.95):
                    if (ind[i] not in ingredients):
                        draw = ImageDraw.Draw(resultImage)
                        draw.ellipse((x, y, x+width//subSize, y+height//subSize), outline="red",
                                    width=3)
                    ingredients.add(ind[i])

print(ingredients)
resultImage.save('Vision-Nutrition/assets/img/result.jpg')