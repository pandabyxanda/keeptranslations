from django.contrib.auth import logout, login, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
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
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'},
]

last_word = {'word': None}
word_in_form1 = {'word': None}
# def index(request, *args, **kwargs):
#     return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})

def index(request, *args, **kwargs):
    # words = Words.objects.order_by('-pk')

    current_user_name = get_user(request).username
    current_user_id = get_user(request).id

    print(f"{get_user(request) = }")
    words = Words.objects.filter(user__username=current_user_name).order_by('-pk')

    paginator = Paginator(words, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"{request.method = }")
    # Words.objects.create(word='235')

    if request.method == 'POST':
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

def about(request, *args, **kwargs):
    context = {
        'menu': menu,
        'title': menu[2]['title'],
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
