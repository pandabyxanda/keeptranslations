# pip install --upgrade google-cloud-translate
from google.cloud import translate_v2


# from google.cloud import translate

def translate_text(text, target_language, source_language=None):
    translate_client = translate_v2.Client()
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return result


def make_google_translation(text):
    result = translate_text(text, 'ru', 'en')
    return result
