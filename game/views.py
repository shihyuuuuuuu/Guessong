from django.conf import settings
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pytube import YouTube
from pytube import request
from random import randint
from .models import Song, Leader
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
        if request.session['ques_num'] > 10:
            request.session['ques_num'] = 0
            response = {'endGame': True, }
        else:
            song_cnt = Song.objects.count()
            prevs = request.session.get('songs', [])
            while True:
                i = randint(0, song_cnt-1)
                if i not in prevs:
                    request.session['songs'] = request.session.get('songs', []) + [i]
                    break
            song = Song.objects.filter(sid=i)[0]
            choices = [song.title]

            sound = AudioSegment.from_file(str(song.audio)[:])
            random_point = randint(20000, len(sound) - 30000)
            ten_sec = sound[random_point:random_point+10000]
            ten_sec.export("media/music/tmp.mp3", format="mp3")

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
        request.session['songs'] = []
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
            if not Song.objects.filter(Q(url__startswith=form.cleaned_data['url'].split('&')[0])):
                url = form.cleaned_data['url']
                singer = form.cleaned_data['singer']
                song_name = form.cleaned_data['song_name']
                yt = YouTube(url)
                stream = yt.streams.filter(only_audio=True)[0]
                path = stream.download(settings.MEDIA_ROOT+'/music')
                Song.objects.create(sid=song_cnt, title=song_name if song_name else yt.title, author=yt.author, singer=singer if singer else yt.author, seconds=yt.length, views=yt.views, audio=settings.MEDIA_URL+path[path.index('music/'):], url=url)
                return HttpResponse("Song Added!")
            else:
                return HttpResponse("Song Exist!")

    context = {
        'form': AddSongForm(),
    }

    return render(request, 'addsong.html', context=context)

def updateleader(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', "")
        score = float(request.POST.get('score', 0))
        if Leader.objects.count() < 10:
            Leader.objects.create(nickname=nickname, score=score)
        else:
            leader_list = Leader.objects.values_list('nickname', 'score')
            min_score = leader_list.order_by('score').first()[1]
            if score > min_score:
                loser = Leader.objects.filter(score=min_score)[0]
                loser.nickname = nickname
                loser.score = score
                loser.save()
    return HttpResponse("Song Added!")

from django.views import generic

class LeaderBoardView(generic.ListView):
    model = Leader
    template_name = 'leaderboard.html'
    def get_queryset(self):
        return Leader.objects.order_by('-score')