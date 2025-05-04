from django.shortcuts import render , get_object_or_404 , redirect
from .models import Song
from .forms import register_Form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login

# Create your views here.
def index(request):
    songs =Song.objects.all()
    play_song_id = request.GET.get('play' , None)
    play_song = None

    if play_song_id:
        play_song = get_object_or_404(Song , id=play_song_id)

    return render(request , 'main/index.html' , {'songs': songs , 'play_song' : play_song})



def register_user(request):
    if request.method == 'POST' :
        form = register_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            user = User.objects.create_user(username=name , password=password)
            login(request , user)
            return redirect('index')
        
    else:
            form = register_Form()

    return render(request, 'main/register_user.html' , {'forms' : form})
            
            


