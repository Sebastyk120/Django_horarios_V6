from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if request.user.username == 'asanchez':
        return redirect('ope_home')
    elif request.user.username == 'mbonilla':
        return redirect('ope_home')
    else:
        return render(request, 'home.html')

