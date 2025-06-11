from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from userauths import forms as userauths_forms
from userauths import models as userauths_models


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged In")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.UserRegisterForm(request.POST)
        print("Form data:", request.POST)
        print("Form errors:", form.errors)

        if form.is_valid():
            # Save the user first
            user = form.save()
            # Get form data
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "Registration successful. You are now Logged In.")
                
                # Create user profile
                profile = userauths_models.Profile.objects.create(
                    full_name=full_name, 
                    mobile=mobile, 
                    user=user
                )

                profile.save()
               
                
                next_url = request.GET.get("next", "store:index")
                return redirect(next_url)
            else:
                messages.error(request, "Registration failed. Please try again.")
    else:
        form = userauths_forms.UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'userauths/register.html', context)




def login_view(request):
   if request.user.is_authenticated:
      messages.warning(request, "You are already Logged In")
      return redirect("/")

   if request.method == 'POST':
      form= userauths_forms.UserLoginForm(request.POST or None)
      if form.is_valid():
         email=form.cleaned_data['email']
         password=form.cleaned_data['password']
         try:
            user_instance=userauths_models.User.objects.get(email=email,is_active=True)
            user_authenticate=authenticate(request,email=email,password=password)

            if user_instance is not None:
                login(request,user_authenticate)
                messages.success(request, "You are now Logged In")
                next_url = request.GET.get("next", "store:index")
                return redirect(next_url)
            else:
                messages.error(request, "UserName or Password doesn't Exist")
         except:
            messages.error(request, "User doesn't Exist")
         
   else:
      form = userauths_forms.UserLoginForm()


   context = {
      "form": form,
   }            
   return render(request,"userauths/login.html",context)



def logout_view(request):
    logout(request)
    messages.success(request,"You have been Logged Out ") 
    return  redirect("userauths:login")