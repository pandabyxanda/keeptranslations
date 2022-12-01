# pip install --upgrade google-cloud-translate
from google.cloud import translate_v2
from google.cloud import translate

def translate_text(text, target_language, source_language=None):
    translate_client = translate_v2.Client()
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return result

def make_google_translation(text):
    result = translate_text(text, 'ru', 'en')
    # print(result)
    return result

# text = "As you can see, this is only returning a single word. The dictionary lookup on the google
# translate page must be an additional call to a different service (not part of the translate service)"
# # text = "machine is running"
# text2 = "to run"
# text3 = "the run"
# result = translate_text(text, 'ru', 'en')
# print(result)
# result = translate_text(text2, 'ru', 'en')
# print(result)
# result = translate_text(text3, 'ru', 'en')
# print(result)
