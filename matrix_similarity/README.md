VQA 작업에서 가장 기초는 영상에서 피쳐들을 뽑아내는 것.

- 최초 사용 방식 : RAPIQUE 논문 코드의 matlab 방식
  - paper : https://arxiv.org/pdf/2101.10955v2.pdf
- 하지만 회사 사정상 matlab 사용이 어려워 python으로 converting 해야하였음
- python으로 converting 이후 성능상에 무결성이 유지되어야 함
  - 이를 체크해보고자 두 방법을 통해 뽑힌 피쳐 사이의 유사도를 체크해보고자 하였음
  - method_similarity.py
   - euclidean, hamming, manhattan, cos 등 다양한 방법들을 모아놓은 함수
  - calucate_similarity.py
   - 위 방법들을 import 하여 실제 서로 비교하는 코드 

### 결과
![image](https://user-images.githubusercontent.com/69031537/171533899-abadfbdd-bf02-4e7d-94c9-13cd294eb693.png)
- 하지만 수치상으로는 의미를 체감하기 어려워서 각 방법으로 직접 성능을 도출해보고 비교하는 방식으로 변경하였음
- 두가지 방법에서 최종 성능 상 별 차이가 없어서 python converting 방법을 끝까지 가져갈 수 있게 됨
