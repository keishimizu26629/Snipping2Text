from google.cloud import vision
from google.oauth2 import service_account
import pyperclip
import glob

def image_to_text(img_bytes):
    files = glob.glob('./api-key/*.json')
    credentials = service_account.Credentials.from_service_account_file(files[0])

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # image = vision.Image(content=content)
    image = vision.Image(content=img_bytes)

    # Performs label detection on the image file
    response =  client.document_text_detection(
            image=image,
            image_context={'language_hints': ['ja']}
        )

    # レスポンスからテキストデータを抽出
    output_text = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    output_text += ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                output_text += '\n'
    pyperclip.copy(output_text)

if __name__ == '__main__':
    import io, os
    # The name of the image file to annotate
    file_name = os.path.abspath('./temp/スクショ.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image_to_text(content)
