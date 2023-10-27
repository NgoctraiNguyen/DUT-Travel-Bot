from django.shortcuts import render, redirect
from .models import *
from duckbot import DuckBot

bot = DuckBot()

# Create your views here.
def home(request):
    # conversation = Conservation.objects.all()
    # context= {'conv': conversation}
    contents = Content.objects.all()
    context= {'contents': contents}
    return render(request, 'home.html', context)

def chatting(request):
    context= {}
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
            content = Content(name= tag, last_tag= tag)
            content.save()
        else:
            content = Content.objects.get(id= tag_post)
            last_tag= content.last_tag
            answer, tag = bot.run(question, last_tag= last_tag)
            content.last_tag = tag
            content.save()

        conversation.user_question = question
        conversation.bot_answer = answer
        conversation.conten = content

        conversation.save()

    return redirect('/search?tag='+ str(content.id))

def search(request):
    conten = request.GET.get('tag')
    conten = Content.objects.get(id= conten)
    conversation = Conservation.objects.filter(conten= conten)


    contents = Content.objects.all()
    context= {'conv': conversation, 'cont': conten, 'contents': contents}
    return render(request, 'home.html', context)