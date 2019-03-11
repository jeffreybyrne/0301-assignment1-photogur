from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment
from photogur.forms import LoginForm
# import ipdb
# import pry


def pictures_page(request):
    pictures = Picture.objects.all()
    context = {'name': 'Jeff', 'pictures': pictures}
    # print(pictures)
    # print(len(pictures[0].comments.all()))
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)


def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)


def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist__contains=query) | Picture.objects.filter(title__contains=query) | Picture.objects.filter(url__contains=query)
    # search_results = Picture.objects.filter(artist=query) | Picture.objects.filter(title=query) | Picture.objects.filter(url=query)
    # ipdb.set_trace()
    # pry()
    context = {'pictures': search_results, 'query': query}
    response = render(request, 'search_results.html', context)
    return HttpResponse(response)


def create_comment(request):
    comment_name = request.POST['comment_name']
    comment_message = request.POST['comment_message']
    comment_picture = Picture.objects.get(pk=request.POST['picture'])
    new_comment = Comment.objects.create(name=comment_name,
                                         message=comment_message,
                                         picture=comment_picture)
    return HttpResponseRedirect('/picture/' + request.POST['picture'])


def login_view(request):
    form = LoginForm()
    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)
