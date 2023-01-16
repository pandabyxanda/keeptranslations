import random

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
words_to_learn = {'words': None, 'words_to_test': None, 'incorrect_answer_response_tip': None}
answers_counter = {'questions': 0, 'correct_answers': 0, 'mistakes': 0}
amount_of_words_to_learn = {'number': 5}



# def index(request, *args, **kwargs):
#     return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})

def index(request, *args, **kwargs):
    # words = Words.objects.order_by('-pk')

    current_user_name = get_user(request).username
    current_user_id = get_user(request).id
    print(f"{request.GET = }")

    print(f"{request.POST = }")
    print(f"{get_user(request) = }")
    print(f"{current_user_name = }")
    print(f"{current_user_id = }")

    button_forms = []
    for i in range(0, 3):
        button_forms.append(AddButtonDeletionForm)
    button_form = AddButtonDeletionForm

    words = Words.objects.filter(user__username=current_user_name).order_by('-pk')

    paginator = Paginator(words, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"{page_obj = }")
    for i in page_obj:
        print(f"{i.pk = }")

    print(f"{request.method = }")
    # Words.objects.create(word='235')

    if request.method == 'POST':
        if request.POST.get('word_pk'):
            print(f"{int(request.POST.get('word_pk')) = }")
            print(f"{Words.objects.filter(pk=int(request.POST.get('word_pk'))) = }")
            Words.objects.filter(pk=int(request.POST.get('word_pk'))).delete()

            words = Words.objects.filter(user__username=current_user_name).order_by('-pk')
            paginator = Paginator(words, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        if not request.POST.get('word') and not request.POST.get('translation'):
            form1 = AddWordsForm()
            form2 = AddTranslationForm()

        if request.POST.get('word'):
            print(f"{request.POST.get('word') = }")
            last_word['word'] = request.POST.get('word')
            translation = make_google_translation(last_word['word'])['translatedText']
            print(f'{translation = }')

            form1 = AddWordsForm(request.POST)
            form2 = AddTranslationForm({'translation': translation})

        if request.POST.get('translation'):
            print(f"{request.POST.get('translation') = }")
            form1 = AddWordsForm(last_word)
            form2 = AddTranslationForm(request.POST)
            # print(f"{form1.cleaned_data = }")
            # print(f"{form2.cleaned_data = }")
            # try:
            if current_user_id != None:
                Words.objects.create(
                    word=last_word['word'],
                    translation=request.POST.get('translation'),
                    user=get_user(request),
                )
            # except:
            #     print("error adding to db")

    else:
        print(f"{last_word = }")
        print(f"{word_in_form1 = }")
        form1 = AddWordsForm()
        form2 = AddTranslationForm()

    # if request.method == 'POST':
    #     word = request.POST['word']
    #
    #     translation = request.POST['translation']
    #     if not translation or word != last_word['word']:
    #         translation = make_google_translation(word)['translatedText'] + "\nnext line" + "\nnext line"
    #         print('translation done')
    #     form3 = AddWordsForm1({'word': word, 'translation': translation})
    #     # print(request.POST['word'])
    #     if form3.is_valid():
    #         print(form3.cleaned_data)
    #         try:
    #             form3.save()
    #             last_word['word'] = word
    #         except:
    #             form3.add_error(None, "Error saving to db")
    #     # translation = 'собака'
    #
    #     # form2 = AddTranslationForm({'translation': translation})
    # else:
    #     form3 = AddWordsForm1()

    # if request.method == 'POST':
    #     form1 = AddWordsForm(request.POST)
    #     print(request.POST)
    #     if form1.is_valid():
    #         print(f"{form1.cleaned_data = }")
    #         word_in_form1['word'] = form1.cleaned_data['word']
    #
    #     # translation = 'собака'
    #     translation = make_google_translation(word_in_form1['word'])['translatedText']
    #
    #     form2 = AddTranslationForm({'translation': translation})
    # else:
    #     form1 = AddWordsForm()
    #     form2 = AddTranslationForm()

    context = {
        'words': words,
        'menu': menu,
        'title': menu[0]['title'],
        'form1': form1,
        'form2': form2,
        'page_obj': page_obj,
        'current_user_id': current_user_id,
        'button_form': button_form,
    }

    return render(request, 'words/index.html', context=context)
    # return render(request, 'words/index.html', {'words': words, 'menu': menu, 'title': 'main pag'})


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
    paginator = Paginator(words, 5)
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

        pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=False).values_list('pk', flat=True)
        pk_list = list(pk_list)
        pk_list_random = random.sample(pk_list, k=amount_of_words_to_learn['number'])
        words = Words.objects.filter(pk__in=pk_list_random)
        words_to_learn['words'] = words
        words_to_learn['pk_list'] = pk_list_random

        print(f"{pk_list = }")
        print(f"{pk_list_random = }")
    # rWomen.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        paginator = Paginator(words_to_learn['words'], 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        if words_to_learn['words'] == None:
            page_obj = None
        else:
            paginator = Paginator(words_to_learn['words'], 20)
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
    print("func test")
    print(f"{request.method = }")
    print(f"{request = }")
    print(f"{request.POST = }")
    print(f"{request.GET = }")

    # try:
    #     print(f"{request.POST.get('chosen_answer') = }")
    #
    #     print(f"{words_to_learn['words to test'][0].translation = }")
    # except Exception:
    #     print("Error...")


    if request.method == 'POST' and 'add_words_to_test' in request.POST.keys():
        print(f"{request.POST['add_words_to_test'] = }")
        print(words_to_learn['words'])
        # for i in words_to_learn['words']:
        #     Words.objects.filter(active=True).update(status='inactive')
        print(f"{words_to_learn['pk_list'] = }")

        Words.objects.filter(pk__in=words_to_learn['pk_list']).update(learned=True)



    current_user_name = get_user(request).username
    if request.method == 'GET' or (request.method == 'POST' and 'add_words_to_test' in request.POST.keys()):
        button_choose_answer_form = ButtonChooseAnswerForm()
        # pk_list = Words.objects.filter(user__username=current_user_name).values_list('pk', flat=True)
        pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk', flat=True)
        pk_list = list(pk_list)
        number_of_words_to_test = 5
        if len(pk_list) < number_of_words_to_test:
            number_of_words_to_test = len(pk_list)
        pk_list_random = random.sample(pk_list, k=number_of_words_to_test)
        words = Words.objects.filter(pk__in=pk_list_random)
        print(f"{pk_list_random = }")
        words = list(words)
        random.shuffle(words)
        words_to_learn['words to test'] = [words[0]]
        random.shuffle(words)
        words_to_learn['answers to choose'] = words
        words_to_learn['incorrect_answer_response_tip'] = None



    else:
        if request.method == 'POST':
            if request.POST.get('chosen_answer') == words_to_learn['words to test'][0].translation:
                print("correct")
                button_choose_answer_form = ButtonChooseAnswerForm()
                pk_list = Words.objects.filter(user__username=current_user_name).filter(learned=True).values_list('pk', flat=True)
                pk_list = list(pk_list)
                number_of_words_to_test = 5
                if len(pk_list) < number_of_words_to_test:
                    number_of_words_to_test = len(pk_list)
                pk_list_random = random.sample(pk_list, k=number_of_words_to_test)
                words = Words.objects.filter(pk__in=pk_list_random)
                words = list(words)
                random.shuffle(words)
                words_to_learn['words to test'] = [words[0]]
                random.shuffle(words)
                words_to_learn['answers to choose'] = words
                words_to_learn['incorrect_answer_response_tip'] = None

                answers_counter['correct_answers'] += 1
                answers_counter['questions'] += 1

                words_to_learn['words to test'][0].learning_rating += 1
                words_to_learn['words to test'][0].save()
            else:
                button_choose_answer_form = ButtonChooseAnswerForm()
                words_to_learn['words to test'][0].learning_rating -= 1
                words_to_learn['words to test'][0].save()
                # Words.objects.filter(pk__in=words_to_learn['pk_list']).update(learning_rating=True)
                if request.POST.get('renew') == 'True':
                    answers_counter['questions'] = 0
                    answers_counter['correct_answers'] = 0
                else:
                    if words_to_learn['incorrect_answer_response_tip'] == None:
                        words_to_learn['incorrect_answer_response_tip'] = "Try again"
                    else:
                        words_to_learn['incorrect_answer_response_tip'] += " and again"
                    answers_counter['questions'] += 1



    # print(f"{pk_list = }")
    # print(f"{words_to_learn['words to test'] = }")
    button_renew_answers_counter = ButtonRenewAnswersCounterForm()



    number_of_all_rows_in_db = Words.objects.count()
    number_of_learned_words_in_db = Words.objects.filter(learned=True).count()
    number_of_words_with_good_rating = Words.objects.filter(learning_rating__gt=1).count()
    # print(f"{number_of_all_rows_in_db = }")
    # print(f"{number_of_learned_words_in_db = }")
    # print(f"{number_of_words_with_good_rating = }")
    words_statistics = {
        'all': number_of_all_rows_in_db,
        'learned_words': number_of_learned_words_in_db,
        'words_with_good_rating': number_of_words_with_good_rating,
    }

    context = {
        'menu': menu,
        'title': menu[3]['title'],
        'words_to_test': words_to_learn['words to test'],
        'answers_to_choose': words_to_learn['answers to choose'],
        'button_choose_answer_form': button_choose_answer_form,
        'incorrect_answer_response_tip': words_to_learn['incorrect_answer_response_tip'],
        'answers_counter': answers_counter,
        'button_renew_answers_counter': button_renew_answers_counter,
        'words_statistics': words_statistics,
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
