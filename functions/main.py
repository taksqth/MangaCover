import json
from google.cloud import storage

from fastai.vision.all import *


def _get_learner():
    client = storage.Client()
    bucket = client.get_bucket("manga-classifier-model")
    blob = bucket.blob("export_multicat.pkl")
    blob.download_to_filename("/tmp/model.pkl")
    learner = load_learner("/tmp/model.pkl")
    return learner


def _get_predictions(learner, image, thresh=0.5):
    _, _, probs = learner.predict(image)
    preds = list(zip(learner.dls.vocab, [prob.item() for prob in probs]))
    preds = [(lab, prob) for lab, prob in preds if prob >= 0.5]
    preds.sort(key=lambda x: x[1], reverse=True)
    return json.dumps(
        {
            "preds": [
                {
                    "label": label,
                    "probability": prob,
                }
                for label, prob in preds
            ]
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
