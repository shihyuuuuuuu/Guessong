from django.shortcuts import render
from pytube import YouTube
from pytube import request
from django.conf import settings
from django.core.files import File
from .models import Song
from .forms import AddSongForm

# Create your views here.
def index(request):
    """View function for home page of site."""

    context = {}
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def addsong(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        song_cnt = Song.objects.count()

        # Create a form instance and populate it with data from the request:
        form = AddSongForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            singer = form.cleaned_data['singer']
            song_name = form.cleaned_data['song_name']
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True)[0]
            stream.download(settings.MEDIA_ROOT, filename_prefix=str(song_cnt)+'_')
            Song.objects.create(sid=song_cnt, title=song_name if song_name else yt.title, author=yt.author, singer=singer if singer else yt.author, seconds=yt.length, views=yt.views, url=url)
    
    context = {
        'form': AddSongForm(),
    }

    return render(request, 'addsong.html', context=context)