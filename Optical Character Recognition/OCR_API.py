import json
import cv2
import requests
import sys
import os


class kakao_API(object):
    
    def __init__(self, path):
        self.result = self.main(path)
        
    # image preprocessing(resize)
    def kakao_ocr_resize(self, image_path):
        LIMIT_PX = 1024
        
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        if LIMIT_PX < height or LIMIT_PX < width:
            ratio = float(LIMIT_PX) / max(height, width)        
            image = cv2.resize(image, None, fx=ratio, fy=ratio)

            height, width, _ = height, width, _ = image.shape   
            return image

        return image

    # kakao api 
    def kakao_ocr(self, image_value, appkey):
    
        API_URL = "https://dapi.kakao.com/v2/vision/text/ocr"
        headers = {"Authorization": "KakaoAK {}".format(appkey)}
    
        jpeg_image = cv2.imencode(".jpg", image_value)[1]  
        data = jpeg_image.tobytes()

        # OCR API 호출 결과값 나오기
        return requests.post(API_URL, headers=headers, files={"image": data}) 
    
    # 전체 main 함수
    def main(self, path):
        '''
        if len(sys.argv) != 3:
            print("Please run with args: $ python example.py /path/to/image appkey")
        image_path, appkey = sys.argv[1], sys.argv[2]
        '''

        # 현재는 해당 코드가 잘 돌아가는지 확인하기 위해 path, appkey는 직접 정의
        image_path = path
        appkey = "85f365cc3daf7b22c8514f9ab0bce3fe"

        # 전처리 진행
        image_value = self.kakao_ocr_resize(image_path)
        
        # Kakao API 불러와서 OCR 진행
        output = self.kakao_ocr(image_value, appkey).json()

        #아스키코드 해제 => 한국어 나옴(True할 경우 한국어 나옴)
        outputdata = json.dumps(output, ensure_ascii=False,sort_keys=True, indent=2)

        # array 결과로 변환
        outputdata = json.loads(outputdata)
        
            # 추가 코드(인식이 여러개 될 경우를 나눠서 
        if outputdata['result'] == 1:
            total_OCR_inf = outputdata['result'][0]['recognition_words'][0]
        else: 
            total_OCR_inf = ''
            for data in outputdata['result']:
                OCR_inf = data['recognition_words'][0]
                    total_OCR_inf = total_OCR_inf + ' ' + OCR_inf
        
        return total_OCR_inf