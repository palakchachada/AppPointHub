from django.shortcuts import render,redirect
from .forms import LoginForm
from .models import AddApps,Employee,Points, Role
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
# Create your views here.
def login_page(request):
    error_message = ""
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        email=request.POST["email"]
        print("userrr",email)
        entered_password = request.POST['password']
        print("entered pass",entered_password)
        try:
            use = Employee.objects.get(email=email)
            print("use", use.password, use.email)

            role = Role.objects.get(email=use.email)
            print("rolee",role.email)
            print("password check",check_password(entered_password, use.password))
            print("password check2",entered_password)
            print("password check3",use.password)
            # Verify the entered password with the hashed password
            if check_password(entered_password, use.password):
                print("Password match")
                request.session['email'] = use.email  # Store email in sessio
                print(request.session['email'],"emm")
                if use.email in role.email and role.role_name == 'Admin':
                    return redirect('add_points')
                else:
                    return redirect('user_details')
            else:
                print("Invalid password")
                error_message = "Invalid Email or Password"
                # Handle invalid password (e.g., show error message or redirect to login)
        except Employee.DoesNotExist:
            print("User not found")
            error_message = "User not found. Please register."
            # Handle case when email does not exist in the database

    return render(request, 'login_page.html', {'form': form, 'error_message':error_message})


def forgot_password(request):
    error = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        print("emailll",email)
        # return redirect('change_password')
        new_password = request.POST.get('password')
        print('new_password',new_password)
        # # 1223
        confirm_password = request.POST.get('confirm_password')
        print('confirm_password',confirm_password)
        try:

            e = Employee.objects.get(email=email)
            print('e o', e, e.password) 
            
            print("nan",new_password == confirm_password)
            e.password = make_password(new_password)
            if new_password == confirm_password:
                e.save()
                print('New pass',e,e.password)
                return redirect('/login/')
            else:
                error = "Passwords Do Not Match"
        except Employee.DoesNotExist:
            error = "User Not Found"
    # return render(request,'change_password.html')
    return render(request,'forgot_password.html',{'error':error})

def change_password(request):
        # email = request.POST.get('email')
        # print('emaill change',email)
    # 
    user_email = request.session.get('email')
    print("user_email",user_email)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        print('new_password',new_password)
        # # 1223
        confirm_password = request.POST.get('confirm_password')
        print('confirm_password',confirm_password)
        
        e = Employee.objects.get(email=user_email)
        print('e o', e, e.password) 
        
        print("nan",new_password != confirm_password)
        e.password = 456
        e.save()
        print('New pass',e,e.password)
        return redirect('/login/')
    return render(request,'change_password.html')

def user_details(request):
    # user = request.session.get('email')
    # print("userr",user)
    user_email = request.session.get('email')
    print("user_email",user_email)
    e = Employee.objects.get(email=user_email)
    print("e",e, e.fname)
    app = AddApps.objects.all()
    print('app',app)
    poin = Points.objects.values('points','app_name')
    print('poin',poin)
    context = {
        'app':app,
        'poin':poin,
        'e':e,
    }
    return render(request,'user_details.html',context)


def task_details(request,app_name):

    user_email = request.session.get('email')
    print("user_email",user_email)
    e = Employee.objects.get(email=user_email)
    print("e",e, e.fname)

    app = AddApps.objects.get(app_name = app_name)
    print("all apps",app)
    poin = Points.objects.filter(app_name=app_name).values()
    print("filtered points",poin)
    context = {
        'app':app,
        'poin':poin,
        'e':e,
    }
    return render(request,'task_details.html',context)


def home_page(request):
    if request.method == "POST":
        app_name = request.POST.get("app_name")
        app_link = request.POST.get("app_link")
        app_category = request.POST.get("app_category")
        sub_category = request.POST.get("sub_category")
    
    return render(request,'home.html')


# def user_profile(request):
#     user_email = request.session.get('email')
#     print("profile",user_email)
#     e = Employee.objects.get(email = user_email)
#     print("profile e", e)
#     context = {
#         'e':e,
#     }
#     return render(request,'profile.html',context)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import AddApps  # Assuming you have an `App` model to store app details

def add_points(request):
    user_email = request.session.get('email')
    print("user_email",user_email)
    e = Employee.objects.get(email = user_email)
    print("e from add points",e)
    if request.method == "POST":
        app_name = request.POST.get("app_name")
        app_link = request.POST.get("app_link")
        app_category = request.POST.get("app_category")
        sub_category = request.POST.get("sub_category")
        app_name1 = request.session.get('app_name')
        image = request.FILES.get("image") 
        print('app_name',app_name1)
        # Save the data into the database
        app = AddApps(
            app_name=app_name,
            app_link=app_link,
            app_category=app_category,
            sub_category=sub_category,
            image = image
        )
        app.save()

        # Store the last added app in the session
        request.session['last_added_app'] = app_name
        print(app_name,"last ")

       
        

        # pid = request.POST.get('pid')
        # points = request.POST.get('points')
        # app_name_str = request.POST.get('app_name')  # Get app_name as a string
        # print("points", points)
    
        # try:
        #     # Fetch the corresponding AddApps instance
        #     app_instance = AddApps.objects.get(app_name=app_name_str)
            
        #     # Save the Points instance
        #     p = Points(points=points, app_name=app_instance)
        #     p.save()
        # except AddApps.DoesNotExist:
        #     # Handle case where the AddApps instance does not exist
        #     print(f"AddApps with name '{app_name_str}' does not exist.")
            

        # Display success message
        messages.success(request, "Points added successfully!")
        return redirect('submit_points')  # Redirect back to the same page
    
    print("aut",request.user.is_authenticated)
    # Pass user's first name to the template
    user_name = request.user.first_name if request.user.is_authenticated else "User"
    print('USername' ,user_name)

    return render(request, 'add_points.html',{'e': e})  # Render the template for GET requests

