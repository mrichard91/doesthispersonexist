import dlib
import numpy as np
from sklearn.metrics import pairwise_distances
import requests
from PIL import Image
from io import BytesIO
import hashlib
import base64

print("loading detector")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_68.dat')
mean_eyes = np.array([[[130.1382, 190.334 , 142.5089, 182.7387, 157.0245, 183.1371,
        170.5474, 193.1198, 156.29  , 194.9045, 141.7933, 194.8574,
        228.8104, 193.0584, 241.8895, 183.0261, 256.3678, 182.7486,
        268.67  , 190.3242, 257.1241, 194.7404, 242.7394, 194.8258]]])
         

def get_eyes(img):
    img_array = np.array(img)
    fbox = detector(img_array)
    if len(fbox) == 0:
        return None
    else:
        fbox = fbox[0]
    pred = predictor(img_array, fbox)
    return [(pred.part(x).x, pred.part(x).y) for x in list(range(36,48))]

def get_pil_img(data):
    img = Image.open(BytesIO(data))
    if img.size != (400,400):
        img = img.resize((400,400))
    return img

def scan_data(data):
    sha256 = hashlib.sha256(data).hexdigest()
    img = get_pil_img(data)
    eyes = get_eyes(img)
    if eyes is None:
        dist = [[-1]]
    else:
        eyes = np.array([eyes])
        flat_pts = eyes.reshape(eyes.shape[0], eyes.shape[1]*eyes.shape[2])
        dist = pairwise_distances(mean_eyes.reshape(1,24), flat_pts)
    return {
        'status': 'ok', 
        'dist': dist[0][0],
        'sha256': sha256,
    } 