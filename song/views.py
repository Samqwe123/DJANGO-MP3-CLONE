from django.shortcuts import render , get_object_or_404 , redirect
from .models import Song , PlayList
from .forms import register_Form , login_Form , playlist_Form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from random import choice

# Create your views here.
def index(request):
    songs =Song.objects.all()
    play_song_id = request.GET.get('play' , None)
    play_song = None
    playlists = PlayList.objects.filter(user=request.user)

    if request.method == 'POST':
         song_id = request.POST.get('song_id')
         playlist_id = request.POST.get('playlist_id')

         if song_id and playlist_id:
              playlist = PlayList.objects.get(id=playlist_id , user=request.user)
              song = Song.objects.get(id=song_id)
              playlist.song.add(song)


    if play_song_id:
        play_song = get_object_or_404(Song , id=play_song_id)

    return render(request , 'main/index.html' , {'songs': songs , 'play_song' : play_song , 'playlists' : playlists})



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



def login_user(request):
    form = login_Form(request.POST or None)
    if request.method == 'POST' and form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']

            user = authenticate(username=username , password=password)
            if user is not None:
                login(request , user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid login credentials")
    
    return render(request, 'main/login_user.html' , {'forms' : form})
    

def logout_user(request):
    logout(request)
    return redirect('login')
          

         
          
def create_playlist(request):
    form = playlist_Form(request.POST or None)
    playlist = PlayList.objects.filter(user=request.user)
    if request.method == 'POST' and form.is_valid():
         name = form.cleaned_data['name']

         if request.user.is_authenticated:
              create_playlist = PlayList.objects.create(name=name , user=request.user)
              create_playlist.save()
              return redirect("index")
         else:
              form.add_error(None , "user is not authenticated")

    return render(request , 'main/create_playlist.html' , {'forms' : form  , 'playlist' : playlist})

def view_playlist(request , pk):
    
    if request.user.is_authenticated:
        playlist = get_object_or_404(PlayList, id=pk, user=request.user)
        play_song_id = request.GET.get('play' , None)
        shuffle = request.GET.get('shuffle' , 'false') == 'true'
        play_song = None
        next_song = None

        play_song_list = list(playlist.song.all())

        if play_song_id:
             play_song=Song.objects.get(id=play_song_id)

        if shuffle and play_song_list:
             possible_songs = []

             for song in play_song_list:
                if song != play_song:
                    possible_songs.append(song)
                
                if possible_songs:
                     next_song = choice(possible_songs)
                

        else:
            if play_song in play_song_list:
                current_index = play_song_list.index(play_song)
                loop_playlist = (current_index +1) % len(play_song_list)
                next_song = play_song_list[loop_playlist]
                       
                  
                  
                
        user = request.user
        return render(request , 'main/view_playlist.html' , {'playlist': playlist , 'user' : user , 'next_song':next_song , 'play_song':play_song ,'shuffle' : shuffle})
    
    else:
        return redirect('index')
     
            
def all_playlist(request):
    if request.user.is_authenticated:
          playlist = PlayList.objects.filter(user=request.user)
          return render(request , 'main/all_playlist.html', {'playlist' : playlist})
    else:
         return redirect('index')
        


