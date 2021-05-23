from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountUpdateForm
from accountapp.models import HelloWorld
from articleapp.models import Article

has_owership = [login_required, account_ownership_required]


@login_required
def hello_world(request):

    if request.method == "POST":

        temp = request.POST.get("hello_world_input")

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        hello_world_list = HelloWorld.objects.all()

        return HttpResponseRedirect(reverse("accountapp:hello_world"))
    else:
        hello_world_list = HelloWorld.objects.all()
        return render(
            request,
            "accountapp/hello_world.html",
            context={"hello_world_list": hello_world_list},
        )


class AccountCreateView(CreateView):
    # 장고에서 제공하는 기본 user 모델
    model = User
    # 장고에서 제공하는 템플릿
    form_class = UserCreationForm
    # 계정 생성 성공시 이동하는 url
    success_url = reverse_lazy("accountapp:hello_world")
    # 회원가입을 할때 어떤 html 파일을 볼지
    template_name = "accountapp/create.html"


class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = "target_user"
    template_name = "accountapp/detail.html"

    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(writer=self.get_object())
        return super(AccountDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )


# @method_decorator(login_required, "post")
# @method_decorator(login_required, "get")
# @method_decorator(account_ownership_required, "get")
# @method_decorator(account_ownership_required, "post")
@method_decorator(has_owership, "get")
@method_decorator(has_owership, "post")
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = "target_user"
    form_class = AccountUpdateForm
    success_url = reverse_lazy("accountapp:hello_world")
    template_name = "accountapp/update.html"

    # 아래 내용을 decorator로 변경
    # def get(self, *args, **kwargs):
    #     if (
    #         self.request.user.is_authenticated
    #         and self.get_object() == self.request.user
    #     ):
    #         return super().get(*args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()
    #
    # def post(self, *args, **kwargs):
    #     if (
    #         self.request.user.is_authenticated
    #         and self.get_object() == self.request.user
    #     ):
    #         return super().get(*args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()


@method_decorator(has_owership, "get")
@method_decorator(has_owership, "post")
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = "target_user"
    success_url = reverse_lazy("accountapp:login")
    template_name = "accountapp/delete.html"
