# JOB4

<br>

### Team명 : 싹(SSAC) 가능

### 구성원 : 김서린, 안나현, 엄민정, 주민기, 조솔하  

#### Directory  

- documents : 프로젝트 관련 문서 모음 디렉터리  
- rhea : 프론트엔드 원본 템플릿 디렉터리  
- job4 : 장고 프로젝트  
- crawling : 크롤링 소스 및 전처리 소스

<br>

## 배포  

- AWS EC2 Public DNS : <http://ec2-3-36-240-12.ap-northeast-2.compute.amazonaws.com/>  
- 웹 서버 : nginx  

<br>

## 프로젝트 개요
1. 주제 : 취업 정보 처리 및 제공  

2. 목적 : 취준생들의 자소서, 면접 준비를 돕기 위해 기업/직무 정보를 컴팩트하게 제공  

3. 기간 : 2021.03.26 ~ 2021.04.15  

4. 대상 : 취준생  

5. 기능  
    - 사용자 인증 기능 : 로그인, 회원가입, 북마크 등  
    - 합격자소서 분석 및 사용자의 자소서 분석 : 키워드 분석, 평점 예측  
        - 배치형 수집 프로그램  
        - 텍스트 데이터 전처리  
        - 파이프라인 : 수집 프로그램 -> 모델 학습  
    - 직무별 채용공고 분석 (미완)  
    - 기업 이슈 분석 (미완)  

<br>


## 사용 기술

- Django, JQuery, MySQL, Flume, HDFS, Spark  
- python library : job4/requirements.txt  

<br>


## 구성 페이지  
![index-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fddz1Xk%2Fbtq2EUR5EpA%2FZk97xecvJwVzFntOxh6BH1%2Fimg.png)

![bookmark-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXobmZ%2Fbtq2JkhvMXP%2FCFVQhBH7ExQkaYTWTijuL1%2Fimg.png)

![letter-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FO3R28%2Fbtq2EhfNut9%2FHw2PbHqDRkwsF06cq1ED4K%2Fimg.png)

![letter-02](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbzE1pH%2Fbtq2GWviACf%2F0Oq0wmx4KbYkOY5tc6M00K%2Fimg.png)

![analyze-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcg3b0H%2Fbtq2D23UnGH%2FOUqo87fsiovfelhCzULQz0%2Fimg.png)

![analyze-02](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcbNtgL%2Fbtq2CWXlEuh%2FegchYTF7dOMrETPwjNnvF0%2Fimg.png)

![analyze-03](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FZ4D02%2Fbtq2ILNbwsN%2Fv7HRLvUYSxch2ZKgBDJCZK%2Fimg.png)

![mypage-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlPsMJ%2Fbtq2HPoSQWZ%2FiTpQbx9qSIktvekijce1sK%2Fimg.png)

![mypage-02](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F0D7YI%2Fbtq2IPWhtQc%2FZc9GZk0mDSMC55VDN2JnXK%2Fimg.png)

![login-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F8kZJm%2Fbtq2HwXsnMf%2Fc5YBlybhNdysfEkKemz5s0%2Fimg.png)

![register-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fc5kvUs%2Fbtq2EU5yoBO%2FXjJicDNwVRSPVYB1voE5Y0%2Fimg.png)

![idrecover-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbGt4e7%2Fbtq2HPWLgxH%2F6G5kHIQiGl0QbneJtfNTP1%2Fimg.png)

![pwrecover-01](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FMOFXd%2Fbtq2HyHJyUw%2FH1IAkQnR3tOioG9wolUgI0%2Fimg.png)

<br>
