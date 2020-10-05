from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pytube import YouTube
from pytube import request
from random import randint
from .models import Song
from .forms import AddSongForm
from pydub import AudioSegment
import random

# Create your views here.
def index(request):
    """View function for home page of site."""
    if request.method == 'GET' and request.GET:
        ques_num = request.session.get('ques_num', 0)
        request.session['ques_num'] = ques_num + 1
        request.session['nickname'] = request.GET.get('nickname', "")
        if request.session['ques_num'] >= 11:
            request.session['ques_num'] = 0
            response = {'endGame': True, }
        else:
            song_cnt = Song.objects.count()
            song = Song.objects.filter(sid=randint(0, song_cnt-1))[0]
            choices = [song.title]

            sound = AudioSegment.from_file(str(song.audio)[1:])
            random_point = randint(20000, len(sound) - 30000)
            first_half = sound[random_point:random_point+10000]
            first_half.export("media/music/tmp.mp3", format="mp3")

            response = {
                'endGame': False,
                'song': {
                    'src': "/media/music/tmp.mp3",
                    'title': song.title,
                },
                'choices': choices,
            }
            while len(choices) != 4:
                t = Song.objects.get(sid=randint(0, song_cnt-1)).title
                if t not in choices:
                    choices.append(t)
            random.shuffle(choices)
        return JsonResponse(response)
    else:
        request.session['ques_num'] = 0
        context = {
            'nickname': request.session.get('nickname', ""),
        }
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
            path = stream.download(settings.MEDIA_ROOT+'/music')
            print(path)

            Song.objects.create(sid=song_cnt, title=song_name if song_name else yt.title, author=yt.author, singer=singer if singer else yt.author,
                                seconds=yt.length, views=yt.views, audio=settings.MEDIA_URL+path[path.index('music/'):], url=url)
            return HttpResponse("Song Added!")

    context = {
        'form': AddSongForm(),
    }

    return render(request, 'addsong.html', context=context)