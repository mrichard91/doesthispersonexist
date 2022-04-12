import dlib
import numpy as np
from sklearn.metrics import pairwise_distances
import requests
from PIL import Image
from io import BytesIO
import hashlib
import base64

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_68.dat')
mean_eyes = np.array([[[130.089, 190.317, 142.481, 182.701, 157.041, 183.098, 170.551,
         193.113, 156.281, 194.948, 141.763, 194.884, 228.793, 193.048,
         241.855, 182.979, 256.366, 182.691, 268.612, 190.299, 257.163,
         194.742, 242.73 , 194.852]]])
         

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

def get_image_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.content
        sha256 = hashlib.sha256(data).hexdigest()
        return (data, sha256)
    return None

def scan_data(b64data):
    try:
        data = base64.b64decode(b64data)
        sha256 = hashlib.sha256(data).hexdigest()
    except Exception as e:
        print("could not decode")
        return {'status': 'fail', 'error': f'could not decode {len(b64data)} {b64data[:10]}'}
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


def scan_url(url):
    try:
        data, sha256 = get_image_data(url)
    except Exception as e:
        print(f'couldnot fetch {url} because {e}')
        return {'status': 'fail', 'error': str(e)}
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
        'img_url': url,
    } 
