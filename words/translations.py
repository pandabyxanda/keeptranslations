"""
How to install lib:
pip install --upgrade google-cloud-translate
if Google can't authenticate:
install google sdk, create json
credential_path = "D:\...... .json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
"""
from google.cloud import translate_v2


# from google.cloud import translate

def make_google_translation(text, target_language='ru', source_language='en'):
    translate_client = translate_v2.Client()
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return result
