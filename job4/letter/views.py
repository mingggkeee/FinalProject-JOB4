from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.http import HttpResponse

# Create your views here.
class ResultView(TemplateView):
    template_name = 'letter/index.html'

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

        return ( self.gb_accuracy, self.rating_accuracy )


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
