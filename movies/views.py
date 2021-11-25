from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
import requests, random

# api 받아오기위해 주소를 입력해놓음 내중에 수정해서 다듬을 예정
base_url = 'https://api.themoviedb.org/3'
api_key = '3268fc394e9330de53ae23e0154458ee'

# Create your views here.
@require_safe
def index(request):
    url = f'{base_url}/movie/top_rated?api_key={api_key}&language=ko-KR&page=1'
    response = requests.get(url).json()
    movies = response['results']
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_id):
    movie_id = int(str(request)[27:-3])
    detail_url = f'{base_url}/movie/{movie_id}?api_key={api_key}&language=ko-KR'
    video_url = f'{base_url}/movie/{movie_id}/videos?api_key={api_key}&language=ko-KR'
    detail_response = requests.get(detail_url).json()
    video_response = requests.get(video_url).json()
    if video_response['results']:
        video_key = video_response['results'][0]['key']
        video_link = 'https://www.youtube.com/embed/'+video_key
    else :
        video_link = ''
    context = {
        'movie': detail_response,
        'video': video_link,
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):
    re_url = f'{base_url}/movie/popular?api_key={api_key}&language=ko-KR'
    re_response = requests.get(re_url).json()
    re_data = re_response['results']
    movies = random.sample(re_data, 3)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/recommended.html', context)

def search(request):
    movie_title = request.GET.get('movie_title')
    id_url = f'{base_url}/search/movie?api_key={api_key}&query={movie_title}&language=ko-KR'
    data = requests.get(id_url).json()
    results = data.get('results')
    num ='0'
    if results:
        if len(results) == 1:
            movie = results[0]
            movie_id = movie['id']
            return redirect('movies:detail', movie_id)
        else:
            num = len(results)
    context = {
        'movies': results,
        'num': num,
    }
    return render(request, 'movies/search.html', context)