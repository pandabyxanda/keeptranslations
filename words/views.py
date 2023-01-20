import random

import numpy
from django.contrib.auth import logout, login, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Window
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *
from .translations import make_google_translation

# Create your views here.

# def index(request, *args, **kwargs):
#     # return HttpResponse("main page yah")
#     from words.models import Words
#
#     print("ge")
#     # w1 = Words(word='Hello22')
#     # w1.save()
#     if request.GET:
#         print(request.GET)
#     return HttpResponse(f"<h1>MAIN</h1> <p>lol</p>")

# menu = ['Main page', 'About', 'Login']

menu = [{'title': 'Main page', 'url_name': 'home'},
        {'title': 'Saved', 'url_name': 'saved'},
        {'title': 'Learn', 'url_name': 'learn'},
        {'title': 'Test', 'url_name': 'test'},
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'},
        ]

last_word = {'word': None}
word_in_form1 = {'word': None}
words_to_learn = {'words': None, 'learning_rating': None, 'language': 'EN', 'words_to_test': None, 'incorrect_answer_response_tip': None}
answers_counter = {'questions': 0, 'correct_answers': 0, 'mistakes': 0}
amount_of_words_to_learn = {'number': 5}

LEARNING_RATING_DECREMENT = 1
LEARNING_RATING_INCREMENT = 2


# def index(request, *args, **kwargs):
#     return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})

def index(request, *args, **kwargs):
    current_user_name = get_user(request).username
    current_user_id = get_user(request).id
    print("")
    print(f"{get_user(request) = }")
    print(f"{current_user_name = }")
    print(f"{current_user_id = }")

    print(f"{request.method = }")
    print(f"{request.POST = }")
    print(f"{request.GET = }")

    # delete when all conditions are done
    form1 = WordTranslationForm()

    if request.method == 'GET':
        form1 = WordTranslationForm()

    if request.method == 'POST':
        if request.POST.get('word') and request.POST.get('do_translate'):
            last_word['word'] = request.POST.get('word')
            translation = make_google_translation(last_word['word'])['translatedText']
            form1 = WordTranslationForm({'word': last_word['word'], 'translation': translation})

        if request.POST.get('word') and request.POST.get('translation') and request.POST.get('do_save'):
            if current_user_id:
                last_word['word'] = request.POST.get('word').strip()
                last_word['translation'] = request.POST.get('translation').strip()
                if last_word['word'] != '' and last_word['translation'] != '':
                    similar_words = list(Words.objects.filter(word=last_word['word']))
                    if len(similar_words) == 0:
                        Words.objects.create(
                            word=last_word['word'],
                            translation=last_word['translation'],
                            user=get_user(request),
                        )
                    else:
                        Words.objects.filter(word=last_word['word']).update(translation=last_word['translation'])
                    form1 = WordTranslationForm({'word': last_word['word'], 'translation': last_word['translation']})

        if request.POST.get('change_word'):
            word = Words.objects.get(pk=int(request.POST.get('change_word')))
            last_word['word'] = word.word
            last_word['translation'] = word.translation
            form1 = WordTranslationForm({'word': last_word['word'], 'translation': last_word['translation']})

        if request.POST.get('delete_word'):
            Words.objects.filter(pk=request.POST.get('delete_word')).delete()

    words = Words.objects.filter(user__username=current_user_name).order_by('-pk')
    paginator = Paginator(words, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'title': menu[0]['title'],
        'form1': form1,
        'current_user_id': current_user_id,
        'page_obj': page_obj,
    }

    return render(request, 'words/index.html', context=context)




# class WordHome(ListView):
#     model = Words
#     template_name = 'words/index.html'

# class WordHome(CreateView):
#     form_class = AddWordsForm1
#     template_name = 'words/index.html'
#     success_url = reverse_lazy('home')
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = menu[0]['title']
#         context['menu'] = menu
#         return context


def saved(request, *args, **kwargs):
    # u1 = get_user(request).username

    # u = get_user(request.user.username)

    # print(f"{u1 = }")
    # print(f"{u = }")
    # words = Words.objects.order_by('-pk')

    # current_user_id = get_user(request).id
    # print(f"{current_user_id = }")
    current_user_name = get_user(request).username
    words = Words.objects.filter(user__username=current_user_name).order_by('-pk')

    # rWomen.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    paginator = Paginator(words, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'menu': menu,
        'title': menu[1]['title'],
        'page_obj': page_obj,
    }
    return render(request, 'words/saved.html', context=context)