from django.contrib.auth.hashers import make_password
def register(request):
    if request.method == 'POST':
        cust_user_id = generate_random_code()
        password = make_password(request.POST['password'])
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        puser = Employee(cust_user_id=cust_user_id,mobile = mobile, email = email, fname = fname, lname = lname,age=age, password = password ,is_user=True )
        puser.save()
        role = Role(email=email,role_name='User')
        role.save()

        name = fname + " " + lname

        return redirect('/login/')
    context = {
        'generated_user_id': generate_random_code(),
    }
    return render(request,'register.html',context)


import secrets
import string   
def generate_random_code(prefix="USER",length=2):
    alphabet = string.digits
    return prefix + ''.join(secrets.choice(alphabet) for _ in range(length))


def add_user(request):
    q = Employee.objects.all()
    print("q",q)
    cust_user_id = generate_random_code()
    print("cust",cust_user_id)
    if request.method == 'POST':
        # cust_user_id = request.POST.get('cust_user_id')
        password = make_password(request.POST['password'])
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        user = Employee(cust_user_id=cust_user_id,password=password,mobile = mobile, email = email, fname = fname, lname = lname,age=age ,is_user=True )
        user.save()
        role = Role(email=email,role_name='User')
        role.save()

    context = {
        'q':q,
    }    

    return render(request,'add_user.html',context)


# def submit_points(request):
#     q = AddApps.objects.last()
#     print("q",q)
#     if request.method == 'POST':
#         pid = request.POST.get('pid')
#         points = request.POST.get('points')
#         app_name = request.POST.get('app_name')
#         print("points",points)

#         p = Points(pid = pid,points = points, app_name = app_name)
#         p.save()

#     context = {
#         'q':q,
#     }
#     return render(request,'submit_points.html',context) 


def submit_points(request):
    q = AddApps.objects.last()  # Fetch the latest AddApps instance
    print("q", q)
    
    # last_app_name = request.session.get('last_added_app', None)
    # print("last app added",last_app_name)
    
    # mm = AddApps.objects.filter(app_name=last_app_name)
    # print("mm",mm)

    
    if request.method == 'POST':
        # pid = request.POST.get('pid')
        points = request.POST.get('points')
        app_name_str = request.POST.get('app_name')  # Get app_name as a string
        print("points", points)

        # pp = Points(points=points,app_name=app_name_str)
        # pp.save()

        try:
            # Fetch the corresponding AddApps instance
            app_instance = AddApps.objects.get(app_name=app_name_str)
            
            # Save the Points instance
            p = Points(points=points, app_name=app_instance)
            p.save()
            return redirect('add_points')
        except AddApps.DoesNotExist:
            # Handle case where the AddApps instance does not exist
            print(f"AddApps with name '{app_name_str}' does not exist.")
            return render(request, 'submit_points.html', {
                'q': q,
                'error_message': f"App name '{app_name_str}' not found. Please ensure the app exists."
            })

    context = {
        'q': q,
        # 'last_app_name':last_app_name,
    }
    return render(request, 'submit_points.html',context)


def all_users(request):
    q = Employee.objects.filter(is_user=True).all()
    print("users",q)
    role = Role.objects.all()
    print("rr",role)
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        print('role_name',role_name)
    context = {
        'q':q,
        'role':role,
    }
    return render(request,'all_users.html',context)


from django.shortcuts import redirect
from django.contrib import messages
from .models import Role  # Import your Role model

def change_role(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("emmm",email)
        new_role = request.POST.get('new_role')

        try:
            use = Employee.objects.get(email=email)
            print("use",use)
            user_role = Role.objects.get(email=email)
            print('uuser_role',user_role)
            user_role.role_name = new_role
            user_role.save()
            messages.success(request, f"Role updated successfully for {email}")
        except Role.DoesNotExist:
            messages.error(request, "User not found!")

    return redirect('all_users')  # Replace with your actual users list view name

from django.contrib import messages
def delete_user(request,cust_user_id):
    cus = Employee.objects.get(cust_user_id=cust_user_id)
    cus.delete()
    mm = Role.objects.get(email=cus.email)
    print("mm",mm)
    mm.delete()
    messages.success(request, "User is deleted successfully.") 
    return redirect('/all_users/')
    

def admin_logout(request):
    if request.user.is_authenticated :
        logout(request)
    return redirect('/login/')