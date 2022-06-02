- 학습된 regressor와 scaler를 갖고 사용자가 입력한 비디오 경로에 구간별 점수를 반환하는 코드 입니다
- 비디오 하나를 입력받아서 특정 구간별로 split 한후 구간별 multiprocess를 이용하여 피쳐 추출, 점수 예측까지 진행합니다
  - 공유자원으로 multiprocessing.Manager().Queue() 를 이용하며, 딕셔너리로 append 하여 최종적으로 구간별 점수가 매칭된 딕셔너리를 반환합니다
 - 다음은 10초짜리 비디오의 경로(video path)를 2초마다 점수를 측정하고 싶은경우의 상황입니다
 ![image](https://user-images.githubusercontent.com/69031537/171541283-095ad04a-0fcf-427f-8314-672dc51ebaf5.png)