def learn(request, *args, **kwargs):
    # u1 = get_user(request).username

    # u = get_user(request.user.username)

    # print(f"{u1 = }")
    # print(f"{u = }")
    # words = Words.objects.order_by('-pk')

    # current_user_id = get_user(request).id
    # print(f"{current_user_id = }")
    # form_input_number_of_words_to_learn = ChooseAmountOfWordsToLearn({'translation': 10})
    print("")
    print("func learn.")
    print(f"{request.method = }")
    print(f"{request = }")
    print(f"{request.POST = }")
    if request.POST:
        print(f"{request.POST['amount_of_words_to_learn'] = }")
        amount_of_words_to_learn['number'] = int(request.POST['amount_of_words_to_learn'])
        current_user_name = get_user(request).username

        pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=False).values_list('pk',
                                                                                                           flat=True)
        pk_list = list(pk_list)
        pk_list_random = random.sample(pk_list, k=amount_of_words_to_learn['number'])
        words = Words.objects.filter(pk__in=pk_list_random)
        words_to_learn['words'] = words
        words_to_learn['pk_list'] = pk_list_random

        print(f"{pk_list = }")
        print(f"{pk_list_random = }")
        # rWomen.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        paginator = Paginator(words_to_learn['words'], 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        if words_to_learn['words'] == None:
            page_obj = None
        else:
            paginator = Paginator(words_to_learn['words'], 100)
            page_obj = paginator.get_page(1)
    form_input_number_of_words_to_learn = ChooseAmountOfWordsToLearnForm(
        {'amount_of_words_to_learn': amount_of_words_to_learn['number']}
    )
    button_start_test_form = ButtonStartTestForm()

    context = {
        'menu': menu,
        'title': menu[2]['title'],
        'page_obj': page_obj,
        'form_input_number_of_words_to_learn': form_input_number_of_words_to_learn,
        'button_start_test_form': button_start_test_form,
    }
    # context = {
    #     'words': words,
    #     'menu': menu,
    #     'title': menu[0]['title'],
    #     'form1': form1,
    #     'form2': form2,
    #     'page_obj': page_obj,
    #     'current_user_id': current_user_id,
    #     'button_form': button_form,
    # }
    return render(request, 'words/learn.html', context=context)


