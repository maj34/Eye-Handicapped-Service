import cv2
from matplotlib import pyplot as plt

import torch
import pandas as pd
import streamlit as st

import mmcv
from mmdet.apis import (inference_detector, show_result_pyplot)
from PIL import Image

def object_detection(img):
    
    model = torch.load('./model_pt/faster-rcnn_model_0.44.pt')

    result = inference_detector(model, img)
    show_result_pyplot(model, img, result)

    # threshold 기준 0.3 이상인 물체 걸러주기, ocr 모델 돌릴 리스트 저장
    class_number = []
    result_list = []
    ocr_list = []
    for i, j in enumerate(result):
        if len(j) != 0:
            for k in j:
                if k[-1] > 0.3:
                    class_number.append(i)
                    if i in [0, 6, 10, 12]:
                        result_list.append(k)
                        ocr_list.append(i)
                    
    unique_list = pd.Series(class_number).unique().tolist()
    label_list = ['바리케이드', '자전거', '볼라드', '버스', '차', '오토바이', '이동 안내판', '사람',
                    '기둥', '스쿠터', '정류장', '신호등', '교통 표지판', '나무', '트럭']
    unit_list = ['개', '대', '개', '대', '대', '대', '개', '명', '개', '대', '개', '개', '개', '그루', '대']

    # 탐지된 물체 출력
    object_list = []
    for i in unique_list:
        object_list.append(label_list[i]+' '+str(class_number.count(i))+unit_list[i])
    
    # 이미지 잘라주기
    cut_list = []
    for i, j in enumerate(result_list):
        cut = img[int(j[1]):int(j[3]),int(j[0]):int(j[2])]
        cut = cv2.cvtColor(cut, cv2.COLOR_BGR2RGB)  # numpy array        
        cut_img = Image.fromarray(cut) # NumPy array to PIL image
        cut_img.save(f'./image/sample_{i}.jpg','JPEG')
        cut_list.append(f'./image/sample_{i}.jpg')
    
    # 텍스트 출력
    object_text = '앞에 ' + ', '.join(object_list) + '가 탐지되었습니다.'
    st.write(object_text)
    
    # ocr_list : 인텍스 : 교통 표지판
    # cut_list : ./image/sample_0.jpg 
    return object_text, ocr_list, cut_list  