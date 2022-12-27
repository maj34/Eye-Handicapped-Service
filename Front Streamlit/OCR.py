import requests
import uuid
import time
import json

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st


def ocr(ocr_list, cut_list):
    api_url = 'https://5100xmdkj5.apigw.ntruss.com/custom/v1/19297/ea728840d371e1a556f51e57413fe891207a25c1f749b6f76fcf068f3e4dcadd/general'
    secret_key = 'dXJSRXppc1FmaWNvaElVTUxaSWVVUWZMbnF2QnRxZWM='
    
    ocr_text_list = []
    
    for i in cut_list:
        image_file = i
        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'out'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
        ('file', open(image_file,'rb'))
        ]
        headers = {
        'X-OCR-SECRET': secret_key
        }

        response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

        res = json.loads(response.text.encode('utf8'))
        
        global ocr_text
        ocr_text = ""
        for i in range(len(res['images'][0]['fields'])):
            ocr_text += res['images'][0]['fields'][i]['inferText']+" "
        
        
        label_list = ['바리케이드', '자전거', '볼라드', '버스', '차', '오토바이', '이동 안내판', '사람',
                    '기둥', '스쿠터', '정류장', '신호등', '교통 표지판', '나무', '트럭']
        
        # text의 길이가 0 초과인 경우만 출력
        if len(ocr_text) != 0:
            for i in ocr_list:
                ocr_text_list.append(label_list[i] + '에는 "' + ocr_text + '" 라고 적혀져 있습니다.') 

    ocr_text_list = ','.join(ocr_text_list)
    st.write(ocr_text_list)        
        
    return ocr_text_list