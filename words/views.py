import random

import numpy
from django.contrib.auth import logout, login, get_user
from django.contrib.sessions.models import Session
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

menu = [{'title': 'Main page', 'url_name': 'home'},
        {'title': 'Saved', 'url_name': 'saved'},
        {'title': 'Learn', 'url_name': 'learn'},
        {'title': 'Test', 'url_name': 'test'},
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'},
        ]

# last_word = {'word': None}
words_to_learn = {'words': None, 'learning_rating': None, 'language': 'EN', 'words_to_test': None,
                  'incorrect_answer_response_tip': None}
answers_counter = {'questions': 0, 'correct_answers': 0, 'mistakes': 0}

LEARNING_RATING_DECREMENT = 1
LEARNING_RATING_INCREMENT = 2
NUMBER_OF_WORDS_TO_TEST = 10


def get_user_and_session_id(request, *args, **kwargs):
    if request.session.session_key and User_And_Session.objects.filter(session=request.session.session_key).exists():
        user_and_session_record = User_And_Session.objects.get(session=request.session.session_key)
    else:
        print("no user_and_session object found, creating new")
        if request.user.is_authenticated:
            if User_And_Session.objects.filter(user=request.user).exists():
                # update table User_And_Session with session data
                User_And_Session.objects.filter(user=request.user).update(
                    session=Session.objects.get(session_key=request.session.session_key)
                )
                user_and_session_record = User_And_Session.objects.get(user=request.user)
            else:
                user_and_session_record = User_And_Session.objects.create(
                    user=User.objects.get(id=request.user.id),
                    session=Session.objects.get(session_key=request.session.session_key)
                )
            # print(f"{request.session.session_key =}")
            # print(f"{user_and_session = }")
        else:
            print(f"not authenticated")

            if not request.session.session_key:
                request.session.create()

            if not Session.objects.filter(session_key=request.session.session_key).exists():
                request.session.create()

            session_key = request.session.session_key
            # print(f"{session_key = }")

            if not User_And_Session.objects.filter(session=request.session.session_key).exists():
                user_and_session_record = User_And_Session.objects.create(
                    session=Session.objects.get(session_key=session_key))

            if User_And_Session.objects.filter(session=request.session.session_key).exists():
                user_and_session_record = User_And_Session.objects.get(session=request.session.session_key)

        # clear User_And_Session objects and words without users
        Words.objects.filter(
            user_and_session__in=User_And_Session.objects.filter(session=None).filter(user=None)).delete()
        User_And_Session.objects.filter(session=None).filter(user=None).delete()

    user_and_session_id = user_and_session_record.id
    print("")
    print(f"{user_and_session_id = }, {request.method = }")
    print(f"{user_and_session_record = }, {request.session.items() = }")
    return user_and_session_record, user_and_session_id


