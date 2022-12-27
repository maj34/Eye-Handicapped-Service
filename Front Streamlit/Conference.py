import cv2
import streamlit as st

import torch
import mmcv
import datetime
import tempfile

import numpy as np
from numpy import asarray

from gtts import gTTS
from IPython.display import Audio
from IPython.display import display

from PIL import Image
from mmdet.apis import (inference_detector, show_result_pyplot)

from Object_Detection import object_detection
from OCR import ocr

# 표지 및 사이드바 꾸미기
head = '<p style="font-family:fantasy; color:crimson; font-size: 60px;">DNA BIGDATA CONFERENCE</p>'
st.markdown(head, unsafe_allow_html=True)

st.title('시각장애인을 위한 안내見 서비스')

personal_selected = st.sidebar.selectbox(
    "Input Image Formation", 
    ('Real-Time', 'Saved', 'Video')
)

st.sidebar.write('Selected: ', personal_selected)

# torch : 1.13.0, cuda : 11.6, nvidia : 512.78
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = torch.load('./model_pt/Faster-RCNN_0.3116.pt')  

if personal_selected == "Real-Time" :
    # 실시간 사진 찍기
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)        
        
        # Object Detection 결과 이미지 출력
        image = Image.open(picture)        
        img = asarray(image)
    
        # 후처리 문장 만들어주기
        object_text, object_list, cut_list = object_detection(img)
        ocr_text = ocr(object_list, cut_list)
        text = object_text + ocr_text
                
        # 문장 결과 오디오로 출력하기
        tts = gTTS(text, lang="ko")
        tts.save("sample_audio.mp3")

        audio_file = open('sample_audio.mp3', 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/mp3')


elif personal_selected == "Saved" :
    # 이미지 업로드
    upload_file = st.file_uploader('Select an Image', type='jpg')
    
    if upload_file is not None:
        image = Image.open(f'./image/{upload_file.name}')
        st.image(image, caption='The image file has been uploaded.')
        img = asarray(image)
        
        # 후처리 문장 만들어주기
        object_text, object_list, cut_list = object_detection(img)
        ocr_text = ocr(object_list, cut_list)
        text = object_text + ocr_text
        
        # 문장 결과 오디오로 출력하기
        tts = gTTS(text, lang="ko")
        tts.save("sample_audio.mp3")

        audio_file = open('sample_audio.mp3', 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/mp3')
    
    
elif personal_selected == "Video" :
    # 비디오 업로드
    uploaded_video = st.file_uploader("Choose video", type=["mp4", "mov"])
    
    if uploaded_video is not None: 
        video_file = open(f'./video/{uploaded_video.name}', 'rb')
        video_bytes = video_file.read()
        
        st.video(video_bytes)
        
        # 이미지 캡쳐
        capture = cv2.VideoCapture(uploaded_video.name)
        ret, frame = capture.read()
        
        now = datetime.datetime.now().strftime("%d_%H-%M-%S")
        key = cv2.waitKey(33)
        
        if st.button('캡처할 버튼'):
            st.write("캡쳐")
            st.image(frame)
            # frame.save(f'./{str(now)}.png')
            cv2.imwrite("./" + str(now) + ".png", frame)
        
        capture.release()
        cv2.destroyAllWindows()
    
        # 문장 결과 오디오로 출력하기
        text = ""
        tts = gTTS(text, lang="ko")
        tts.save("sample_audio.mp3")

        audio_file = open('sample_audio.mp3', 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/mp3')

    