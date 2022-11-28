from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

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
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'},
]

last_word = {'word': None}

# def index(request, *args, **kwargs):
#     return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})

def index(request, *args, **kwargs):
    words = Words.objects.all()

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
    }


    return render(request, 'words/index.html', context=context)
    # return render(request, 'words/index.html', {'words': words, 'menu': menu, 'title': 'main pag'})

def about(request, *args, **kwargs):
    context = {
        'menu': menu,
        'title': menu[1]['title'],
    }
    return render(request, 'words/about.html', context=context)

def login(request, *args, **kwargs):
    return HttpResponse("login page, not created")

# only if debug = True
def pageNotFound(request, exception):
    return redirect('home')
    # return HttpResponseNotFound("<h1>nah.. not found page</h1>"
    #                             "<hr>"
    #                             "<p>"
    #                             "<h1>stop experiments</h1>")
