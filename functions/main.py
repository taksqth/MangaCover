from google.cloud import storage
from mangacover.model import load_learner_and_predict

LEARNER_BUCKET = 'manga-classifier-model'
LEARNER_BLOB = 'export_multicat.pkl'
LEARNER_PATH = '/tmp/model.pkl'

def _download_learner():
    client = storage.Client()
    bucket = client.get_bucket(LEARNER_BUCKET)
    blob = bucket.blob(LEARNER_BLOB)
    blob.download_to_filename(LEARNER_PATH)


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

    _download_learner()
    return (load_learner_and_predict(LEARNER_PATH, file), 200, headers)
