from fastapi import FastAPI
from pydantic import BaseModel
from utils.qrDetector import QRDetector

from PIL import Image
import base64
from io import BytesIO

app = FastAPI()

qr_detector = QRDetector()

class RequestImage(BaseModel):
    imgBase64: str

@app.post("/get-qrs")
def get_qrs_detection(data: RequestImage):
    
    input_image = Image.open(BytesIO(base64.b64decode(data.imgBase64))).convert('RGB')

    # image de entrada ya como Pillow.Image
    status, response = qr_detector.detect(input_image)

    detection_dict = {}

    for index, qr in enumerate(response):
        bbox = qr.getBoundingBox()

        detection_dict[str(index)] = [int(bbox.left), int(bbox.top), int(bbox.right), int(bbox.bottom)]


    return {
        'status': status,
        'response': dict(detection_dict)
    }

