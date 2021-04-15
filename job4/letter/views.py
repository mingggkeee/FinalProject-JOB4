from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# result view packages
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

        # 존재하지 않는 단어에 대해 예외처리 필요

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

        file = open("letter/stopwords.txt", "r", encoding='utf-8')
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
        filtered_task_letter3 = Letter2.objects.filter(task=task_id, company=company_id)
        questions_answers = []

        for letter in filtered_task_letter3:
            questions_answers.append((letter.question, letter.answer, letter.letter_id))

        return render(request, 'letter/index.html',
                      {"company_name": company_name, "task_name": task_name, "word_count": word_count[:10],
                       "word_count2": word_count2[:10], "questions_answers": questions_answers})


class AnalyzeView(TemplateView):
    template_name = 'letter/analyze.html'


class AnalyzeRequestView(View):

    def __init__(self):
        self.gb_accuracy = -1
        self.rating_accuracy = -1

    def get_model_info(self, gb_model, r_model):
        import pickle

        if self.gb_accuracy == -1:
            with open("letter/gb_softmax_test_x.pkl", "rb") as f:
                gb_test_x = pickle.load(f)
            with open("letter/gb_softmax_test_y.pkl", "rb") as f:
                gb_test_y = pickle.load(f)
            gb_result = gb_model.evaluate(gb_test_x, gb_test_y)
            self.gb_accuracy = gb_result[1]

        if self.rating_accuracy == -1:
            with open("letter/rating_test_x.pkl", "rb") as f:
                rating_test_x = pickle.load(f)
            with open("letter/rating_test_y.pkl", "rb") as f:
                rating_test_y = pickle.load(f)
            rating_result = r_model.evaluate(rating_test_x, rating_test_y)
            self.rating_accuracy = rating_result[1]

        return (self.gb_accuracy, self.rating_accuracy)

    def get(self, request):
        if request.method == 'GET':
            content = request.GET['letter-area']

            user_letter_input = [content.split()]

            from keras.models import load_model
            import pickle
            import numpy as np

            with open("letter/gb_evaluate_tk.pkl", "rb") as f:
                tokenizer = pickle.load(f)

            with open("letter/rating_tokenizer.pkl", "rb") as f:
                rating_tk = pickle.load(f)

            token_letter = tokenizer.texts_to_sequences(user_letter_input)
            tk_rating_letter = rating_tk.texts_to_sequences(user_letter_input)

            # gb_binary_model = load_model("letter/gb_evaluate_binary_model")
            gb_softmax_model = load_model("letter/gb_evaluate_model")
            rating_model = load_model("letter/rating_evaluate_model")

            # vectorize
            def vectorize(sequences, dimension=10000):
                results = np.zeros((len(sequences), dimension))
                for i, seq in enumerate(sequences):
                    results[i, seq] = 1.
                return results

            vector_letter = vectorize(token_letter)
            vector_rating_letter = vectorize(tk_rating_letter)

            prediction = gb_softmax_model.predict(vector_letter)
            rating_prediction = rating_model.predict(vector_rating_letter)

            # evaluate 결과를 전달해야함
            gb_acc, r_acc = self.get_model_info(gb_softmax_model, rating_model)

            context = {'result': {'bad': str(prediction[0][0]),
                                  'good': str(prediction[0][1]),
                                  'gb_result': int(np.argmax(prediction[0])),
                                  'analyze_done': True,
                                  'content': content,
                                  'rating_result': float(np.argmax(rating_prediction[0])),
                                  'gb_accuracy': str(gb_acc),
                                  'rating_accuracy': str(r_acc)
                                  }
                       }

            return render(request, "letter/analyze.html", context)

        return redirect("/")



class ShowCompany(View):
    def get(self, request):
        click_number = request.GET['key']
        print(click_number)

        from gensim.models import KeyedVectors

        loaded_model = KeyedVectors.load_word2vec_format("letter/sample.bin", binary=True)  # 모델 로드
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

        loaded_model = KeyedVectors.load_word2vec_format("letter/sample.bin", binary=True)  # 모델 로드
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
