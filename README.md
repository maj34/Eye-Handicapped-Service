# Eye-Handicapped-Service
시각장애인을 위한 안내見 서비스

<br/>

## 1. 배경 & 목적

- 실시간 카메라 송출을 통한 이미지 인식 및 음성 안내 모델 제작
- 사용자가 질문을 하여 정보를 요청할 경우 자동으로 답변해주는 서비스를 추가해 논문 작성 중
- Journal of KIISE, JOK 논문지에 2023년 2월 발간 예정

<br/>

## 2. 주최/주관 & 팀원

- 주최/주관: AI빅데이터융합경영학과 인공지능 학회 X:AI
- 팀원: 전공생 총 3명

<br/>

## 3. 프로젝트 기간

- 2022.07. ~ 2022.11. (5개월)

<br/>

## 4. 프로젝트 소개

<img src='https://user-images.githubusercontent.com/75362328/212482000-1254df9f-eca4-4713-a76b-8f5c2f1db98b.png' width='100%' height='80%'>

&nbsp;&nbsp;&nbsp;&nbsp; 사회적 약자를 위한 ‘**Social Impact 프로젝트**’를 만들어 보고자 하는 취지에서 본 프로젝트를 시작하였다. 단순한 삶의 편의 개선도 좋지만 필수적으로 AI가 필요한 곳에 기술이 쓰이면 좋을 것이라고 판단했기 때문이다. 기존 시각장애인들을 위한 안내犬은 간단한 길 안내와 위험물 탐지만이 가능하다는 단점이 있었다. 따라서 시각장애인에게 눈이 되어 주자는 목표로 개 견(犬)이 아닌 볼 견(見)을 써서 **‘시각장애인을 위한 안내見 서비스’를 제작**하였다.

&nbsp;&nbsp;&nbsp;&nbsp; Input으로 길거리 이미지 정보가 전달되면 자동차, 자전거, 사람 등 **총 29가지 장애물에 대해 Object Detection을 통한 객체 탐지**를 하게 된다. Object Detection은 Bipartite Matching과 Transformer를 사용해 큰 성능 향상을 냈던 **Facebook AI Research Team의 DETR을 모델을 사용**했다.

&nbsp;&nbsp;&nbsp;&nbsp; 장애물은 사람(1개), 차량류(6개), 기둥류(4개), 안내류(4개), 기타(14개)로 나누어 그중 안내류에 포함되는 **안내판, 바리케이드, 버스/택시 정류장, 교통 표지판 5가지 라벨**에 대해서는 글귀를 탐지해 주기 위해 **OCR을 활용한 추가 Text 정보를 수집**했다. OCR은 Naver Clova AI Team에서 2019년에 발표한 **TRBA를 사용**했는데, 이는 **TPS-ResNet-BiLSTM-Attnd**의 약자로 최적의 모듈 조합을 제안한 모델이다. 그 후 각각의 물체가 몇 개 있는지, 안내판에는 무엇이라고 쓰여 있는지 출력해 알려주도록 **후처리를 해서 문장**을 만들어 주게 된다. 

&nbsp;&nbsp;&nbsp;&nbsp; 이를 사용자에게 송출하기 위해 간단한 파이썬 코드로 앱을 만들 수 있는 **Streamlit이라는 플랫폼을 사용해 웹/앱으로 송출**했다. 텍스트를 소리로 바꾸어 송출할 때는 여러 API를 실험한 결과 가장 성능이 좋았던 오픈소스인 **Google의 gTTS를 가지고 와서 사용**하였다. 결과적으로 질문을 하지 않아도 실시간으로 상황을 알려줄 수 있는 서비스를 제공할 수 있었으며 현재는 **STT, Image Captioning, VQA**를 사용해 **사용자가 질문을 했을 때 자동으로 답변**해 주는 서비스도 추가하여 논문을 작성 중이다.

<br/>

## 5. 프로젝트 담당 역할

- 길거리 데이터 셋 구축 및 전처리 & 후처리
- DETR 모델 학습 및 최적화
    - MMDetection, Detectron2, TIMM 등의 Object Detection 라이브러리 실험
- BAN-KVQA 모델 학습 및  최적화 & 새로운 Inference 코드 제작
- Streamlit 웹 제작 및 5가지 모델 (Object Detection, VQA, OCR, NER, TTS) 연동

<br/>

## 6. 발표 자료

[시각장애인을 위한 안내견 서비스 발표 자료](https://drive.google.com/file/d/1LucNwGaHszsWa-NIxNpl8cFeIRABim0f/view)  
