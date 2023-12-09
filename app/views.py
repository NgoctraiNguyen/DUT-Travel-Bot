from django.shortcuts import render, redirect
from .models import *
import random
from duckbot import DuckBot
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
import ast
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
bot = DuckBot()


@login_required(login_url='login')
# Create your views here.
def home(request):
    # conversation = Conservation.objects.all()
    # context= {'conv': conversation}
    user = request.user
    contents = Content.objects.filter(user=user)
    context= {'contents': contents}
    return render(request, 'home.html', context)

@login_required(login_url="login")
def demo(request):
    user = request.user
    contents = Content.objects.filter(user=user)
    context = {"contents": contents}
    return render(request, "demo2.html", context)

def chatting(request):
    context = {}
    user = request.user
    conversation = Conservation()
    if request.method == "POST":
        question = request.POST.get("question")
        tag_post = request.POST.get("tag")
        # Xử lý kết quả
        # answer, tag = bot.run(question, last_tag= last_tag)
        # # answer = 'Đây là câu trả lời'
        print("người dùng hỏi :  ",question)
        list_chao_hoi = ['xin chào', 'chào bạn', 'hello bạn','chào bot']
        contains_chao_hoi = any(chao_hoi in question for chao_hoi in list_chao_hoi)
        list_answer = ["Xin chào! Tôi là chatbot Đà Nẵng. Bạn cần giúp gì hôm nay?","Chào bạn! Đây là chatbot Đà Nẵng. Có điều gì tôi có thể hỗ trợ bạn?","Chào bạn! Tôi là đại diện ảo cho Đà Nẵng. Cần tôi giúp gì không?","Xin chào! Tôi là chatbot của Đà Nẵng. Bạn muốn biết thông tin gì về thành phố này?"]
        random.shuffle(list_answer)
        
        if contains_chao_hoi:
            answer = random.choice(list_answer)
            tag = "Chào hỏi"
            content = Content(name=tag, last_tag=tag, user=user)
            content.save()
            img_text = ""
            suggest_text = '["Giới thiệu về thành phố đà nẵng", "Giới thiệu về Đà Nẵng những thắng cảnh nổi tiếng", "Giới thiệu những bãi biển đẹp ở Đà Nẵng?"]'
            
        # Xử lý content
        elif tag_post == "":
            answer, tag, img_text, suggest_text = bot.run(question)
            content = Content(name=tag, last_tag=tag, user=user)
            content.save()
        else:
            content = Content.objects.get(id=tag_post, user=user)

            last_tag = content.last_tag
            answer, tag, img_text, suggest_text = bot.run(question, last_tag=last_tag)
            content.last_tag = tag
            content.save()
        print(f"img_text {img_text}")
        if '\n' not in  img_text :
            print("img_text ", img_text)
            link_img = img_text
        elif img_text:
            img_text_list = img_text.split("\n")
            link_img = img_text_list[0]
        else:
            link_img = ""

        conversation.user_question = question
        conversation.bot_answer = answer
        conversation.conten = content
        conversation.link_img = link_img    
        conversation.suggest_text = suggest_text
        conversation.save()
        print(suggest_text)
        suggest_text = ast.literal_eval(suggest_text)
        random.shuffle(suggest_text)
        if (len(suggest_text) >= 3):
            suggest_text1 = suggest_text[:3]
        else:
            suggest_text1 = suggest_text
        # print("len : ",len(suggest_text))
        # print("noi dung suggest_text: ", suggest_text1)
    request.session["suggest_text_first"] = suggest_text1
    return redirect("/search?tag=" + str(content.id))

