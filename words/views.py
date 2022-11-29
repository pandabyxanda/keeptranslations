from django.contrib.auth import logout, login
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

# def index(request, *args, **kwargs):
#     return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})

def index(request, *args, **kwargs):
    words = Words.objects.order_by('-pk')
    paginator = Paginator(words, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(last_word)
    if request.method == 'POST':
        word = request.POST['word']

        translation = request.POST['translation']
        if not translation or word != last_word['word']:
            translation = make_google_translation(word)['translatedText']
            print('translation done')
        form3 = AddWordsForm1({'word': word, 'translation': translation})
        # print(request.POST['word'])
        if form3.is_valid():
            print(form3.cleaned_data)
            try:
                form3.save()
                last_word['word'] = word
            except:
                form3.add_error(None, "Error saving to db")
        # translation = 'собака'

        # form2 = AddTranslationForm({'translation': translation})
    else:
        form3 = AddWordsForm1()

    # if request.method == 'POST':
    #     form1 = AddWordsForm(request.POST)
    #     print(request.POST)
    #     if form1.is_valid():
    #         print(form1.cleaned_data)
    #     # translation = 'собака'
    #     translation = make_google_translation(form1.cleaned_data['word'])['translatedText']
    #
    #     form2 = AddTranslationForm({'translation': translation})
    # else:
    #     form1 = AddWordsForm()
    #     form2 = AddTranslationForm()

    context = {
        'words': words,
        'menu': menu,
        'title': menu[0]['title'],
        'form3': form3,
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
    words = Words.objects.order_by('-pk')
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
