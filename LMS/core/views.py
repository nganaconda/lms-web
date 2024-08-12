from django.shortcuts import render,redirect
from django.db import connection
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from django.contrib import messages
import logging
from django.http import HttpResponse
from .models import Users
from django.db import connections
import mysql.connector
from operator import itemgetter
from django.contrib.auth.hashers import make_password
import hashlib
from pyexpat.errors import messages
import secrets
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from .models import Users
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from core.models import Test, Question, Attribute, Users, Professor, Student, TestScore, ClassGroup

User = get_user_model()
class LoginAndRegister():
    username="admin"
    first_name="admin"
    last_name="admin"
    email="admin@aueb.gr"
    password="R3nd0mP@ssw0rd!"
    is_admin=True

    if Users.objects.filter(username=username).exists():
                print('Username already exists.')
    else:
                # with connection.cursor() as cursor:
                #             cursor.execute(
                #                 """
                #                 INSERT INTO users (gid, username, first_name, last_name, email, password, is_admin)
                #                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                #                 """,
                #                 [str(uuid.uuid4()),username,first_name,last_name,email,password,is_admin]
                #             )
                
                user = Users(username=username, first_name=first_name, last_name=last_name, email=email, is_admin=is_admin)
                user.set_password(password)
                user.save()

    username="f3312305"
    first_name="student"
    last_name="student"
    email="student@aueb.gr"
    password="R3nd0mP@ssw0rdForStudent!"
    is_admin=False

    if Users.objects.filter(username=username).exists():
                print('Username already exists.')
    else:
                # with connection.cursor() as cursor:
                #             cursor.execute(
                #                 """
                #                 INSERT INTO users (gid, username, first_name, last_name, email, password, is_admin)
                #                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                #                 """,
                #                 [str(uuid.uuid4()),username,first_name,last_name,email,password,is_admin]
                #             )
                
                user = Users(username=username, first_name=first_name, last_name=last_name, email=email, is_admin=is_admin)
                user.set_password(password)
                user.save()

    def login(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            con = mysql.connector.connect(host="localhost", user="root", passwd="gate123@A", database="LMSDB")
            cursor = con.cursor()

            try:
                cursor.execute("SELECT password FROM users WHERE username=%s --", [username])
                row = cursor.fetchone()
                
                if row is not None:
                    password_saved = row[0]
                    is_password_valid = check_password(password, password_saved)

                    if is_password_valid:
                        request.session['username'] = username
                        
                        Rb = generate_nonce(10)
                        request.session['Rb'] = Rb
                        return redirect('portfolio')
                    else:
                        messages.error(request, "Invalid username or password.")
                else:
                    messages.error(request, "Invalid username or password.")

            except mysql.connector.Error as err:
                messages.error(request, "An error occurred during login.")

            finally:
                cursor.close()
                con.close()

        return render(request, 'core/login.html')
   
    def welcome(request):
        return render(request,'core/welcome.html')     
    
    def register(request):
        if request.method == "POST":
            username = request.POST.get('username')

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not (username and first_name and last_name and email and password):
                messages.error(request, 'Please fill in all fields.')
                return redirect('register')

            user = Users(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()

            messages.success(request, 'Registration is done. Please go to the login page.')
            return redirect('login')
        
        return render(request, 'core/registration.html')


def generate_nonce(length):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def portfolio(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        contextNow = {
             'username': username
        }

        if user.is_admin:  # Assuming `is_admin` is True for professors
            try:
                professor = Professor.objects.get(user=user)

                # Retrieve all Test objects associated with this professor
                tests = Test.objects.filter(professor=professor).order_by('-createdAt')
                tests_info = []
                for test in tests:
                    test_scores = TestScore.objects.filter(test=test)
                    average_score = 0
                    no_of_scores = 0
                    
                    for test_score in test_scores:
                         average_score += test_score.result
                         no_of_scores += 1
                    
                    average_score = average_score / no_of_scores

                    tests_info.append({
                         'gid': test.gid,
                         'name': test.test_name,
                         'average': average_score,
                         'date': test.createdAt
                    })
                
                # Add the list to the context
                contextNow['tests_info'] = tests_info

                return render(request, 'core/professor_portfolio.html', contextNow)
            except Professor.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate
        else:  # Non-admin users are students
            try:
                student = Student.objects.get(user=user)

                # Retrieve all TestScore objects associated with this student
                test_scores = TestScore.objects.filter(student=student).select_related('test').order_by('-test__createdAt')

                # Prepare a list of tests with their GIDs and names
                tests_info = []
                for test_score in test_scores:
                    test = test_score.test
                    tests_info.append({
                        'gid': test.gid,
                        'name': test.test_name,
                        'score': test_score.result,
                        'date': test.createdAt
                    })
                
                # Add the list to the context
                contextNow['tests_info'] = tests_info

                return render(request, 'core/student_portfolio.html', contextNow)
            except Student.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate

    # try:
    #     cursor.execute("SELECT password FROM users WHERE username=%s --", [username])
    #     row = cursor.fetchone()
        
    #     if row is not None:
    #         password_saved = row[0]
    #         is_password_valid = check_password(password, password_saved)

    #         if is_password_valid:
    #             request.session['username'] = username
                
    #             Rb = generate_nonce(10)
    #             request.session['Rb'] = Rb
    #             return redirect('portfolio')
    #         else:
    #             messages.error(request, "Invalid username or password.")
    #     else:
    #         messages.error(request, "Invalid username or password.")

    # except mysql.connector.Error as err:
    #     messages.error(request, "An error occurred during login.")

    
    # Rb = generate_nonce(10)
    # contextNow = {
    #         'username': username,
    #         'Rb': Rb
    #     }
    # if request.method == 'POST':
    #     # Step 1: Generate random strings Ra and Rb
    #     Ra = generate_nonce(10)
    #     request.session['Ra'] = Ra
    #     request.session['Rb'] = Rb
        
    #     # Step 2: Anne rolls a dice (simulation)
    #     roll_the_dice_client  = secrets.choice('123456')

    #     # Store relevant session data
    #     request.session['roll_the_dice_client'] = roll_the_dice_client

    #     return redirect('ask_server')

    # return render(request, 'core/portfolio.html', contextNow)


def profile_view(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        contextNow = {
             'username': username
        }

        # Fetch common user info
        full_name = f"{user.first_name} {user.last_name}"
        username = user.username
        email = user.email

        if user.is_admin:  # Assuming `is_admin` is True for professors
            try:
                professor = Professor.objects.get(user=user)
                department = professor.department
                reg_number = ""  # Professors don't have a reg number, leave as empty
                year = ""  # Professors don't have a year, leave as empty
            except Professor.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate
        else:  # Non-admin users are students
            try:
                student = Student.objects.get(user=user)
                student = Student.objects.get(user=user)
                reg_number = student.reg_number
                year = student.year
                department = ""  # Students don't have a department, leave as empty
            except Student.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate
        
        contextNow = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'reg_number': reg_number,
            'department': department,
            'year': year,
        }

        return render(request, 'core/profile.html', contextNow)
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


def delete_user_view(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        user.delete()
        return redirect('login')  # Redirect to login page after deletion

    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate



def ask_server(request):
    username = request.session.get('username')
    Ra = request.session.get('Ra')
    Rb = request.session.get('Rb')
    roll_the_dice_client = request.session.get('roll_the_dice_client')

    # Step 4: Calculate Hcommit = SHA256(dice_result || Ra || Rb)
    message = f"{roll_the_dice_client}{Ra}{Rb}"
    request.session['message'] = message
    Hcommit = hashlib.sha256(message.encode('utf-8')).hexdigest()

    context = {
        'username': username,
        'message': message,
        'roll_the_dice_client': roll_the_dice_client,
        'Ra': Ra,
        'Rb': Rb,
        'Hcommit': Hcommit,
        'roll_the_dice_server': 0
    }

    request.session['Hcommit'] = Hcommit

    return render(request, 'core/ask_server.html', context)


def calculate_winner(request):
    # Step 7: Bill reveals his dice roll result (simulated by the user)
    roll_the_dice_server = secrets.choice('123456')
    
    username = request.session.get('username')
    Ra = request.session.get('Ra')
    Rb = request.session.get('Rb')
    Hcommit = request.session.get('Hcommit')
    message = request.session.get('message')
    roll_the_dice_client = request.session.get('roll_the_dice_client')

    if not all([Ra, Rb, Hcommit, roll_the_dice_client]):
        return HttpResponse("Error: Session data missing. Please restart the game.")

    # Step 8: Anne compares dice_result with bill_dice_result to determine the winner
    if roll_the_dice_client > roll_the_dice_server:
        winner = f"{username} won!"
    elif roll_the_dice_client < roll_the_dice_server:
        winner = "Server won!"
    else:
        winner = "It's a tie! No winner."

    # Step 9: Anne sends the string "dice_result || Ra || Rb" to Bill
    message_to_bill = f"{roll_the_dice_client}{Ra}{Rb}"
    request.session['roll_the_dice_server'] = roll_the_dice_server

    context = {
        'username': username,
        'winner': winner,
        'roll_the_dice_server': roll_the_dice_server,
        'roll_the_dice_client': roll_the_dice_client,
        'message_to_bill': message_to_bill,
        'clientSHA256': Hcommit,
        'message': message,
        'nonceClient': Ra,
        'nonceServer': Rb
    }

    request.session['message_to_bill'] = message_to_bill
    request.session['winner'] = winner

    return render(request, 'core/calculate_winner.html', context)


def result(request):
    username = request.session.get('username')
    Ra = request.session.get('Ra')
    Rb = request.session.get('Rb')
    Hcommit = request.session.get('Hcommit')
    roll_the_dice_client = request.session.get('roll_the_dice_client')
    roll_the_dice_server = request.session.get('roll_the_dice_server')
    winner = request.session.get('winner')
    message_to_bill = request.session.get('message_to_bill')

    if not all([Ra, Rb, Hcommit, roll_the_dice_client]):
        return HttpResponse("Error: Session data missing. Please restart the game.")

    if request.method == 'POST':
        # Step 10: Bill checks if Anne was truthful
        H2 = hashlib.sha256(message_to_bill.encode('utf-8')).hexdigest()
        truthful = (H2 == Hcommit)

        context = {
            'username': username,
            'winner': winner,
            'roll_the_dice_server': roll_the_dice_server,
            'roll_the_dice_client': roll_the_dice_client,
            'message_to_bill': message_to_bill,
            'truthful': truthful,
            'clientSHA256': Hcommit,
            'serverSHA256': H2,
            'nonceClient': Ra,
            'nonceServer': Rb
        }

        return render(request, 'core/result.html', context)