import json
import io
import binascii
import base64
from PIL import Image
import os
import argparse


class coco2labelme:
    def __init__(self, img_path, json_file='', save_path=''):
        self.img_path = img_path
        self.save_path = save_path
        self.json_file = json_file
        self.data3 = {'version': '5.0.1',
                      'flags': {},
                      'shapes': [{'label': '2',
                                  'points': [[539.099099099099, 836.9369369369368],
                                             [576.036036036036, 859.4594594594594],
                                             [635.4954954954954, 863.0630630630629],
                                             [711.1711711711711, 843.2432432432431],
                                             [763.4234234234233, 818.018018018018],
                                             [803.9639639639639, 808.108108108108],
                                             [723.0841121495326, 920.7943925233644],
                                             [599.7196261682243, 958.1775700934579],
                                             [574.4859813084112, 917.0560747663551]],
                                  'group_id': None,
                                  'shape_type': 'polygon',
                                  'flags': {}},
                                 {'label': '1',
                                  'points': [[589.4392523364486, 869.3925233644859],
                                             [618.4112149532709, 884.3457943925233],
                                             [632.4299065420561, 919.8598130841121],
                                             [632.4299065420561, 981.5420560747663],
                                             [651.1214953271027, 984.3457943925233],
                                             [645.5140186915887, 947.8971962616822],
                                             [640.841121495327, 902.1028037383177],
                                             [655.7943925233644, 869.3925233644859],
                                             [669.8130841121495, 848.8317757009345],
                                             [624.9532710280373, 859.1121495327102]],
                                  'group_id': None,
                                  'shape_type': 'polygon',
                                  'flags': {}}],
                      'imagePath': 'A0522_H-42_43.jpg',
                      'imageData': '',
                      'imageHeight': 1289,
                      'imageWidth': 1289}

    def img2ascii(self, path):
        image = Image.open(path).convert("RGB")
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        byte_data = img_bytes.getvalue()
        img_byte = binascii.b2a_base64(byte_data)

        return str(img_byte)[2:-3]

    def write_json(self):
        with open(self.json_file, 'r') as f:
            data2 = json.load(f)

        a1 = []
        for i in range(len(data2['annotations'])):
            label = data2['annotations'][i]['name']
            a2 = {}
            a2['label'] = label

            paths = data2['annotations'][i]['polygon']['paths']

            for j in range(len(paths)):
                a3 = []
                for k in range(len(paths[j])):
                    x = paths[j][k]['x']
                    y = paths[j][k]['y']
                    a3.append([x, y])
                a2['points'] = a3

            a2['group_id'] = None
            a2['shape_type'] = 'polygon'
            a2['flags'] = {}
            a1.append(a2)

        self.data3['shapes'] = a1
        self.data3['imagePath'] = data2['item']['name']
        self.data3['imageHeight'] = data2['item']['slots'][0]['height']
        self.data3['imageWidth'] = data2['item']['slots'][0]['width']
        self.data3['imageData'] = self.img2ascii(self.img_path)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        newfile = os.path.join(self.save_path, self.data3['imagePath'][:-4] + '.json')
        print(newfile)
        with open(newfile, 'w') as f:
            json.dump(self.data3, f)

        print('Done')


if __name__ == '__main__':
    paser = argparse.ArgumentParser(description='coco2labelme')
    paser.add_argument('--json-file', default='demo.json',
                       help='json file to be converted')

    paser.add_argument('--img-file', default='E066M_H138_01.jpg',
                       help='json file to be converted')

    paser.add_argument('--save-path', default='output',
                       help='save directory of new json file ')
    args = paser.parse_args()

    a = coco2labelme(img_path=args.img_file,
                     json_file=args.json_file,
                     save_path=args.save_path)
    a.write_json()

