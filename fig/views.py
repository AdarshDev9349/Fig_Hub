from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as user_logout
from .forms import proform
from django.db.models import Q
from .models import profile as profile_model
import requests 
from .figma import extract_file_key,extract_node_ids
from django.contrib.auth.models import User

@login_required
def home(request):
   users=User.objects.all()
   #print(users)
   user=request.user
   person=profile_model.objects.filter(user=str(request.user.username))
   
   context={'user': user,'person': person, 'users': users}
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
def searchuser(request):
   if request.method == 'POST':

      if 'figma_url' and 'searched_guy' in request.POST:
           figma_url = request.POST.get('figma_url')
           searched_guy = request.POST.get('searched_guy')
           person=profile_model.objects.filter(Q(user__icontains=searched_guy))
           #print(figma_url)
           if figma_url:
             try:
                
                #print(figma_url)
                file_key = extract_file_key(figma_url)
                #print(f'File Key: {file_key}')
                node_id = extract_node_ids()
                #print(f'Node ID: {node_id}')
                api_url = f'https://api.figma.com/v1/images/{file_key}?ids={node_id}'
                #print(api_url)
                headers = {'X-FIGMA-TOKEN': os.environ.get('FIGMA_TOKEN')}
               # print(headers)
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                   image_url = response.json()['images'][node_id]
                   #print(image_url)
                   context={'image_url': image_url,'searched_guy':searched_guy, 'person':person}
                   return render(request, 'usersprofile.html',context)

             except :
              return JsonResponse({'error': 'Error fetching image from Figma API'}, status=400)
      elif 'search' in request.POST:    
       query=request.POST.get('search')
       person=profile_model.objects.filter(Q(user__icontains=query))
       context={'person':person,'searched_guy':query}
       #print(person)
       if not person:
         return HttpResponse("No such person")
       else:
         return render(request,'usersprofile.html',context)



@login_required
def render_figma_image(request):
    if request.method == 'POST':
        if 'figma_url' in request.POST:
         figma_url = request.POST.get('figma_url')
         #print(figma_url)
         if figma_url:
          try:
                
                #print(figma_url)
                file_key = extract_file_key(figma_url)
                #print(f'File Key: {file_key}')
                node_id = extract_node_ids()
                #print(f'Node ID: {node_id}')
                api_url = f'https://api.figma.com/v1/images/{file_key}?ids={node_id}'
                #print(api_url)
                headers = {'X-FIGMA-TOKEN': os.environ.get('FIGMA_TOKEN')}
                #print(headers)
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                   image_url = response.json()['images'][node_id]
                   #print(image_url)
                   return home_with_image(request, image_url)
  
                     
            
            
                else:
                 return JsonResponse({'error': 'Error fetching image from Figma API'}, status=400)
                   
          except :
              return JsonResponse({'error': 'Error fetching image from Figma API'}, status=400)
        if 'delete' in request.POST:
            name=request.POST.get('filename')
            del_pro=profile_model.objects.filter(name=name)
            #print(del_pro)
            del_pro.delete()
            return redirect('fig:home')
           
           
    else:
           return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    



@login_required
def home_with_image(request, image_url):
    user = request.user
    person = profile_model.objects.filter(user=str(request.user.username))
    context = {'user': user, 'person': person, 'image_url': image_url}
    return render(request, 'profile.html', context)






   





