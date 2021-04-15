from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from myauth.models import Letter2, Company2, Task2
from django.core import serializers
import json
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import KeyedVectors
from konlpy.tag import Okt
import numpy as np
import operator
from urllib.parse import quote_plus
import requests
import lxml.html
tagger = Okt()

# Create your views here.
class ResultView(View):
    # template_name = 'letter/index.html'
    def post(self, request):

        company_id = request.POST['company_id']
        task_id =  request.POST['task_id']

        # 데이터 조회 코드 작성

        filtered_company_letter2 = Letter2.objects.filter(company = company_id)

        filtered_company = Company2.objects.filter(company_id = company_id)
        company_name = filtered_company[0].name
        
        result = []
        for letter in filtered_company_letter2:
            result.append( letter.question )
            result.append( letter.answer )
        
        def get_noun(text):
            nouns = tagger.nouns(text)
            return [n for n in nouns if len(n) > 1]  # 2글자 이상인 명사만 추출

        file = open(r"C:\job4(민) (2)\letter\stopwords.txt", "r", encoding='utf-8')
        stopwords = []
        while True:
            line = file.readline()
            if not line:
                break
            stopwords.append(line)

        file.close()

        stopwords = [w.replace('\n', '') for w in stopwords]

        cv = CountVectorizer(tokenizer=get_noun, max_features=100)
        tdm = cv.fit_transform(result)
        words = cv.get_feature_names()
        count_mat = tdm.sum(axis=0)
        count = np.squeeze(np.asarray(count_mat))

        result = []
        for w in words:
            if w not in stopwords:
                result.append(w)

        word_count = list(zip(result, count))
        word_count = sorted(word_count, key=operator.itemgetter(1), reverse=True)
        
        # loaded_model = KeyedVectors.load_word2vec_format("result.bin", binary=True) # 모델 로드
        # loaded_model.most_similar(positive=["가장"], topn=10) # 유사 키워드 추천 알고리즘

        # 템플릿에서 읽을 수 있도록 조회된 데이터를 저장하는 코드 작성2

        filtered_task = Task2.objects.filter(task_id = task_id)
        task_name = filtered_task[0].name

        filtered_task_letter2 = Letter2.objects.filter(task = task_id)
        result2 = []
        for letter in filtered_task_letter2:
            result2.append( letter.question )
            result2.append( letter.answer )
        
        cv2 = CountVectorizer(tokenizer=get_noun, max_features=100)
        tdm2 = cv2.fit_transform(result2)
        words2 = cv2.get_feature_names()
        count_mat2 = tdm2.sum(axis=0)
        count2 = np.squeeze(np.asarray(count_mat2))

        result3 = []
        for w in words2:
            if w not in stopwords:
                result3.append(w)

        word_count2 = list(zip(result3, count2))
        word_count2 = sorted(word_count2, key=operator.itemgetter(1), reverse=True)

        # print( word_count[:10] , word_count2[:10])
        
        # loaded_model = KeyedVectors.load_word2vec_format("result.bin", binary=True) # 모델 로드
        # loaded_model.most_similar(positive=["가장"], topn=10) # 유사 키워드 추천 알고리즘

        # 해당 자소서만 뽑기
        filtered_task_letter3 = Letter2.objects.filter(task = task_id, company = company_id)
        questions_answers = []
        
        for letter in filtered_task_letter3:
            questions_answers.append( (letter.question, letter.answer ) )

        return render(request, 'letter/index.html', {"company_name": company_name, "task_name": task_name, "word_count": word_count[:10], "word_count2": word_count2[:10], "questions_answers": questions_answers })
       
class AnalyzeView(TemplateView):
    template_name = 'letter/analyze.html'

class ShowCompany(View):
    def get(self, request):
        click_number = request.GET['key']
        print(click_number)

        from gensim.models import KeyedVectors

        loaded_model = KeyedVectors.load_word2vec_format("letter/sample.bin", binary=True) # 모델 로드
        # print(loaded_model.most_similar(positive=[click_number], topn=10)) # 유사 키워드 추천 알고리즘

        keyword = loaded_model.most_similar(positive=[click_number], topn=5)

        json_keyword = json.dumps(keyword)
        # serialized_keyword = serializers.serialize('json', keyword)

        return HttpResponse(json_keyword, content_type="application/json")


        # return render(request, 'letter/index.html', {"keyword":keyword})
class ShowTask(View):
    def get(self, request):
        click_number = request.GET['key']
        print(click_number)
    
        from gensim.models import KeyedVectors

        loaded_model = KeyedVectors.load_word2vec_format("letter/sample.bin", binary=True) # 모델 로드
        # print(loaded_model.most_similar(positive=[click_number], topn=10)) # 유사 키워드 추천 알고리즘

        keyword = loaded_model.most_similar(positive=[click_number], topn=5)

        json_keyword = json.dumps(keyword)
        # serialized_keyword = serializers.serialize('json', keyword)

        return HttpResponse(json_keyword, content_type="application/json")

class NewsView(View):
    template_name = 'letter/news.html'
    # def post(self, request):

    #     company_id = request.POST['company_id']
    #     task_id =  request.POST['task_id']

    #     # 데이터 조회 코드 작성

    #     filtered_company_letter2 = Letter2.objects.filter(company = company_id)

    #     filtered_company = Company2.objects.filter(company_id = company_id)
    #     company_name = filtered_company[0].name
        
    #     query = company_name
    #     url = 'http://search.daum.net/search?w=news&cluster=n&sort=recency&DA=PGD&q={query}&p={page}'
    #     articles = []
    #     for page in range(1, 20):
    #         search_url = url.format(query=query, page=page)
    #         res = requests.get(search_url)
    #         root = lxml.html.fromstring(res.text)
    #         for link in root.cssselect('a.f_nb'):  # 링크 추출
    #             news = requests.get(link.attrib['href'])
    #             news_root = lxml.html.fromstring(news.text)
    #             try:  # 일단 시도를 해본다
    #                 article = news_root.cssselect('section')[0]  # 본문 추출
    #                 text = article.text_content()
    #                 articles.append(text)
    #             except IndexError:  # IndexError가 발생할 경우
    #                 pass  # 아무 일도 하지 않고 넘어간다

    #     def get_noun(text):
    #         nouns = tagger.nouns(text)
    #         return [n for n in nouns if len(n) > 1]  # 2글자 이상인 명사만 추출

    #     cv = CountVectorizer(tokenizer=get_noun, max_features=100)
    #     tdm = cv.fit_transform(articles)
    #     words = cv.get_feature_names()
    #     count_mat = tdm.sum(axis=0)
    #     count = numpy.squeeze(numpy.asarray(count_mat))
    #     word_count = list(zip(words, count))
    #     word_count = sorted(word_count, key=operator.itemgetter(1), reverse=True)
    

    #     return render(request, 'letter/news.html', {"company_name": company_name, "word_count": word_count[:10]})