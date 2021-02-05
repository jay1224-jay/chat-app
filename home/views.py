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
        t = chr(random.randint(65, 122))
        if t != '/' and t != '\'' and t != '\"' and t != '\\' and t != '%':
            text += t
            c += 1
    return text

def index(request, key=None):
    if key:
        user = user_data.objects.get(userAccount=user_key.objects.get(value=key).account)
        #user_data.objects.get(userAccount=user_key.objects.get(value=value).account).friends.split()
        friends = []

        try:
            eval(user.friends)
        except:
            user.friends = "[]"
            user.save()
        n = 0
        for i in eval(user_data.objects.get(userAccount=user_key.objects.get(value=key).account).friends): # <= list
            try:
                friends.append(user_data.objects.get(userAccount=i))
            except: # already delete
                friend = eval(user.friends)
                del friend[n]
                user.friends = str(friend)
                user.save()
            n += 1

        return render(request, 'index.html', {'key': key, 'user': user, 'friends': friends, 'login': True})
    return render(request, 'index.html', {'login': False})

def create_user(request):
    return render(request, 'sign-up.html')


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

def delete(request, acc):
    user_data.objects.filter(userAccount=acc).delete()
    user_key.objects.filter(account=acc).delete()
    return HttpResponseRedirect('/')

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
    s = request.GET['s_']
    n_list = user_data.objects.filter(userName=s)
    a_list = user_data.objects.filter(userAccount=s)
    list = n_list | a_list 
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
    print(to_update.friends)
    try:
        eval(to_update.friends)
    except:
        to_update.friends = "[]" # set default
    
    to_update.friends = str(eval(to_update.friends) + eval(f"[\"{add_acc}\"]"))    # f{user_data  .objects.get(userAccount=add_acc).user} "
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

def delete_friend(request, key, acc):
    to_update = user_data.objects.get(userAccount=user_key.objects.get(value=key).account)
    
    old = eval(to_update.friends)
    del old[old.index(acc)]
    
    to_update.friends = str(old)
    to_update.save()
    return HttpResponseRedirect('/l/'+key)