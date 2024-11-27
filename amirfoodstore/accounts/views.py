from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from accounts.models import Profile
from cart.cart import Cart
from .forms import SignUpForm,UserChangeForm,UpdateUserForm,changepasswordform
from django.contrib.auth.models import User
from random import randint
from django.contrib.auth import login
import ghasedak_sms


sms_api= ghasedak_sms.Ghasedak(baseurl="",api_key='')
class register_user():
    form = SignUpForm()
    otp=''
    username=''
    password=''

    def get_user_data(request):
        form = SignUpForm()
        if request.method == "POST":

            form = SignUpForm(request.POST)

            if form.is_valid():
                register_user.form=form
                otp=str(randint(100000,999999))
                phone_number=form.cleaned_data['number']
                print(otp)
                print(phone_number)
                register_user.otp=otp
                response= sms_api.send_single_sms(message= "",receptor=str(phone_number),line_number='',senddate='',checkid='')
                username=form.cleaned_data['username']
                password=form.cleaned_data['password1']
                register_user.username=username
                register_user.password=password
                return render(request, "accounts/send_otp.html", {})

            else:
                return redirect("register")
        else:
            return render(request, "accounts/register.html", {'form': form})

    def get_otp(request):
        if request.method== "POST":
            sent_otp = str(request.POST.get('sent_otp'))
            if register_user.otp==sent_otp:
                form = register_user.form
                form.save()
                #
                username = register_user.username
                password = register_user.password
                print(username)
                print(password)
                user = authenticate(username=username, password=password)
                login(request,user)
                # login(request,user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, ("You have successfully registered! Welcome!"))
                return redirect('home')
            else:
                print(register_user.otp)
                return redirect("register")


        else:

            return redirect("send_otp")






def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("شما وارد شدید..."))
			return redirect('home')
		else:
			messages.success(request, ("اشکالی وجود دارد... لطفا دوباره تلاش کنید"))
			return redirect('login')

	else:
		return render(request, 'accounts/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("شما بیرون شدید...."))
	return redirect('home')

def profileRegisterView(request):
    if request.method == "POST":
        profileRegisterForm = SignUpForm(request.POST, request.FILES)
        if profileRegisterForm.is_valid():
            user = User.objects.create_user(username=profileRegisterForm.cleaned_data['username'],
                                            email=profileRegisterForm.cleaned_data['email'],
                                            password=profileRegisterForm.cleaned_data['password'],
                                            first_name=profileRegisterForm.cleaned_data['first_name'],
                                            last_name=profileRegisterForm.cleaned_data['last_name'])

            user.save()

            profileModel = Profile(user=user,
                                        ProfileImage=profileRegisterForm.cleaned_data['ProfileImage'],
                                        Gender=profileRegisterForm.cleaned_data['Gender'],
                                        Credit=profileRegisterForm.cleaned_data['Credit'])

            profileModel.save()

            return redirect("home")
    else:
        profileRegisterForm = SignUpForm()

    context = {
        "formData": profileRegisterForm
    }

    return render(request, "shop/signup.html", context)
def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user

        if request.method == 'POST':
            form = changepasswordform(current_user,request.POST)
            if form.is_valid():
                form.save()
                logout(request,current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form=changepasswordform(current_user)
            return render(request, "shop/update_password.html", {'form':form})

    else:
        return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info

        # Get original User Form
        form = UpdateUserForm(request.POST or None, instance=current_user)
        # Get User's Shipping Form

        if form.is_valid():
            # Save original form
            form.save()
            # Save shipping form


            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "shop/update_user.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
# post_save.connect(create_profile, sender=User)


