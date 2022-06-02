### main_script.py
  - 사용자가 터미널에서 입력한 arguments에 따라 왜곡된 영상을 만드는 기능
  - method 종류로 (glitchify, down up scale, frame drop) 등이 있고 각 method 별 intensity를 float으로 입력할 수 있음
  - usage example : python main_script.py --method 'scale' --fr 0.8 --rr 0.2
 
### down_up_scale.py
  - 원리 : 이미지를 resize하였다가 다시 복원하면 품질이 복원되지 않고 감소함. 이를 비디오로 확장
  - resize ratio : 얼마나 resize 시켰다가 복원할 것인가 (작을수록 큰 왜곡 발생)
  - frame ratio : 전체 비디오에서 왜곡을 적용할 frame 비율 (높을수록 큰 왜곡 발생)
  - 원본
    - 어쩌다보니 뉴스내용인데 특정 정치성향을 절대 내포한 작업이 아닙니다
  - 왜곡적용
 
### glitchify.py
  - 원리 : bite stream으로 읽어서 랜덤한 특정구간을 선택하여 랜덤 값으로 바꾼다 (깨진듯한 효과를 얻을 수 있음) 
  - 원본
  - 왜곡적용
