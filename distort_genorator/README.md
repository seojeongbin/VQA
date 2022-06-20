### main_script.py
  - 사용자가 터미널에서 입력한 arguments에 따라 왜곡된 영상을 만드는 기능
  - method 종류로 (glitchify, down up scale, frame drop) 등이 있고 각 method 별 intensity를 float으로 입력할 수 있음
  - usage example : python main_script.py --method 'scale' --fr 0.8 --rr 0.2

### frame_drop.py
  - 입력받은 비디오의 전체 프레임에서 drop frame 수 만큼 삭제 후, 삭제된 프레임의 직전 프레임으로 freeze된 영상을 생성하는 코드 (멈칫거리는, 버퍼링 같은 영상)
  - total_frames 에서 랜덤하게 지점을 택한 후, 이 지점에서 1~10 사이의 랜덤값만큼 프레임을 drop 시킴. 이 때 이렇게 drop 시키는 프레임 인덱스 값들을 all dropped indices에 저장
  - total frames 에서 dropped 된 프레임들을 제외하여 위의 과정을 반복
  - 이때, drop되는 프레임들을 겹치지 않게 하기위해 합집합 원리를 사용
  - 첫번째 장면이 drop 되는경우에는 표현할 프레임이 없으므로 0번째 프레임이 있는경우 
 
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
