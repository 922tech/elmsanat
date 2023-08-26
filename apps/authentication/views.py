from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from config import settings
from .services import AuthService
 

BROWSER_AGENT =  'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'
client_id = settings.OAUTH_CREDENTIALS['login']['client_id']
client_secret = settings.OAUTH_CREDENTIALS['login']['client_secret']
token_url = settings.TOKEN_URL


def index(request):
    return HttpResponse('<h1>Welcome to the web app</h1>')


@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        user_agent = request.headers.get('user-agent')
        if request.COOKIES.get('access_token'):
            return HttpResponse(f'<section>You are already logged in</section>')
        if user_agent == BROWSER_AGENT :
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(request.POST.dict())
            credentials = {"username":username, "password":password}
        else:
            credentials = request.data

        response =  AuthService.obtain_token_request(**credentials)

        if response.status_code == 200:
            response_data = response.json()

            if user_agent != BROWSER_AGENT :
                return Response(response_data)

            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            res =  HttpResponse(f'<section>You have logged in!</section>')
            res.set_cookie('access_token', access_token)
            res.set_cookie('refresh_token', refresh_token)

        else:
            res =  HttpResponse(f'<section>Cridentials were not valid!</section>' , status=400)

        return res


@csrf_exempt
@api_view(['GET','POST'])
def logout(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    
    elif request.method == 'POST':
        user_agent = request.headers.get('user-agent')

        if user_agent == BROWSER_AGENT:
            token = request.COOKIES.get('access_token')
            if not token:
                return HttpResponse(f'<section>you are not logged in.</section>' , status=400)
            
        else:
            token = request.data['token']
            if not token:
                Response({'response':'You are not logged in'}, status=400)
            
        response = AuthService.revoke_token_request(token)
        print(response.text)

        return HttpResponse(f'<h3> Good Bye! </h3>' , status=200)
    