def index(request, *args, **kwargs):
    user_and_session, user_and_session_id = get_user_and_session_id(request)

    word = None
    translation = None
    form1 = None

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        if request.POST.get('do_translate'):
            word = request.POST.get('word').strip()
            if word:
                translation = make_google_translation(word)['translatedText'].strip()
        if request.POST.get('do_save'):
            if request.POST.get('word') and request.POST.get('translation'):
                word = request.POST.get('word')
                translation = request.POST.get('translation')
                if word != '' and translation != '':
                    similar_words = list(
                        Words.objects.filter(user_and_session__id=user_and_session_id).filter(
                            word=word))
                    if len(similar_words) == 0:
                        Words.objects.create(
                            word=word,
                            translation=translation,
                            user_and_session=user_and_session,
                        )
                    else:
                        Words.objects.filter(user_and_session__id=user_and_session_id).filter(word=word). \
                            update(translation=translation)

        if request.POST.get('change_word'):
            record = Words.objects.get(pk=int(request.POST.get('change_word')))
            word = record.word
            translation = record.translation

        if request.POST.get('delete_word'):
            Words.objects.filter(pk=request.POST.get('delete_word')).delete()
            word = request.session['last_word']['word']
            translation = request.session['last_word']['translation']

    words = Words.objects.filter(user_and_session=user_and_session).order_by('-pk')[:6]
    paginator = Paginator(words, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    form1 = WordTranslationForm({'word': word, 'translation': translation})

    request.session['last_word']['word'] = word
    request.session['last_word']['translation'] = translation
    request.session.save()
    context = {
        'menu': menu,
        'title': menu[0]['title'],
        'form1': form1,
        'page_obj': page_obj,
    }
    return render(request, 'words/index.html', context=context)


def saved(request, *args, **kwargs):
    user_and_session, user_and_session_id = get_user_and_session_id(request)

    words_records = Words.objects.filter(user_and_session__id=user_and_session_id).order_by('-pk')

    paginator = Paginator(words_records, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'menu': menu,
        'title': menu[1]['title'],
        'page_obj': page_obj,
    }
    return render(request, 'words/saved.html', context=context)


def learn(request, *args, **kwargs):
    user_and_session, user_and_session_id = get_user_and_session_id(request)

    words_pks = list(Words.objects.filter(user_and_session__id=user_and_session_id).filter(learned=False). \
                     values_list('pk', flat=True))

    amount_of_words_to_learn = 1
    if request.method == 'GET':
        amount_of_words_to_learn = min(5, len(words_pks))
    else:
        if 'amount_of_words_to_learn' in request.POST and int(request.POST['amount_of_words_to_learn']) > 1:
            amount_of_words_to_learn = min(int(request.POST['amount_of_words_to_learn']), len(words_pks))

    pk_list_random = random.sample(words_pks, k=amount_of_words_to_learn)
    words_records = list(Words.objects.filter(pk__in=pk_list_random))
    # paginator = Paginator(words_records, 100)
    # page_obj = paginator.get_page(request.GET.get('page'))

    form_input_number_of_words_to_learn = ChooseAmountOfWordsToLearnForm(
        {'amount_of_words_to_learn': amount_of_words_to_learn}
    )
    button_start_test_form = ButtonStartTestForm()

    if 'add_words_to_test' not in request.session:
        request.session['add_words_to_test'] = {}
    request.session['add_words_to_test']['words_pks'] = pk_list_random
    request.session.save()

    context = {
        'menu': menu,
        'title': menu[2]['title'],
        'words_records': words_records,
        'form_input_number_of_words_to_learn': form_input_number_of_words_to_learn,
        'button_start_test_form': button_start_test_form,
    }
    return render(request, 'words/learn.html', context=context)


def test(request, *args, **kwargs):
    user_and_session, user_and_session_id = get_user_and_session_id(request)


    # print(f"{request.method = }")
    # print(f"{request.POST = }")
    # print(f"{request.GET = }")
    language = 'EN'


    if request.method == 'GET' or request.POST.get('add_words_to_test'):
        if request.POST.get('add_words_to_test'):
            Words.objects.filter(pk__in=request.session['add_words_to_test']['words_pks']).update(learned=True)
        words_pks = list(Words.objects.filter(user_and_session__id=user_and_session_id).filter(learned=True). \
            values_list('pk', flat=True))
        if len(words_pks) < NUMBER_OF_WORDS_TO_TEST:
            number_of_words_to_test = len(words_pks)
        else:
            number_of_words_to_test = NUMBER_OF_WORDS_TO_TEST
        pk_list_random = random.sample(words_pks, k=number_of_words_to_test)
        words_records = list(Words.objects.filter(pk__in=pk_list_random))
        random.shuffle(words_records)
        tested_word = words_records[0]
        tested_word_rating = words_records[0].learning_rating
        random.shuffle(words_records)
        answers_to_choose = words_records

    if request.method == 'POST':
        if request.POST.get('change_lang') == 'EN':
            language = 'RU'
        else:
            language = 'EN'
    #
    #     # if request.POST.get('word') and request.POST.get('do_translate'):
    #     #     button_choose_answer_form = ButtonChooseAnswerForm()
    #     if request.POST.get('chosen_answer'):
    #         answers_counter['questions'] += 1
    #         if request.POST.get('chosen_answer') in \
    #                 (request.session['words_to_learn']['word to test'].word,
    #                  request.session['words_to_learn']['word to test'].translation):
    #             # print("correct")
    #
    #             answers_counter['correct_answers'] += 1
    #             if request.session['words_to_learn']['learning_rating'] > 1 + LEARNING_RATING_DECREMENT:
    #                 request.session['words_to_learn']['word to test'].learning_rating -= LEARNING_RATING_DECREMENT
    #                 request.session['words_to_learn']['word to test'].save()
    #             #
    #             #     button_choose_answer_form = ButtonChooseAnswerForm()
    #             #     # pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk', flat=True)
    #             records = Words.objects.filter(user_and_session__id=user_and_session_id).filter(
    #                 learned=True).values_list('pk',
    #                                           'learning_rating')
    #             #
    #             #     # print(f"{records = }")
    #             pk_list = [record[0] for record in records]
    #             learning_rating_list = [record[1] for record in records]
    #             #     # print(pk_list)
    #             #     # print(learning_rating_list)
    #             #
    #             #     # pk_list = list(pk_list)
    #             if len(pk_list) < number_of_words_to_test:
    #                 number_of_words_to_test = len(pk_list)
    #             #
    #             #
    #             #     # lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #             #     # lst2 = [1, 3, 1, 1, 1, 1, 1, 1, 1, 1]
    #             rates_for_choose = [x / sum(learning_rating_list) for x in learning_rating_list]
    #             #     # print([round(x, 3) for x in rates_for_choose])
    #             pk_list_random = numpy.random.choice(pk_list, p=rates_for_choose, size=number_of_words_to_test,
    #                                                  replace=False)
    #             #     # print(f"{list(pk_list_random) = }")
    #             #
    #             #
    #             #
    #             #     # pk_list_random = random.sample(pk_list, k=number_of_words_to_test)
    #             words = Words.objects.filter(pk__in=pk_list_random)
    #             words = list(words)
    #             random.shuffle(words)
    #
    #             word = words[0]
    #             for i in range(len(words)):
    #                 if words[i].learning_rating > word.learning_rating:
    #                     word = words[i]
    #             request.session['words_to_learn']['word to test'] = word
    #             # words_to_learn['words to test'] = random.choice()
    #             # random.shuffle(words)
    #             request.session['words_to_learn']['answers to choose'] = words
    #             request.session['words_to_learn']['incorrect_answer_response_tip'] = None
    #         else:
    #             request.session['words_to_learn']['word to test'].learning_rating += LEARNING_RATING_INCREMENT
    #             request.session['words_to_learn']['word to test'].save()
    #         request.session['words_to_learn']['learning_rating'] = request.session['words_to_learn'][
    #             'word to test'].learning_rating
    #
    #     if request.POST.get('renew') == 'True':
    #         answers_counter['questions'] = 0
    #         answers_counter['correct_answers'] = 0
    #
    # number_of_all_rows_in_db = Words.objects.filter(user_and_session__id=user_and_session_id).count()
    # number_of_learned_words_in_db = Words.objects.filter(user_and_session__id=user_and_session_id). \
    #     filter(learned=True).count()
    # number_of_words_with_good_rating = Words.objects.filter(user_and_session__id=user_and_session_id). \
    #     filter(learning_rating__lt=10).count()
    # words_statistics = {
    #     'all': number_of_all_rows_in_db,
    #     'learned_words': number_of_learned_words_in_db,
    #     'words_with_good_rating': number_of_words_with_good_rating,
    # }
    #
    # if request.session['words_to_learn']['language'] == 'EN':
    #     word_to_test = request.session['words_to_learn']['word to test'].word
    #     answers_to_choose = [x.translation for x in request.session['words_to_learn']['answers to choose']]
    # else:
    #     word_to_test = request.session['words_to_learn']['word to test'].translation
    #     answers_to_choose = [x.word for x in request.session['words_to_learn']['answers to choose']]
    #
    # answers_to_choose_rating = [x.learning_rating for x in request.session['words_to_learn']['answers to choose']]
    # print(f"{request.session['words_to_learn']['language'] = }")
    # print(f"{answers_to_choose_rating = }")
    #
    button_choose_answer_form = ButtonChooseAnswerForm()
    # request.session.save()

    context = {
        'menu': menu,
        'title': menu[3]['title'],
        'word_to_test': tested_word,
        'lang': language,
        'answers_to_choose': answers_to_choose,
        # 'answers_to_choose_rating': answers_to_choose_rating,
        'button_choose_answer_form': button_choose_answer_form,
        # 'incorrect_answer_response_tip': words_to_learn['incorrect_answer_response_tip'],
        # 'answers_counter': answers_counter,
        # 'button_renew_answers_counter': button_renew_answers_counter,
        # 'words_statistics': words_statistics,
        # 'leaning_rating': request.session['words_to_learn']['learning_rating'],
    }

    # context = {
    #     'menu': menu,
    #     'title': menu[3]['title'],
    #     'word_to_test': word_to_test,
    #     'lang': request.session['words_to_learn']['language'],
    #     'answers_to_choose': answers_to_choose,
    #     # 'answers_to_choose_rating': answers_to_choose_rating,
    #     'button_choose_answer_form': button_choose_answer_form,
    #     # 'incorrect_answer_response_tip': words_to_learn['incorrect_answer_response_tip'],
    #     'answers_counter': answers_counter,
    #     # 'button_renew_answers_counter': button_renew_answers_counter,
    #     'words_statistics': words_statistics,
    #     'leaning_rating': request.session['words_to_learn']['learning_rating'],
    # }
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
