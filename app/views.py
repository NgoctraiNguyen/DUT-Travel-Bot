from django.shortcuts import render, redirect
from .models import *
from duckbot import DuckBot
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse

bot = DuckBot()


# @login_required(login_url='login')
# # Create your views here.
# def home(request):
#     # conversation = Conservation.objects.all()
#     # context= {'conv': conversation}
#     user = request.user
#     contents = Content.objects.filter(user=user)
#     context= {'contents': contents}
#     return render(request, 'home.html', context)

@login_required(login_url='login')
def demo(request):
    # conversation = Conservation.objects.all()
    # context= {'conv': conversation}
    user = request.user
    contents = Content.objects.filter(user=user)
    context= {'contents': contents}
    return render(request, 'demo.html', context)

def chatting(request):
    context= {}
    user = request.user
    conversation = Conservation()
    if request.method == 'POST':
        question = request.POST.get('question')
        tag_post = request.POST.get('tag')


        # Xử lý kết quả
        # answer, tag = bot.run(question, last_tag= last_tag)
        # # answer = 'Đây là câu trả lời'

        # Xử lý content
        if tag_post == '':
            # content = Content(name= 'test2', last_tag= 'hhphh')
            # content.save()

            #...
            answer, tag = bot.run(question)
            content = Content(name= tag, last_tag= tag, user= user)
            content.save()
        else:
            content = Content.objects.get(id= tag_post, user= user)
 
            last_tag= content.last_tag
            answer, tag = bot.run(question, last_tag= last_tag)
            content.last_tag = tag
            content.save()

        conversation.user_question = question
        conversation.bot_answer = answer
        conversation.conten = content
        conversation.save()

    return redirect('/search?tag='+ str(content.id))

def predict(request):
    user = request.user
    conversation = Conservation()
    if request.method == 'POST':
        question = request.POST.get('question')
        tag_post = request.POST.get('tag')

        # Xử lý kết quả
        # answer, tag = bot.run(question, last_tag= last_tag)
        # # answer = 'Đây là câu trả lời'

        # Xử lý content
        if tag_post == '':
            # content = Content(name= 'test2', last_tag= 'hhphh')
            # content.save()

            #...
            answer, tag = bot.run(question)
            content = Content(name= tag, last_tag= tag, user= user)
            content.save()
        else:
            content = Content.objects.get(id= tag_post, user= user)
 
            last_tag= content.last_tag
            answer, tag = bot.run(question, last_tag= last_tag)
            content.last_tag = tag
            content.save()

        conversation.user_question = question
        conversation.bot_answer = answer
        conversation.conten = content
        conversation.save()

    return JsonResponse(
        {'result': answer}
    )

def search(request):
    conten = request.GET.get('tag')
    conten = Content.objects.get(id= conten)
    conversation = Conservation.objects.filter(conten= conten)

    user = request.user
    contents = Content.objects.filter(user=user)
    # contents = Content.objects.all()
    
    context= {'conv': conversation, 'cont': conten, 'contents': contents}
    return render(request, 'demo.html', context)

def login_chatbot(request):
    return  render(request, 'login.html')

def handle_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        print('username ', username)
        pass1 = request.POST['pass1']
        print('password ', pass1)
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request, user)
            return redirect('demo')
        else:
            request.session['message'] = "Sai mật khẩu hoặc sai tên đăng nhập!!"
            context = {'message':'Sai mật khẩu hoặc sai tên đăng nhập!!'}
            return render(request,'login.html', context)
    else:
        return redirect('login')
    
def handle_logout(request):
    logout(request)
    return redirect('login')