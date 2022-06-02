### main_script.py
  - 사용자가 터미널에서 입력한 arguments에 따라 왜곡된 영상을 만드는 기능
  - method 종류로 (glitchify, down up scale, frame drop) 등이 있고 각 method 별 intensity를 float으로 입력할 수 있음
  - usage example : python main_script.py --method 'scale' --fr 0.8 --rr 0.2
 
### down_up_scale.py
  - 원리 : 이미지를 resize하였다가 다시 복원하면 품질이 복원되지 않고 감소함. 이를 비디오로 확장
  - resize ratio : 얼마나 resize 시켰다가 복원할 것인가 (작을수록 큰 왜곡 발생)
  - frame ratio : 전체 비디오에서 왜곡을 적용할 frame 비율 (높을수록 큰 왜곡 발생)
  - 원본
    - ![resized_intensity_1](https://user-images.githubusercontent.com/69031537/171537426-9ed6a710-108d-4b81-9db1-f72fdaa99253.png)
    - 어쩌다보니 뉴스내용인데 특정 정치성향을 절대 내포한 작업이 아닙니다
  - 왜곡적용
    - ![resized_intensity_5](https://user-images.githubusercontent.com/69031537/171537475-3899fd87-3ab6-4119-b57a-fbb7204f9249.png)
 
### glitchify.py
  - 원리 : bite stream으로 읽어서 랜덤한 특정구간을 선택하여 랜덤 값으로 바꾼다 (깨진듯한 효과를 얻을 수 있음) 
  - 원본
    - ![glitched_intensity_20](https://user-images.githubusercontent.com/69031537/171537523-dfdf3956-9104-4edf-82fa-f749d0df6dd8.png)
  - 왜곡적용
    - ![glitched_intensity_100](https://user-images.githubusercontent.com/69031537/171537546-10d54d3a-2aa8-4364-b3aa-a3f10de41d57.png)
