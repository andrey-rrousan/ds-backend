from flask import Flask, request
from models.plate_reader import PlateReader
import requests
import logging
from PIL import UnidentifiedImageError, Image
import io


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


def img_to_plate(img):
    try:
        result = plate_reader.read_text(img)
    except UnidentifiedImageError:
        return {'error': 'No such ID in the database, please check the passed image ID.'}, 400
    return {'name':result}

# /readNumber <- img bin
# {'name':a}
@app.route('/readNumber', methods=['POST'])
def read_number():
    body = request.get_data()
    im = io.BytesIO(body)
    return img_to_plate(im)


@app.route('/health')
def health():
    return {'result':True}


@app.route('/readId/<int:img_id>')
def read_from_id(img_id):
    img_byte = requests.get(f'http://51.250.83.169:7878/images/{img_id}')
    img = io.BytesIO(img_byte.content)
    return img_to_plate(img)

@app.route('/readSomeIds/')
def read_multiple_id():
    multiple_ids = request.args.getlist('img_id')
    result = []
    for img_id in multiple_ids:
        try:
            res = read_from_id(img_id)
            result.append(res['name'])
        except TypeError:
            return {'error': 'No such ID in the database, please check the passed image ID.'}, 400
    return {
        'names': result
    }



if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
