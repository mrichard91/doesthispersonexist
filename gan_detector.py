import dlib
import numpy as np
from sklearn.metrics import pairwise_distances
from PIL import Image
from io import BytesIO
import hashlib

print("loading detector")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_68.dat')
mean_eyes = np.array([[[130.1382, 190.334 , 142.5089, 182.7387, 157.0245, 183.1371,
        170.5474, 193.1198, 156.29  , 194.9045, 141.7933, 194.8574,
        228.8104, 193.0584, 241.8895, 183.0261, 256.3678, 182.7486,
        268.67  , 190.3242, 257.1241, 194.7404, 242.7394, 194.8258]]])
mean_beyes = np.array([[[170.57202 , 193.121576],
       [156.293828, 194.92348 ],
       [141.789276, 194.877196],
       [228.799716, 193.071276],
       [242.74386 , 194.8333  ],
       [257.128396, 194.743512]]])
eye_indexes = list(range(36,48))
beye_indexes = [39, 40, 41, 42, 47, 46]

def get_face(img):
    img_array = np.array(img)
    fbox = detector(img_array)
    if len(fbox) == 0:
        return None
    else:
        fbox = fbox[0]
    pred = predictor(img_array, fbox)
    return [(pred.part(x).x, pred.part(x).y) for x in range(68)]

def get_pil_img(data):
    img = Image.open(BytesIO(data))
    if img.size != (400,400):
        img = img.resize((400,400))
    if img.mode != "RGB":
        img = img.convert('RGB')
    return img

def scan_data(data):
    sha256 = hashlib.sha256(data).hexdigest()
    img = get_pil_img(data)
    face_pts = get_face(img)
    if face_pts is None:
        eye_dist = [[-1]]
        beye_dist = [[-1]]
    else:
        eyes = np.array([np.array(face_pts)[eye_indexes]])

        flat_pts = eyes.reshape(eyes.shape[0], eyes.shape[1]*eyes.shape[2])
        eye_dist = pairwise_distances(mean_eyes.reshape(1,len(eye_indexes)*2), flat_pts)
        beyes = np.array([np.array(face_pts)[beye_indexes]])

        flat_pts = beyes.reshape(beyes.shape[0], beyes.shape[1]*beyes.shape[2])
        beye_dist = pairwise_distances(mean_beyes.reshape(1,len(beye_indexes)*2), flat_pts)
    return {
        'status': 'ok', 
        'eye_dist': eye_dist[0][0],
        'beye_dist': beye_dist[0][0],
        'dist': eye_dist[0][0],
        'sha256': sha256,
        'face_pts': face_pts,
    } 