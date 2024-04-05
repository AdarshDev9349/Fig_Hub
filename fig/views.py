from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as user_logout
from .forms import proform
from django.db.models import Q
from .models import profile as profile_model


@login_required
def home(request):
    
   user=request.user
   person=profile_model.objects.filter(user=str(request.user.username))
   context={'user': user,'person': person}
   return render(request,'profile.html',context)

def signup(request):
     if request.method=='POST':
        myform=UserCreationForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('fig:login')
     else :   
      myform= UserCreationForm()
     context={'form':myform}
     return render(request, 'registration/signup.html',context)

@login_required
def logout(request):
    if request.method == 'POST':
        user_logout(request)
        return redirect('home')

@login_required
def profile(request):
    if request.method=='POST':
      myform=proform(request.POST)
      if myform.is_valid():
         person=profile_model(
            user=str(request.user.username),
            name=myform.cleaned_data['name'],
            figma_file=myform.cleaned_data['figma_file']
         )
         person.save()
         return redirect('fig:home')
    else:     
      myform=proform()
    context={'myform':myform}
    return render(request,'form.html',context)

@login_required
def search(request):
   return render(request,'search.html')

@login_required
def searchuser(request):
   if request.method == 'POST':
      query=request.POST.get('search')
      person=profile_model.objects.filter(Q(user__icontains=query))
      context={'person':person,'searched_guy':query}
      print(person)
      if not person:
         return HttpResponse("No such person")
      else:
         return render(request,'usersprofile.html',context)