def predict(request):
    user = request.user
    conversation = Conservation()
    if request.method == "POST":
        question = request.POST.get("question")
        tag_post = request.POST.get("tag")

        # Xử lý kết quả
        # answer, tag = bot.run(question, last_tag= last_tag)
        # # answer = 'Đây là câu trả lời'
        list_chao_hoi = ['xin chào', 'chào bạn', 'hello bạn','chào bot']
        contains_chao_hoi = any(chao_hoi in question for chao_hoi in list_chao_hoi)
        list_answer = ["Xin chào! Tôi là chatbot Đà Nẵng. Bạn cần giúp gì hôm nay?","Chào bạn! Đây là chatbot Đà Nẵng. Có điều gì tôi có thể hỗ trợ bạn?","Chào bạn! Tôi là đại diện ảo cho Đà Nẵng. Cần tôi giúp gì không?","Xin chào! Tôi là chatbot của Đà Nẵng. Bạn muốn biết thông tin gì về thành phố này?"]
        random.shuffle(list_answer)
        
        if contains_chao_hoi:
            answer = random.choice(list_answer)
            tag = "Chào hỏi"
            content = Content(name=tag, last_tag=tag, user=user)
            content.save()
            img_text = ""
            suggest_text = '["Giới thiệu về thành phố đà nẵng", "Giới thiệu về Đà Nẵng những thắng cảnh nổi tiếng", "Giới thiệu những bãi biển đẹp ở Đà Nẵng?"]'
        # Xử lý content
        elif tag_post == "":
            answer, tag, img_text, suggest_text = bot.run(question)
            content = Content(name=tag, last_tag=tag, user=user)
            content.save()
        else:
            content = Content.objects.get(id=tag_post, user=user)

            last_tag = content.last_tag
            answer, tag, img_text, suggest_text = bot.run(question, last_tag=last_tag)
            content.last_tag = tag
            content.save()

        print("len (img_text)")
        if '\n' not in  img_text:
            print("img_text ", img_text)
            link_img = img_text
        elif img_text:
            img_text_list = img_text.split("\n")
            link_img = img_text_list[0]
        else:
            link_img = ""

        print("link_img ", link_img)
        conversation.user_question = question
        conversation.bot_answer = answer
        conversation.conten = content
        conversation.link_img = link_img
        conversation.suggest_text = suggest_text
        conversation.save()

    return JsonResponse(
        {"answer": answer, "link_img": link_img, "suggest_text": suggest_text}
    )

def search(request):
    conten = request.GET.get("tag")
    conten = Content.objects.get(id=conten)
    conversation = Conservation.objects.filter(conten=conten)
    user = request.user
    contents = Content.objects.filter(user=user)
    conversation_last = conversation.last()
    suggest_text = conversation_last.suggest_text
    suggest_text = ast.literal_eval(suggest_text)
    random.shuffle(suggest_text)
    if (len(suggest_text) >= 3):
        suggest_text1 = suggest_text[:3]
    else:
        suggest_text1 = suggest_text
    print("len : ",len(suggest_text1))
    request.session['suggest_text_first'] = suggest_text1
    
    context = {
        "conv": conversation,
        "cont": conten,
        "contents": contents,
        # "suggest_text_first": suggest_text_first,
    }
    return render(request, "demo2.html", context)

def login_chatbot(request):
    return render(request, "login.html")

def handle_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        print("username ", username)
        pass1 = request.POST["pass1"]
        print("password ", pass1)
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("demo")
        else:
            messages.error(request, 'Có lỗi xảy ra khi đăng nhập tài khoản.')
            return redirect("login")
    else:
        return redirect("login")

def handle_logout(request):
    logout(request)
    return redirect("login")

def signup(request):
    return render(request,"signup.html")

def handle_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã đăng ký !')
            return redirect('signup')    
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username đã trùng!')
            return redirect('signup')     
        if pass1 != pass2:
            messages.error(request, 'Mật khẩu không khớp !')
            return redirect('signup') 
        
        try:
            validate_password(pass1)
            print("Mật khẩu hợp lệ")
        except Exception as e:
            messages.error(request, 'mật khẩu không hợp lệ !')
            return redirect('signup') 
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = True
        myuser.save()
        messages.success(request, 'Đăng kí tài khoản thành công!')
        return redirect("login")
    return redirect('signup')