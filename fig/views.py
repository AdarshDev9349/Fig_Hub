from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as user_logout
from .forms import proform
from django.db.models import Q
from .models import profile as profile_model
import requests 
from .figma import extract_file_key,extract_node_ids


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
      


@login_required
def render_figma_image(request):
    if request.method == 'POST':
        figma_url = request.POST.get('figma_url')
        print(figma_url)
        if figma_url:
          try:
                
                print(figma_url)
                file_key = extract_file_key(figma_url)
                print(f'File Key: {file_key}')
                node_id = extract_node_ids(figma_url)
                print(f'Node ID: {node_id}')
                api_url = f'https://api.figma.com/v1/images/{file_key}?ids={node_id}'
                headers = {'X-FIGMA-TOKEN': 'figd_4FulpmVt5KJksGuri0UGFjpqBotFW0BuXmxBbXZI'}
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    image_url = response.json()['images'][node_id]
                    return render(request,'figma.html',{'image_url':image_url})
  
                     
            
            
                else:
                 return JsonResponse({'error': 'Error fetching image from Figma API'}, status=400)
                   
          except :
              return JsonResponse({'error': 'Error fetching image from Figma API'}, status=400)
             
    else:
           return JsonResponse({'error': 'Invalid request method'}, status=405)
















