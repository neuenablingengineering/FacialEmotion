#coding: utf-8

import requests
from json import JSONDecoder
import base64


class Video2:
    # load our serialized model from disk
    def run(self):
    
        filepath1 = 'cache.png'
        with open(filepath1, 'rb') as f:
            img_bytes = base64.b64encode(f.read())

        http_url_1 ="https://api-cn.faceplusplus.com/facepp/v3/detect"
        http_url_2 ="https://api-cn.faceplusplus.com/facepp/v3/face/analyze"
        key ="tV4oCkxjehao4vhLpaWp_x3mO_Iju6wa"
        secret ="_1wvIuKbheSsTRPEhdTaOqv7IKKmL1TI"

        data_1 = {"api_key":key, "api_secret": secret, "image_base64": img_bytes.decode('ascii')}


        response = requests.post(http_url_1, data=data_1)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        # print(req_dict)

        req_dict = str(req_dict)
        str_face_tokens = req_dict[req_dict.find("'face_token':")+len("'face_token':"):]
        str_face_tokens = str_face_tokens[str_face_tokens.find("'")+1:str_face_tokens.find("'}")]
        # print(str_face_tokens)
        data_2 = {"api_key":key, "api_secret": secret, "face_tokens": str_face_tokens , "return_attributes": "emotion"}
        response = requests.post(http_url_2, data=data_2)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        # print(req_dict)
        # print(req_dict['faces'][0]['attributes']['emotion']['sadness'])
        # print(req_dict['faces'][0]['attributes']['emotion']['neutral'])
        # print(req_dict['faces'][0]['attributes']['emotion']['disgust'])
        # print(req_dict['faces'][0]['attributes']['emotion']['anger'])
        # print(req_dict['faces'][0]['attributes']['emotion']['surprise'])
        # print(req_dict['faces'][0]['attributes']['emotion']['fear'])
        # print(req_dict['faces'][0]['attributes']['emotion']['happiness'])

        sadness = int(req_dict['faces'][0]['attributes']['emotion']['sadness'])
        neutral = int(req_dict['faces'][0]['attributes']['emotion']['neutral'])
        disgust = int(req_dict['faces'][0]['attributes']['emotion']['disgust'])
        anger = int(req_dict['faces'][0]['attributes']['emotion']['anger'])
        surprise = int(req_dict['faces'][0]['attributes']['emotion']['surprise'])
        fear = int(req_dict['faces'][0]['attributes']['emotion']['fear'])
        happiness = int(req_dict['faces'][0]['attributes']['emotion']['happiness'])
        result = max(sadness,neutral ,disgust,anger,surprise,fear,happiness)
        if result == sadness:
            result_str = 'Sad'
        elif result == neutral:
            result_str = 'Neutral'
        elif result == disgust:
            result_str = 'Disgust'
        elif result == anger:
            result_str = 'Anger'
        elif result == surprise:
            result_str = 'Surprise'
        elif result == fear:
            result_str = 'Fear'
        elif result == happiness:
            result_str = 'Happiness'
        else:
            result_str = ''
        return req_dict,result_str



