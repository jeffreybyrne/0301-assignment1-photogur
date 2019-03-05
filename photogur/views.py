from django.http import HttpResponse
from django.shortcuts import render
from photogur.models import Picture  # , Comment
# import ipdb


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
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results, 'query': query}
    response = render(request, 'search_results.html', context)
    return HttpResponse(response)
