import json
from google.cloud import storage

from fastai.vision.all import *


def _get_learner():
    client = storage.Client()
    bucket = client.get_bucket("manga-classifier-model")
    blob = bucket.blob("export.pkl")
    blob.download_to_filename("/tmp/model.pkl")
    learner = load_learner("/tmp/model.pkl")
    return learner


def _get_predictions(learner, image):
    pred_class, pred_idx, probs = learner.predict(image)
    return json.dumps(
        {
            "pred": pred_class,
            "prob": f"{probs[pred_idx]:.04f}",
        }
    )


def predict(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}
    file = request.files["file"]

    learner = _get_learner()
    image = PILImage.create(file)
    return (_get_predictions(learner, image), 200, headers)
