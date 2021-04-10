from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, UserIp
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from datetime import timedelta
from django.core import serializers
from django.http import HttpResponse
from .forms import RegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .utils import sendTransaction
import hashlib


#Richiesta n°8 funzione per la lettura dell'IP del client.
def getIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#Richiesta n°1 una pagina da cui è possibile far registrare ed accedere gli utenti.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    form = RegisterForm(request.POST)
    modelIp = UserIp()
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        modelIp.user = User.objects.get(username=user)
        modelIp.ip = getIp(request)
        modelIp.save()
        messages.success(request,'Account creato con successo, benvenuto '+ user)
        return redirect('log-in')
    context = {'form':form}
    return render(request, 'api/sign_up.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            lastIp = UserIp.objects.get(user=user)
            if not lastIp.ip == getIp(request):
                lastIp.ip = getIp(request)
                lastIp.save()
                messages.info(request,"Attenzione il tuo ip è cambiato dall'ultima sessione")
            return redirect('post_list')
        else:
            messages.info(request, 'Nome utente o Password non corretti')

    return render(request, 'api/login.html')

#Richiesta n°2 pagina da cui è possibile scrivere un post
# vedere i post di tutti gli utenti  in ordine cronologico.
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'api/post_list.html', context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.hash = hashlib.sha256(post.text.encode('utf-8')).hexdigest()
            post.txId = sendTransaction(post.hash)
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'api/post_edit.html', {'form':form})

# pagina accessibile solo dagli admin che riporta alle varie
# funzioni avanzate (Richieste n°3, n°5, n°6)
@user_passes_test(lambda u: u.is_staff)
def staff_index(self):
    return render(self, 'api/staff_index.html')

# Richiesta n°3 pagina accessibile solo agli admin dove è possibile vedere
# il numero di post pubblicati da ciascun utente.
@user_passes_test(lambda u: u.is_staff)
def num_post(request):
    num_post = dict(User.objects.values_list('username').annotate(Count('post')))
    context = {'num_post' : num_post}
    return render(request, 'api/post_numbers.html', context)

# Richiesta n°4 pagina accessibile dall'url /utente/id, per ulteriore personalizzazione ho aggiunto la possibilità
# di visualizzare tutti i post dell'utente corrispondente all'id.
@login_required
def user_profile(request, pk):
    if User.objects.filter(pk=pk).exists():
        user = get_object_or_404(User, pk=pk)
        userPosts = Post.objects.filter(author=pk).order_by('-published_date')
        context = {
            'user': user,
            "userPosts": userPosts
        }
        return render(request, 'api/user_profile.html', context)
    else:
        return render(request, 'api/invalid_user.html'.format(pk))

# Richiesta n°5 un endpoint che fornisca una risposta in JSON contenente le info sui post
# pubblicati nell'ultima ora
def last_hour(self):
    time_treshold = timezone.now() - timedelta(hours=1)
    posts = serializers.serialize('json', Post.objects.filter(published_date__gte=time_treshold).order_by('-published_date'))
    return HttpResponse(posts, content_type='json')

# Richiesta n°6 un endpoint che fornita una stringa tramite GET restituisca un
# valore intero corrispondente al numero di volte che quella stringa compare
# nei post pubblicati (controllo sia nel titolo che nel corpo dei post).
def search(request):
    query = request.GET.get('q')
    control_text = str(Post.objects.values('title', 'text'))
    control_text.lower()
    counter = control_text.count(query)
    context = {
        'counter': counter,
        'query': query
    }
    return render(request, 'api/search.html', context)
