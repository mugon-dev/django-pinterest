from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from accountapp.models import HelloWorld


def hello_world(request):
    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        hello_world_list = HelloWorld.objects.all()

        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    else:
        hello_world_list = HelloWorld.objects.all()
        return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})


class AccountCreateView(CreateView):
    # 장고에서 제공하는 기본 user 모델
    model = User
    # 장고에서 제공하는 템플릿
    form_class = UserCreationForm
    # 계정 생성 성공시 이동하는 url
    success_url = reverse_lazy('accountapp:hello_world')
    # 회원가입을 할때 어떤 html 파일을 볼지
    template_name = 'accountapp/create.html'
