import requests
import json

class PlateClient:
    def __init__(self, url:str):
        self.url = url

    def read_number(self, img_id: int) -> str:
        # img = requests.get(f'http://51.250.83.169:7878/images/<int:{img_id}>')
        try:
            res = requests.get(f'{self.url}/readId/{img_id}',
                # headers={'Content-Type':'application/x-www-form-urlcoded'},
            )
            return res.json()['name']
        except KeyError:
            print('No file with that ID, please, try another ID')
        except json.decoder.JSONDecodeError:
            print('Invalid request, please, pass the ID of image')

    def read_numbers(self, img_ids: list) -> list:
        params = '?'
        for img_id in img_ids:
            params += f'img_id={img_id}&'
        params = params[:-1]
        try:
            res = requests.get(f'{self.url}/readSomeIds{params}')
            return res.json()['names']
        except KeyError:
            print('No file with that ID, please, try another ID')
        except json.decoder.JSONDecodeError:
            print('Invalid request, please, pass the ID of image')


if __name__ == '__main__':
    client = PlateClient('http://0.0.0.0:8080')
    result = client.read_number('10022')
    print(result)
    result = client.read_numbers([10022, 9965])
    print(result)