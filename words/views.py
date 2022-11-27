from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect


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

menu = {'Main page', 'About', 'Login'}

def index(request, *args, **kwargs):
    return render(request, 'words/index.html', {'menu': menu, 'title': 'main pag'})


def about(request, *args, **kwargs):
    return render(request, 'words/about.html', {'menu': menu, 'title': 'ABOUT'})


# only if debug = True
def pageNotFound(request, exception):
    return redirect('home')
    # return HttpResponseNotFound("<h1>nah.. not found page</h1>"
    #                             "<hr>"
    #                             "<p>"
    #                             "<h1>stop experiments</h1>")
