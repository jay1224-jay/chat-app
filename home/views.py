from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from home.models import user_data, message, user_key
from django.http import HttpResponseRedirect, JsonResponse
import random
from datetime import datetime
import time

# Create your views here.

def random_text():
    text = ""
    c = 0
    while c < 5:
        t = chr(random.randint(33, 125))
        if t != '/' or t != '\'' or t != '\"' or t != '\\':
            text += chr(random.randint(33, 125))
            c += 1
    return text

def index(request, value=None):
    if value:
        user = user_data.objects.get(userAccount=user_key.objects.get(value=value).account)
        #user_data.objects.get(userAccount=user_key.objects.get(value=value).account).friends.split()
        friends = []
        for i in user_data.objects.get(userAccount=user_key.objects.get(value=value).account).friends.split(): # <= list
            friends.append(user_data.objects.get(userAccount=i))
        print(friends)

        return render(request, 'index.html', {'value': value, 'user': user, 'friends': friends})
    message.objects.all().delete()

    """master_msg = message.objects.all().filter(since='jay',to='123')
    customer_msg = message.objects.all().filter(since='123', to='jay')

    msgs = master_msg | customer_msg
    q_set = msgs
    print(list(q_set.values()))"""
    return render(request, 'index.html')

def create_user(request):
    return render(request, 'sign-up.html')

def delete(request):
    # user_data.objects.filter(id=10).delete()
    return HttpResponseRedirect('/')

def error(request, kind=None, attributes=None): # Attributes => 屬性
    """
    kind: (no-type), (owned)
    Attributes: (no-name, no-account, no-password), (account)
    """
    """
    if kind == 'no-type':
        if attributes == "no-name":

        elif attributes == 'no-account':

        elif attributes == 'no-password':
            
        else:
            # 請勿亂打網址
    """
    return render(request, 'error.html', {
        'kind': kind,
        'attributes': attributes,
    })

# update: UserInfo.objects.filter(owner=user).update(username='your data') 

@csrf_exempt
def build(request):
    if request.POST['name']:
        if request.POST['account']:
            if request.POST['password']:
                if user_data.objects.filter(userAccount=request.POST['account']):
                    return HttpResponseRedirect('/error/owned/' + request.POST['account'])
                else:
                    user_data.objects.create(userName=request.POST['name'], userAccount=request.POST['account'], userPassword=request.POST['password'], friends="")
                    user_key.objects.create(account=request.POST['account'], value=random_text())
                    return HttpResponseRedirect('/login_page/')
            else:
                return HttpResponseRedirect('/error/no-type/no-password/')
        else:
            return HttpResponseRedirect('/error/no-type/no-account/')
    return HttpResponseRedirect('/error/no-type/no-name/')

def login_page(request):
    return render(request, 'login.html')

@csrf_exempt
def login(request):
    return HttpResponseRedirect("/l/"+user_key.objects.get(account=request.POST['account']).value)

def watch_data(request):
    # user_data.objects.get(userAccount='dc').userName
    data = user_data.objects.all()
    return render(request, 'data.html', {'data': data})

def add_friends_p(request, key):
    return render(request, 'add-friends.html', {'user': key})

def search_friend(request, key):
    name = request.GET['s_name']
    list = user_data.objects.filter(userName=name)
    return render(request, 'add-friends.html', {'list': list, 'user': key})
    """
    add_name = request.GET['add_name']
    #user_data.objects.filter(userAccount=user_acc_v.objects.get(value=user_key).account).update(friends=user_data.objects.get(userAccount=user_acc_v.objects.get(value=user_key).account).friends+=)
    #objs = user_data.objects.all()
    to_update = user_data.objects.get(userAccount=user_key.objects.get(value=key).account)
    to_update.friends += f"{add_name} "
    to_update.save()
    return HttpResponseRedirect('/l/'+key)
    """

def add_friends(request, key, add_acc):
    #print(user_data.objects.get(userAccount=add_acc).userName)
    to_update = user_data.objects.get(userAccount=user_key.objects.get(value=key).account)
    to_update.friends += f"{add_acc} "   #f"{user_data  .objects.get(userAccount=add_acc).user} "
    to_update.save()
    return HttpResponseRedirect('/l/'+key)

def talk(request, key, acc):
    """
    master = message.objects.all().filter(_from='jay')
    
    all = master | cus
    print(type(all))
    print(all.order_by('add_time'))
    """
    friend = user_data.objects.get(userAccount=acc)

    customer_acc = acc
    master_acc = user_data.objects.get(userAccount=user_key.objects.get(value=key).account).userAccount

    master_msg = message.objects.all().filter(since=master_acc,to=customer_acc)
    customer_msg = message.objects.all().filter(since=customer_acc, to=master_acc)

    msgs = master_msg | customer_msg
    return render(request, 'talk.html', {'friend': friend, 'user':user_data.objects.get(userAccount=user_key.objects.get(value=key).account), 'key':key, 'msgs':msgs})

@csrf_exempt
def add_talk(request, key, acc):
    if request.POST["mesg"]:
        current_date = timezone.now()
        content = request.POST["mesg"]
        message.objects.create(text=content, since=user_data.objects.get(userAccount=user_key.objects.get(value=key).account).userAccount, to=acc, add_time=current_date)
        
    return HttpResponseRedirect(f'/l/{key}/t/{acc}')


def show(request):
    master_acc = request.GET["user_acc"]
    customer_acc = request.GET["friend_acc"]

    master_msg = message.objects.all().filter(since=master_acc,to=customer_acc)
    customer_msg = message.objects.all().filter(since=customer_acc, to=master_acc)

    msgs = master_msg | customer_msg
    q_set = msgs
    return JsonResponse({'mesgs': list(q_set.values())})