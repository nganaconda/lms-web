from django.shortcuts import render,redirect
from django.db import connection
from django.db import transaction
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render,redirect
from django.contrib import messages
from django import forms
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
from core.models import Test, Question, Attribute, Users, Professor, Student, CompletedTest, CompletedTestAnswer, ClassGroup, TestQuestion
from .forms import QuestionForm, AttributeFormSet, TestForm
import random
import math
import logging
from datetime import datetime


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
            email = request.POST.get('email')
            role = request.POST.get('role')  # Get the user role (student or professor)

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            if Users.objects.filter(email=email).exists():
                messages.error(request, 'Email is already used.')
                return redirect('register')
            
            # Check if the professor_id is present when the role is professor
            professor_id = request.POST.get('professor_id') if role == 'professor' else None
            department = request.POST.get('department') if role == 'professor' else None
            
            if role == 'professor':
                if Professor.objects.filter(professorID=professor_id).exists():
                    messages.error(request, 'Professor ID already exists.')
                    return redirect('register')

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            repassword = request.POST.get('re-password')

            if not (username and first_name and last_name and email and password and repassword):
                messages.error(request, 'Please fill in all fields.')
                return redirect('register')
            
            if password != repassword:
                messages.error(request, 'The password and re-entered password are not the same.')
                return redirect('register')
            
            # Ensure professor_id is provided if the role is professor
            if role == 'professor' and not professor_id:
                messages.error(request, 'Professor ID is required for professors.')
                return redirect('register')

            user = Users(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            
            user.save()

            if role == 'professor':
                user.is_admin = True
                user.save()
                Professor.objects.create(
                    professorID = professor_id,
                    department = department,
                    user = user
                )
            elif role == 'student':
                Student.objects.create(
                    reg_number = StudentRegistry.generate_reg_number(),
                    year = datetime.now().year,
                    user = user
                )

            messages.success(request, 'Registration is done. Please go to the login page.')
            return redirect('login')
        
        return render(request, 'core/registration.html')


class StudentRegistry:
    counter = 3000000  # Starting value for the global counter

    @classmethod
    def generate_reg_number(cls):
        reg_number = f"f{cls.counter:07d}"  # Format to "fXXXXXXX" with leading zeros
        cls.counter += 1  # Increment the counter for the next call

        
        if Student.objects.filter(reg_number=reg_number).exists():
            students = Student.objects.all()
            current_reg = 0

            if students:
                for student in students:
                    if int(student.reg_number.replace('f', '')) > current_reg:
                        current_reg = int(student.reg_number.replace('f', ''))
                reg_number = 'f' + str(current_reg + 1)
        
        return reg_number


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
                    completed_tests = CompletedTest.objects.filter(test=test)
                    average_score = 0
                    no_of_scores = 0
                    
                    for completed_test in completed_tests:
                         average_score += completed_test.score
                         no_of_scores += 1
                    
                    if no_of_scores > 0:
                        average_score = average_score / no_of_scores
                    else: 
                        average_score = 0

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

                # Retrieve all CompletedTest objects associated with this student
                completed_tests = CompletedTest.objects.filter(student=student).select_related('test').order_by('-test__createdAt')

                # Prepare a list of tests with their GIDs and names
                tests_info = []
                for completed_test in completed_tests:
                    test = completed_test.test
                    tests_info.append({
                        'gid': test.gid,
                        'name': test.test_name,
                        'score': completed_test.score,
                        'date': test.createdAt,
                        'completed_test_gid': completed_test.gid
                    })
                
                # Add the list to the context
                contextNow['tests_info'] = tests_info

                return render(request, 'core/student_portfolio.html', contextNow)
            except Student.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate
    

def newTests(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        contextNow = {
             'username': username
        }

        if not user.is_admin:
            try:
                student = Student.objects.get(user=user)

                classGroup = ClassGroup.objects.filter(students=student).first()

                # Retrieve all Test objects associated with this student
                allStudentTests = Test.objects.filter(classGroup=classGroup)
                allStudentCompletedTests = CompletedTest.objects.filter(student=student).select_related('test').order_by('-test__createdAt')

                tests_info = []
                for test in allStudentTests:
                    isCompleted = False

                    for completedTest in allStudentCompletedTests:
                        if test.gid == completedTest.test.gid:
                            isCompleted = True
                    
                    if isCompleted == False:
                        tests_info.append({
                            'gid': test.gid,
                            'name': test.test_name,
                            'date': test.createdAt,
                        })
                
                # Add the list to the context
                contextNow['tests_info'] = tests_info

                return render(request, 'core/newTests.html', contextNow)
            except Student.DoesNotExist:
                return redirect('403.html')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate


def addTest(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:  # Assuming `is_admin` is True for professors
        
            professor = Professor.objects.get(user=user)

            if request.method == 'POST':
                form = TestForm(request.POST, professor=professor)
 
                if form.is_valid():
                    test = form.save(commit=False)
                    test.professor = professor  # Assign the logged-in professor
                    test.save()

                    # Retrieve the test criteria
                    test_type = test.type
                    test_difficulty = test.questions_dif
                    questions_required = test.questions_no

                    # Check if there are questions of the specified type
                    type_questions = Question.objects.filter(
                        type=test_type,
                        professor=professor
                    )
                    if type_questions.count() == 0:
                        test.delete()
                        # Add an error to the form's questions_no field
                        form.add_error('type', forms.ValidationError(
                            f'There are no questions available of type "{test_type}".'
                        ))
                    else:
                        # Query for questions that match the criteria
                        matching_questions = Question.objects.filter(
                            type=test_type,
                            difficulty=test_difficulty,
                            professor=professor
                        )

                        # Check if enough questions are available
                        if matching_questions.count() >= questions_required:
                            # Randomly select the required number of questions
                            selected_questions = random.sample(list(matching_questions), questions_required)
                            
                            # Calculate the weight for each question
                            weight = round(1/questions_required, 2)

                            # Save each question in the `TestQuestion` table with the assigned weight
                            for question in selected_questions:
                                TestQuestion.objects.create(
                                    test=test,
                                    question=question,
                                    weight=weight
                                )
                            
                            test.questions.set(selected_questions)  # Assign questions to the test
                            test.save()
                            return redirect('viewCreated', test_gid=test.gid)  # Redirect to test view
                        else:
                            test.delete()
                            # Add an error to the form's questions_no field
                            form.add_error('questions_no', forms.ValidationError(
                                f'Not enough questions available of type "{test_type}" and difficulty "{test_difficulty}".'
                            ))

            else:
                form = TestForm(professor=professor)
 
            contextNow = {
                'username': username,
                'form': form,
            }

            return render(request, 'core/addTest.html', contextNow)

    except Professor.DoesNotExist:
        return redirect(request, '403.html')  # Return a 403 page if the user is not a professor


def remakeTest(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:
            professor = Professor.objects.get(user=user)

            # Retrieve the existing test
            test = get_object_or_404(Test, gid=test_gid)
            
            # Retrieve the test criteria
            test_type = test.type
            test_difficulty = test.questions_dif
            questions_required = test.questions_no

            # Delete the existing test
            test.questions.clear()

            # Query for questions that match the criteria
            matching_questions = Question.objects.filter(
                type=test_type,
                difficulty=test_difficulty,
                professor=professor
            )

            # Randomly select the required number of questions
            selected_questions = random.sample(list(matching_questions), questions_required)
            
            # Calculate the weight for each question
            weight = round(1/questions_required, 2)

            # Save each question in the `TestQuestion` table with the assigned weight
            for question in selected_questions:
                TestQuestion.objects.create(
                    test=test,
                    question=question,
                    weight=weight
                )
            
            test.questions.set(selected_questions)  # Assign questions to the test
            test.save()
            
            # Redirect to the updated test analysis view
            return redirect('viewCreated', test_gid=test.gid)

    except Professor.DoesNotExist:
        return redirect('403')


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

                contextNow = {
                    'full_name': full_name,
                    'username': username,
                    'email': email,
                    'department': department,
                    'professorID': professor.professorID
                }

                return render(request, 'core/prof_profile.html', contextNow)

            except Professor.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate
        else:  # Non-admin users are students
            try:
                student = Student.objects.get(user=user)
                reg_number = student.reg_number
                year = student.year

                contextNow = {
                    'full_name': full_name,
                    'username': username,
                    'email': email,
                    'reg_number': reg_number,
                    'year': year,
                }

                return render(request, 'core/stud_profile.html', contextNow)

            except Student.DoesNotExist:
                return redirect('error_page')  # Or handle as appropriate
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


def delete_user_view(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:
            try: 
                professor = Professor.objects.get(user=user)
                professor.delete()
            except Professor.DoesNotExist:
                return redirect('error pages')
        else:
            try: 
                student = Student.objects.get(user=user)
                student.delete()
            except Student.DoesNotExist:
                return redirect('error pages')

        user.delete()
        return redirect('login')  # Redirect to login page after deletion

    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


def completed_test_view(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        # Retrieve the completed test using the provided GID
        completed_test = get_object_or_404(CompletedTest, gid=test_gid)
        
        # Get all the answers related to this completed test
        completed_test_answers = CompletedTestAnswer.objects.filter(completedTest=completed_test).select_related('question', 'attribute')
        
        # Prepare the data structure to be passed to the template
        questions_info = []
        
        # Iterate through each question in the test
        for question in completed_test.test.questions.all():
            # Get all answers (attributes) related to the question
            attributes = question.attributes.all()
            question_data = {
                'question_text': question.question,
                'question_weight': get_test_question(str(completed_test.test.gid).replace('-', ''), str(question.gid).replace('-', '')),
                'attributes': []
            }
            original_question = Question.objects.get(question=question.question)
            
            for attribute in attributes:
                # Find the selected answer and whether it was correct
                selected_answer = completed_test_answers.filter(question=question, attribute=attribute).first()
                rightAnswer = original_question.rightAnswer
                is_selected = selected_answer is not None
                is_correct = selected_answer.is_correct if selected_answer else False
                
                question_data['attributes'].append({
                    'answer_text': attribute.answer,
                    'is_selected': is_selected,
                    'is_correct': is_correct,
                    'rightAnswer': rightAnswer.answer
                })
            
            questions_info.append(question_data)
        
        context = {
            'username': username,
            'test_name': completed_test.test.test_name,
            'score': completed_test.score,
            'completion_date': completed_test.completion_date,
            'questions_info': questions_info
        }
        
        return render(request, 'core/completed_test.html', context)
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


def test_view(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        # Retrieve the test using the provided GID
        test = get_object_or_404(Test, gid=test_gid)
        
        # Get all the questions related to this completed test
        test_questions = test.questions.all()
        
        # Prepare the data structure to be passed to the template
        questions_info = []
        
        # Iterate through each question in the test
        for question in test_questions:
            # Get all answers (attributes) related to the question
            attributes = question.attributes.all()
            question_data = {
                'question_text': question.question,
                'question_weight': get_test_question(str(test_gid).replace('-', ''), str(question.gid).replace('-', '')),
                'attributes': []
            }
            original_question = Question.objects.get(question=question.question)
            
            for attribute in attributes:
                # Find the selected answer and whether it was correct
                rightAnswer = original_question.rightAnswer
                
                question_data['attributes'].append({
                    'answer_text': attribute.answer,
                    'rightAnswer': rightAnswer.answer
                })
            
            questions_info.append(question_data)
        
        context = {
            'username': username,
            'test_name': test.test_name,
            'createdAt': test.createdAt,
            'questions_info': questions_info
        }
        
        return render(request, 'core/test_analysis.html', context)
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate
    

def get_test_question(test_id, question_id):
    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="gate123@A", database="LMSDB")
        cursor = con.cursor()
        with connection.cursor() as cursor:
            cursor.execute('SELECT weight FROM tests_questions WHERE test_id=%s AND question_id=%s --', [test_id , question_id])
            row = cursor.fetchone()
            
            if row is not None:
                weight=row[0]
                
                return weight
            return 1
    except Exception as e:
        print(f"Error executing raw SQL: {e}")
        return None


def viewCreated(request, test_gid):
    logger = logging.getLogger('django')
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        # Retrieve the test using the provided GID
        test = get_object_or_404(Test, gid=test_gid)
        
        # Get all the questions related to this completed test
        test_questions = test.questions.all()
        
        # Prepare the data structure to be passed to the template
        questions_info = []
        
        # Iterate through each question in the test
        for question in test_questions:
            original_question = Question.objects.get(question=question.question)
            testgid = str(test_gid).replace('-', '')
            questiongid = str(original_question.gid).replace('-', '')

            # Get all answers (attributes) related to the question
            attributes = question.attributes.all()
            question_data = {
                'question_text': question.question,
                'weight': get_test_question(testgid, questiongid),
                'attributes': []
            }
            
            for attribute in attributes:
                # Find the selected answer and whether it was correct
                rightAnswer = original_question.rightAnswer
                
                question_data['attributes'].append({
                    'answer_text': attribute.answer,
                    'rightAnswer': rightAnswer.answer
                })
            
            questions_info.append(question_data)
        
        context = {
            'username': username,
            'test_name': test.test_name,
            'createdAt': test.createdAt,
            'questions_info': questions_info,
            'test_gid': test.gid
        }
        
        return render(request, 'core/createdTest_analysis.html', context)
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


@transaction.atomic
def save_test_weights(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="gate123@A", database="LMSDB")
        cursor = con.cursor()

        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)
    
        if request.method == 'POST':
            # Retrieve the test
            test = get_object_or_404(Test, gid=test_gid)
            
            # Get all questions related to the test
            #test_questions = TestQuestion.objects.filter(test=test)
            test_questions = []

            test_id = str(test_gid).replace('-', '')

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM tests_questions
                    WHERE test_id = %s
                """, [test_id])
                rows = cursor.fetchall()
                
                if rows:
                    for row in rows:
                        test_question = TestQuestion(
                            test_id=row[0],
                            question_id=row[1],
                            weight=row[2]
                        
                        )
                        test_questions.append(test_question)
            
            # Retrieve the weights from the POST data
            weights = request.POST.getlist('weights')
            
            # Ensure we have the same number of weights as there are questions
            if len(weights) != len(test_questions):
                return JsonResponse({'error': 'Mismatch between number of questions and weights.'}, status=400)

            # Sum the weights and validate
            total_weight = sum([float(w) for w in weights if w])
            if round(total_weight, 2) != 1.00:

                questions_info = []
            
                # Iterate through each question in the test
                for question in test_questions:
                    original_question = Question.objects.get(question=question.question)
                    testgid = str(test_gid).replace('-', '')
                    questiongid = str(original_question.gid).replace('-', '')

                    # Get all answers (attributes) related to the question
                    attributes = question.attributes.all()
                    question_data = {
                        'question_text': question.question,
                        'weight': get_test_question(testgid, questiongid),
                        'attributes': []
                    }
                    
                    for attribute in attributes:
                        # Find the selected answer and whether it was correct
                        rightAnswer = original_question.rightAnswer
                        
                        question_data['attributes'].append({
                            'answer_text': attribute.answer,
                            'rightAnswer': rightAnswer.answer
                        })
                    
                    questions_info.append(question_data)
                
                context = {
                    'username': username,
                    'test_name': test.test_name,
                    'createdAt': test.createdAt,
                    'questions_info': questions_info,
                    'test_gid': test.gid,
                    'error_message': 'The total weight must equal 1. Please correct the values.'
                }

                return render(request, 'core/createdTest_analysis.html', context)
            
            # Update the weights in the database
            for i, test_question in enumerate(test_questions):
                                
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE tests_questions SET weight = %s
                        WHERE test_id = %s and question_id = %s
                    """, [weights[i], test_id, str(test_question.question_id).replace('-', '')])
            
            # Redirect to the same page or wherever appropriate after successful save
            return redirect('portfolio')
        
        return redirect('viewCreated', test_gid=test_gid)
    
    except Users.DoesNotExist:
        return redirect('error_page')  # Or handle as appropriate


def my_test_questions(request):
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

                # Get distinct question types
                question_types = Question.objects.filter(professor=professor).values_list('type', flat=True).distinct()

                context = {
                    'username': username,
                    'question_types': question_types
                }

                return render(request, 'core/my_questions_types.html', context)

            except Professor.DoesNotExist:
                return redirect(request, '403.html')  # Return a 403 page if the user is not a professor
            
    except Users.DoesNotExist:
        return redirect(request, '403.html')  # Return a 403 page if the user is not a professor


def addQuestion(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:  # Assuming `is_admin` is True for professors
        
            professor = Professor.objects.get(user=user)

            if request.method == 'POST':
                form = QuestionForm(request.POST)
                formset = AttributeFormSet(request.POST, queryset=Attribute.objects.none())  # Start with an empty queryset

                if form.is_valid() and formset.is_valid():
                    question = form.save(commit=False)
                    question.professor = professor  # Assign the logged-in professor
                    question.save()

                    # Handle the right answer
                    right_answer_text = form.cleaned_data['rightAnswerText']
                    right_answer = Attribute.objects.create(answer=right_answer_text)
                    question.rightAnswer = right_answer
                    question.attributes.add(right_answer)

                    # Save each attribute and link it to the question
                    for attribute_form in formset:
                        if attribute_form.cleaned_data:
                            attribute = attribute_form.save()
                            question.attributes.add(attribute)

                    question.save()
                    return redirect('questions_by_type', type=question.type)

            else:
                form = QuestionForm()
                formset = AttributeFormSet(queryset=Attribute.objects.none())  # Start with an empty queryset

            contextNow = {
                'username': username,
                'form': form,
                'formset': formset,
            }

            return render(request, 'core/addQuestion.html', contextNow)

    except Professor.DoesNotExist:
        return redirect(request, '403.html')  # Return a 403 page if the user is not a professor


def questions_by_type(request, type):
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

                questions = Question.objects.filter(type=type, professor=professor)

                # Prepare a list of tests with their GIDs and names
                questions_info = []
                for question in questions:
                    right_answer = question.rightAnswer.answer
                    questions_info.append({
                        'gid': question.gid,
                        'question': question.question,
                        'difficulty': question.difficulty,
                        'type': question.type,
                        'rightanswer': right_answer
                    })
                
                # Add the list to the context
                contextNow['questions_info'] = questions_info

                return render(request, 'core/questions_by_type.html', contextNow)

            except Professor.DoesNotExist:
                return redirect(request, '403.html')  # Return a 403 page if the user is not a professor
            
    except Users.DoesNotExist:
        return redirect(request, '403.html')  # Return a 403 page if the user is not a professor


def question_analysis(request, type, question_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        # Retrieve the question using the provided GID
        question = get_object_or_404(Question, gid=question_gid)
        
        # Get all answers (attributes) related to the question
        attributes = question.attributes.all()
        question_data = {
            'question_text': question.question,
            'difficulty': question.difficulty,
            'rightanswer': question.rightAnswer.answer,
            'attributes': []
        }
        
        for attribute in attributes:            
            question_data['attributes'].append({
                'answer_text': attribute.answer
            })
                
        context = {
            'username': username,
            'question_data': question_data
        }
        
        return render(request, 'core/question_analysis.html', context)
    
    except Users.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate


def completeTest(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        user = Users.objects.get(username=username)
        student = Student.objects.get(user=user)

        # Fetch the test using the provided gid
        test = get_object_or_404(Test, gid=test_gid)

        # Fetch the questions related to the test
        questions = test.questions.all()

        # Prepare the data structure to be passed to the template
        questions_info = []
        
        # Iterate through each question in the test
        for question in questions:
            original_question = Question.objects.get(question=question.question)
            testgid = str(test_gid).replace('-', '')
            questiongid = str(original_question.gid).replace('-', '')

            # Get all answers (attributes) related to the question
            attributes = question.attributes.all()
            question_data = {
                'question_text': question.question,
                'gid': question.gid,
                'question_weight': get_test_question(testgid, questiongid),
                'attributes': []
            }
            
            for attribute in attributes:
                # Find the selected answer and whether it was correct
                rightAnswer = original_question.rightAnswer
                
                question_data['attributes'].append({
                    'gid': attribute.gid,
                    'answer_text': attribute.answer,
                    'rightAnswer': rightAnswer.answer
                })
            
            questions_info.append(question_data)

        context = {
            'username': username,
            'test': test,
            'questions': questions_info,
        }

        return render(request, 'core/completeTest.html', context)

    except Users.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate
    except Student.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate


def submitTest(request, test_gid):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        user = Users.objects.get(username=username)
        student = Student.objects.get(user=user)

        test = get_object_or_404(Test, gid=test_gid)

        if request.method == 'POST':
            score = 0
            questions = test.questions.all()
            total_questions = len(questions)

            # Create a CompletedTest record
            completedTest = CompletedTest.objects.create(
                test=test,
                student=student,
                score=score
            )

            for question in questions:

                selected_answer_gid = request.POST.get(str(question.gid))
                if selected_answer_gid:
                    selected_answer = Attribute.objects.get(gid=selected_answer_gid)
                    
                    completedTestAnswer = CompletedTestAnswer.objects.create(
                    question=question,
                    completedTest=completedTest,
                    is_correct=False,
                    attribute=selected_answer
                    )

                    if selected_answer == question.rightAnswer:
                        weight = get_test_question(str(test_gid).replace('-', ''), str(question.gid).replace('-', ''))
                        score += weight
                        completedTestAnswer.is_correct=True
                        completedTestAnswer.save()
            
            # Calculate the score as a percentage
            score_percentage = score * 10

            completedTest.score = score_percentage
            completedTest.save()
            
            messages.success(request, f'Test completed successfully! Your score: {score_percentage}%')
            return redirect('newTests')

    except Users.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate
    except Student.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate
    

def viewGrades(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        contextNow = {
             'username': username
        }

        username = user.username

        if not user.is_admin:  # Assuming `is_admin` is False for students
            try:
                student = Student.objects.get(user=user)

                # Retrieve all completed tests for the student
                completed_tests = CompletedTest.objects.filter(student=student)

                # Filter out the tests that are passed (scores >= 5)
                passing_tests = completed_tests.filter(score__gte=5)

                # Calculate the overall average score (considering only passing scores)
                if passing_tests.exists():
                    overall_average = passing_tests.aggregate(Avg('score'))['score__avg']
                    # Round to 2 decimal places and use ceil to always round up
                    overall_average = math.ceil(overall_average * 100) / 100
                else:
                    overall_average = 0

                # Calculate the average scores by test type (for passing scores only)
                test_types = Test.objects.values_list('type', flat=True).distinct()
                type_averages = []
                
                for test_type in test_types:
                    # Get passing tests of this type
                    type_tests = passing_tests.filter(test__type=test_type)
                    if type_tests.exists():
                        avg_score = type_tests.aggregate(Avg('score'))['score__avg']
                        # Round the average score for each type
                        avg_score = math.ceil(avg_score * 100) / 100
                        type_averages.append({
                            'type': test_type,
                            'average_score': avg_score,
                            'tests': type_tests  # To show individual tests later
                        })
                        
                        # Add the list to the context
                        contextNow = {
                            'username': username,
                            'overall_average': overall_average,
                            'type_averages': type_averages
                        }

                        return render(request, 'core/viewGrades.html', contextNow)

            except Student.DoesNotExist:
                return redirect('403.html')  # Or handle as appropriate
    
    except Users.DoesNotExist:
        return redirect('403.html')  # Or handle as appropriate


def viewProfessorGrades(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:  # Assuming `is_admin` is True for professors
            try:
                professor = Professor.objects.get(user=user)

                # Get all class groups the professor is responsible for
                class_groups = professor.classGroups.all()

                class_group_averages = []

                for class_group in class_groups:
                    # Fetch all tests created by the professor for this class group
                    tests_in_class = Test.objects.filter(professor=professor, classGroup=class_group)
                    # Find all completed tests for this class group
                    completed_tests = CompletedTest.objects.filter(test__in=tests_in_class)
                    
                    if completed_tests.exists():
                        # Calculate the average score for all tests in the class group (including failed ones)
                        average_score = completed_tests.aggregate(Avg('score'))['score__avg']
                    else:
                        average_score = 0

                    class_group_averages.append({
                        'class_name': class_group.class_name,
                        'class_group_id': class_group.gid,
                        'average_score': round(average_score, 2),  # Rounding to 2 decimal places
                    })

                context = {
                    'username': username,
                    'class_group_averages': class_group_averages
                }

                return render(request, 'core/viewProfessorGrades.html', context)
    
            except Professor.DoesNotExist:
                return redirect('403.html')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('403.html')  # Handle non-existent user or redirect appropriately


def viewClassGroupTestTypeAverages(request, class_group_id):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:  # Assuming `is_admin` is True for professors
            try:
                professor = Professor.objects.get(user=user)
                class_group = ClassGroup.objects.get(gid=class_group_id)

                # Check if the professor is responsible for the class group
                if class_group not in professor.classGroups.all():
                    return redirect('403.html')

                # Fetch tests for the class group created by this professor
                tests_in_class = Test.objects.filter(professor=professor, classGroup=class_group)

                # Get the distinct test types
                test_types = tests_in_class.values_list('type', flat=True).distinct()

                test_type_averages = []
                for test_type in test_types:
                    # Fetch all tests of this type in the class group
                    tests_of_type = tests_in_class.filter(type=test_type)
                    # Find all completed tests of this type
                    completed_tests = CompletedTest.objects.filter(test__in=tests_of_type)

                    if completed_tests.exists():
                        # Calculate the average score for this test type
                        average_score = completed_tests.aggregate(Avg('score'))['score__avg']
                    else:
                        average_score = 0

                    test_type_averages.append({
                        'test_type': test_type,
                        'average_score': round(average_score, 2),  # Rounding to 2 decimal places
                    })

                context = {
                    'username': username,
                    'class_group_name': class_group.class_name,
                    'class_group_id': class_group_id,
                    'test_type_averages': test_type_averages
                }

                return render(request, 'core/viewClassGroupTestTypeAverages.html', context)
            except Professor.DoesNotExist:
                return redirect('403.html')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('403.html')  # Handle non-existent user or redirect appropriately


def viewClassGroupTestAverages(request, class_group_id, type):
    username = request.session.get('username')

    if not username:
        return redirect('login')  # Assuming there's a login view
    
    try:
        # Retrieve the user object from the Users model
        user = Users.objects.get(username=username)

        if user.is_admin:  # Assuming `is_admin` is True for professors
            try:
                professor = Professor.objects.get(user=user)
                class_group = ClassGroup.objects.get(gid=class_group_id)

                # Check if the professor is responsible for the class group
                if class_group not in professor.classGroups.all():
                    return redirect('403.html')

                # Fetch tests for the class group created by this professor and that are of this specific type
                tests_in_class = Test.objects.filter(professor=professor, classGroup=class_group, type=type).order_by('-createdAt')

                test_averages = []
                for test in tests_in_class:
                    # Find all completed tests
                    completed_tests = CompletedTest.objects.filter(test=test)

                    if completed_tests.exists():
                        # Calculate the average score for this test type
                        average_score = completed_tests.aggregate(Avg('score'))['score__avg']
                    else:
                        average_score = 0

                    test_averages.append({
                        'test_name': test.test_name,
                        'test_gid': test.gid,
                        'date': test.createdAt,
                        'average_score': round(average_score, 2),  # Rounding to 2 decimal places
                    })

                context = {
                    'username': username,
                    'class_group_name': class_group.class_name,
                    'class_group_gid': class_group_id,
                    'test_type': type,
                    'test_averages': test_averages
                }

                return render(request, 'core/viewClassGroupTestAverages.html', context)
            except Professor.DoesNotExist:
                return redirect('403.html')  # Or handle as appropriate

    except Users.DoesNotExist:
        return redirect('403.html')  # Handle non-existent user or redirect appropriately


def viewTestResults(request, test_gid, class_group_id, type):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        # Retrieve the user object
        user = Users.objects.get(username=username)

        if user.is_admin:
            try:
                professor = Professor.objects.get(user=user)
                class_group = ClassGroup.objects.get(gid=class_group_id)
                test = Test.objects.get(gid=test_gid)

                # Ensure the professor is responsible for the class group associated with the test
                if test.professor != professor:
                    return redirect('403.html')

                # Fetch all completed tests for this test
                completed_tests = CompletedTest.objects.filter(test=test).order_by('student__reg_number')

                test_results = []
                for completed_test in completed_tests:
                    student = completed_test.student
                    test_results.append({
                        'student_name': f"{student.user.first_name} {student.user.last_name}",
                        'reg_number': student.reg_number,
                        'score': completed_test.score,
                    })

                context = {
                    'username': username,
                    'class_group_name': class_group.class_name,
                    'class_group_gid': class_group_id,
                    'test_name': test.test_name,
                    'test_results': test_results
                }

                return render(request, 'core/viewTestResults.html', context)
            except (Professor.DoesNotExist, Test.DoesNotExist):
                return redirect('403.html')

    except Users.DoesNotExist:
        return redirect('403.html')