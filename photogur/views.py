from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def pictures_page(request):
    pictures = Picture.objects.all()
    context = {'name': 'Jeff', 'pictures': pictures}
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
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_pw = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pw)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    response = render(request, 'signup.html', {'form': form})
    return HttpResponse(response)


@login_required
def new_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            new_picture = form.save()
            new_picture.user = request.user
            new_picture.save()
            return HttpResponseRedirect('/picture/' + str(new_picture.id))
    else:
        form = PictureForm()
    response = render(request, 'new_picture.html', {'form': form})
    return HttpResponse(response)


def home(request):
    return HttpResponseRedirect('/pictures')


@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
    if request.method == 'GET':
        form = PictureForm(instance=picture)
        context = {'picture': picture, 'form': form}
        response = render(request, 'edit_picture.html', context)
        return HttpResponse(response)
    elif request.method == 'POST':
        form = PictureForm(request.POST, instance=picture)
        if form.is_valid():
            updated_picture = form.save()
            return HttpResponseRedirect('/picture/{}'.format(picture.id))
        else:
            context = {'form': form, 'picture': picture}
            response = render(request, 'edit_picture.html', context)
            return HttpResponse(response)