def test(request, *args, **kwargs):
    print("")
    print(f"{request.method = }")
    print(f"{request.POST = }")
    print(f"{request.GET = }")

    # button_choose_answer_form = ButtonChooseAnswerForm()
    current_user_name = get_user(request).username
    number_of_words_to_test = 10
    button_choose_answer_form = ButtonChooseAnswerForm()
    if request.method == 'GET' or request.POST.get('add_words_to_test'):
        if request.POST.get('add_words_to_test'):
            words_to_learn['words'].update(learned=True)
        pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk',
                                                                                                          flat=True)
        pk_list = list(pk_list)
        if len(pk_list) < number_of_words_to_test:
            number_of_words_to_test = len(pk_list)
        pk_list_random = random.sample(pk_list, k=number_of_words_to_test)
        words = Words.objects.filter(pk__in=pk_list_random)
        # print(f"{pk_list_random = }")
        words = list(words)
        random.shuffle(words)
        words_to_learn['word to test'] = words[0]
        words_to_learn['learning_rating'] = words[0].learning_rating
        random.shuffle(words)
        words_to_learn['answers to choose'] = words
        words_to_learn['incorrect_answer_response_tip'] = None

    if request.method == 'POST':
        if request.POST.get('change_lang'):
            if words_to_learn['language'] == 'EN':
                words_to_learn['language'] = 'RU'
            else:
                words_to_learn['language'] = 'EN'

        # if request.POST.get('word') and request.POST.get('do_translate'):
        #     button_choose_answer_form = ButtonChooseAnswerForm()
        if request.POST.get('chosen_answer'):
            answers_counter['questions'] += 1
            if request.POST.get('chosen_answer') in \
                    (words_to_learn['word to test'].word, words_to_learn['word to test'].translation):
                # print("correct")

                answers_counter['correct_answers'] += 1
                if words_to_learn['learning_rating'] > 1 + LEARNING_RATING_DECREMENT:
                    words_to_learn['word to test'].learning_rating -= LEARNING_RATING_DECREMENT
                    words_to_learn['word to test'].save()
                #
                #     button_choose_answer_form = ButtonChooseAnswerForm()
                #     # pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk', flat=True)
                records = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk',
                                                                                                                  'learning_rating')
                #
                #     # print(f"{records = }")
                pk_list = [record[0] for record in records]
                learning_rating_list = [record[1] for record in records]
                #     # print(pk_list)
                #     # print(learning_rating_list)
                #
                #     # pk_list = list(pk_list)
                if len(pk_list) < number_of_words_to_test:
                    number_of_words_to_test = len(pk_list)
                #
                #
                #     # lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                #     # lst2 = [1, 3, 1, 1, 1, 1, 1, 1, 1, 1]
                rates_for_choose = [x / sum(learning_rating_list) for x in learning_rating_list]
                #     # print([round(x, 3) for x in rates_for_choose])
                pk_list_random = numpy.random.choice(pk_list, p=rates_for_choose, size=number_of_words_to_test,
                                                     replace=False)
                #     # print(f"{list(pk_list_random) = }")
                #
                #
                #
                #     # pk_list_random = random.sample(pk_list, k=number_of_words_to_test)
                words = Words.objects.filter(pk__in=pk_list_random)
                words = list(words)
                random.shuffle(words)

                word = words[0]
                for i in range(len(words)):
                    if words[i].learning_rating > word.learning_rating:
                        word = words[i]
                words_to_learn['word to test'] = word
                # words_to_learn['words to test'] = random.choice()
                # random.shuffle(words)
                words_to_learn['answers to choose'] = words
                words_to_learn['incorrect_answer_response_tip'] = None
            else:
                words_to_learn['word to test'].learning_rating += LEARNING_RATING_INCREMENT
                words_to_learn['word to test'].save()
            words_to_learn['learning_rating'] = words_to_learn['word to test'].learning_rating

        if request.POST.get('renew') == 'True':
            answers_counter['questions'] = 0
            answers_counter['correct_answers'] = 0




    number_of_all_rows_in_db = Words.objects.count()
    number_of_learned_words_in_db = Words.objects.filter(learned=True).count()
    number_of_words_with_good_rating = Words.objects.filter(learning_rating__lt=10).count()
    words_statistics = {
        'all': number_of_all_rows_in_db,
        'learned_words': number_of_learned_words_in_db,
        'words_with_good_rating': number_of_words_with_good_rating,
    }

    if words_to_learn['language'] == 'EN':
        word_to_test = words_to_learn['word to test'].word
        answers_to_choose = [x.translation for x in words_to_learn['answers to choose']]
    else:
        word_to_test = words_to_learn['word to test'].translation
        answers_to_choose = [x.word for x in words_to_learn['answers to choose']]

    answers_to_choose_rating = [x.learning_rating for x in words_to_learn['answers to choose']]
    print(f"{words_to_learn['language'] = }")
    print(f"{answers_to_choose_rating = }")

    context = {
        'menu': menu,
        'title': menu[3]['title'],
        'word_to_test': word_to_test,
        'answers_to_choose': answers_to_choose,
        # 'answers_to_choose_rating': answers_to_choose_rating,
        'button_choose_answer_form': button_choose_answer_form,
        # 'incorrect_answer_response_tip': words_to_learn['incorrect_answer_response_tip'],
        'answers_counter': answers_counter,
        # 'button_renew_answers_counter': button_renew_answers_counter,
        'words_statistics': words_statistics,
        'leaning_rating': words_to_learn['learning_rating'],
    }
    return render(request, 'words/test.html', context=context)



def about(request, *args, **kwargs):
    context = {
        'menu': menu,
        'title': menu[4]['title'],
    }
    return render(request, 'words/about.html', context=context)


# def login(request, *args, **kwargs):
#     context = {
#         'menu': menu,
#         'title': menu[-1]['title'],
#     }
#     return render(request, 'words/login.html', context=context)

# def register(request, *args, **kwargs):
#     context = {
#         'menu': menu,
#         'title': menu[-1]['title'],
#     }
#     return render(request, 'words/login.html', context=context)

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'words/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'words/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse_lazy('home')


# only if debug = True
def pageNotFound(request, exception):
    return redirect('home')
    # return HttpResponseNotFound("<h1>nah.. not found page</h1>"
    #                             "<hr>"
    #                             "<p>"
    #                             "<h1>stop experiments</h1>")


def logout_user(request):
    logout(request)
    return redirect('login')
