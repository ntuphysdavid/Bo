from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Inventory, Img, FA
from django.core.urlresolvers import reverse
from management.utils import permission_check,  permission_check2, permission_check3


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_inventory(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_inventory = Inventory(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', ''),
                publish_date=request.POST.get('publish_date', ''),
                description=request.POST.get('description', '')
        )
        new_inventory.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_inventory',
        'state': state,
    }
    return render(request, 'management/add_inventory.html', content)

@user_passes_test(permission_check2)
def view_inventory_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Inventory.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Inventory.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        inventory_list = Inventory.objects.all()
    else:
        inventory_list = Inventory.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        inventory_list = Inventory.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(inventory_list, 65)
    page = request.GET.get('page')
    try:
        inventory_list = paginator.page(page)
    except PageNotAnInteger:
        inventory_list = paginator.page(1)
    except EmptyPage:
        inventory_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_inventory',
        'category_list': category_list,
        'query_category': query_category,
        'inventory_list': inventory_list,
    }
    return render(request, 'management/view_inventory_list.html', content)

@user_passes_test(permission_check2)
def detail(request):
    user = request.user if request.user.is_authenticated() else None
    inventory_id = request.GET.get('id', '')
    if inventory_id == '':
        return HttpResponseRedirect(reverse('view_inventory_list'))
    try:
        inventory = Inventory.objects.get(pk=inventory_id)
    except Inventory.DoesNotExist:
        return HttpResponseRedirect(reverse('view_inventory_list'))
    content = {
        'user': user,
        'active_menu': 'view_inventory',
        'inventory': inventory,
    }
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    inventory=Inventory.objects.get(pk=request.POST.get('inventory', ''))
            )
            new_img.save()
        except Inventory.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'inventory_list': Inventory.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)

@user_passes_test(permission_check3)
def view_FA_list(request):
    user = request.user if request.user.is_authenticated() else None
    bugzilla_list = FA.objects.values_list('bugzilla', flat=True).distinct()
    query_bugzilla = request.GET.get('bugzilla', 'all')
    if (not query_bugzilla) or FA.objects.filter(bugzilla=query_bugzilla).count() is 0:
        query_bugzilla = 'all'
        fa_list = FA.objects.all()
    else:
        fa_list = FA.objects.filter(bugzilla=query_bugzilla)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        FA_list = FA.objects.filter(name__contains=keyword)
        query_bugzilla = 'all'

    paginator = Paginator(FA_list, 5)
    page = request.GET.get('page')
    try:
        FA_list = paginator.page(page)
    except PageNotAnInteger:
        FA_list = paginator.page(1)
    except EmptyPage:
        FA_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_FA',
        'bugzilla_list': bugzilla_list,
        'query_bugzilla': query_bugzilla,
        'FA_list': FA_list,
    }
    return render(request, 'management/view_FA_list.html', content)
