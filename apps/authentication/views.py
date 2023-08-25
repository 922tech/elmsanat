from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from config import settings
from .services import AuthService


client_id = settings.OAUTH_CREDENTIALS['login']['client_id']
client_secret = settings.OAUTH_CREDENTIALS['login']['client_secret']
token_url = settings.TOKEN_URL


def index(request):
    return HttpResponse('<h1>THIS APP</h1>')


def login(request:HttpRequest):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        if request.COOKIES.get('access_token'):
            return HttpResponse(f'<section>You are already logged in</section>')

        username = request.POST.get('username')
        password = request.POST.get('password')

        response =  AuthService.obtain_token_request(username, password)

        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            res =  HttpResponse(f'<section>You have logged in!</section>')
            res.set_cookie('access_token', access_token)
            res.set_cookie('refresh_token', refresh_token)

        else:
            res =  HttpResponse(f'<section>Cridentials were not valid!</section>' , status=400)

        return res


def logout(request :HttpRequest):
    if request.method == 'GET':
        return render(request, 'logout.html')
    
    elif request.method == 'POST':
        token = request.COOKIES.get('access_token')
        if not token:
            return HttpResponse(f'<section>you are not logged in.</section>' )
            
        response = AuthService.revoke_token_request(token)
        res = HttpResponse(f'<section>{response.status_code}</section>' )
        print( response.text)
        return res
    
    pass