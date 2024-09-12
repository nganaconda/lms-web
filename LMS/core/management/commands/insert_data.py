import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Question, Attribute, Users, Professor, Student, CompletedTest, CompletedTestAnswer, ClassGroup
from datetime import datetime

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Create a test of type "math"
        test = Test.objects.create(
            gid=uuid.uuid4(),
            test_name='2024 Sep Exams Math',
            level=1,
            age=10,
            type='math',
            questions_no=3,
            questions_dif=4,
            createdAt=datetime(2024, 9, 14, 10, 0)
        )
        self.stdout.write(self.style.SUCCESS(f'Created Test: {test.gid}'))

        test1 = Test.objects.create(
            gid=uuid.uuid4(),
            test_name='2024 June Exams Math',
            level=2,
            age=10,
            type='math',
            questions_no=4,
            questions_dif=4,
            createdAt=datetime(2024, 6, 10, 9, 0)
        )

        # Sample questions and attributes
        questions_data = [
            {
                'question': 'What is 2 + 2?',
                'type': 'math',
                'difficulty': 1,
                'attributes': [
                    '2 + 2 = 4',
                    '4 is an even number',
                    '2 is a prime number',
                    'Addition of positive numbers'
                ],
                'rightAnswer': '2 + 2 = 4'
            },
            {
                'question': 'What is 5 - 3?',
                'type': 'math',
                'difficulty': 1,
                'attributes': [
                    '5 - 3 = 2',
                    '2 is an even number',
                    '5 is a prime number',
                    'Subtraction of positive numbers'
                ],
                'rightAnswer': '5 - 3 = 2'
            },
            {
                'question': 'What is 3 * 3?',
                'type': 'math',
                'difficulty': 2,
                'attributes': [
                    '3 * 3 = 9',
                    '9 is a square number',
                    '3 is a prime number',
                    'Multiplication of single digits'
                ],
                'rightAnswer': '3 * 3 = 9'
            }
        ]

        questions_dataJun = [
            {
                'question': 'What is the square root of 25?',
                'type': 'math',
                'difficulty': 4,
                'attributes': [
                    '50',
                    '25',
                    '1',
                    '5'
                ],
                'rightAnswer': '5'
            },
            {
                'question': 'What is 25000 / 100?',
                'type': 'math',
                'difficulty': 4,
                'attributes': [
                    '250',
                    '2500',
                    '2500000',
                    '125'
                ],
                'rightAnswer': '250'
            },
            {
                'question': 'What is 3! ?',
                'type': 'math',
                'difficulty': 4,
                'attributes': [
                    '3',
                    '1',
                    '6',
                    '9'
                ],
                'rightAnswer': '6'
            },
            {
                'question': 'How many sides are there in a square?',
                'type': 'math',
                'difficulty': 4,
                'attributes': [
                    '2 sides',
                    '4 sides',
                    '6 sides',
                    '1 side'
                ],
                'rightAnswer': '4 sides'
            }
        ]

        for q_data in questions_data:
            question = Question.objects.create(
                gid=uuid.uuid4(),
                question=q_data['question'],
                type=q_data['type'],
                difficulty=q_data['difficulty']
            )
            self.stdout.write(self.style.SUCCESS(f'Created Question: {question.gid}'))

            for attr in q_data['attributes']:
                attribute = Attribute.objects.create(
                    gid=uuid.uuid4(),
                    answer=attr
                )
                self.stdout.write(self.style.SUCCESS(f'Created Attribute: {attribute.gid}'))
                
                # Associate the question with attributes
                question.attributes.add(attribute)

                ansr = q_data['rightAnswer']
                self.stdout.write(self.style.SUCCESS(f'ATTR VALUE: {attr}'))
                self.stdout.write(self.style.SUCCESS(f'QDATA VALUE: {ansr}'))
                if attr == ansr:
                    self.stdout.write(self.style.SUCCESS(f'MPHKE'))
                    question.rightAnswer = attribute
                    question.save()

                self.stdout.write(self.style.SUCCESS(f'Linked Question {question.gid} with Attribute {attribute.gid}'))

            # Associate the test with questions
            test.questions.add(question)
            self.stdout.write(self.style.SUCCESS(f'Linked Test {test.gid} with Question {question.gid}'))

        for q_data in questions_dataJun:
            question = Question.objects.create(
                gid=uuid.uuid4(),
                question=q_data['question'],
                type=q_data['type'],
                difficulty=q_data['difficulty']
            )
            self.stdout.write(self.style.SUCCESS(f'Created Question: {question.gid}'))

            for attr in q_data['attributes']:
                attribute = Attribute.objects.create(
                    gid=uuid.uuid4(),
                    answer=attr
                )
                self.stdout.write(self.style.SUCCESS(f'Created Attribute: {attribute.gid}'))
                
                # Associate the question with attributes
                question.attributes.add(attribute)

                ansr = q_data['rightAnswer']
                self.stdout.write(self.style.SUCCESS(f'ATTR VALUE: {attr}'))
                self.stdout.write(self.style.SUCCESS(f'QDATA VALUE: {ansr}'))
                if attr == ansr:
                    self.stdout.write(self.style.SUCCESS(f'MPHKE'))
                    question.rightAnswer = attribute
                    question.save()

                self.stdout.write(self.style.SUCCESS(f'Linked Question {question.gid} with Attribute {attribute.gid}'))

            # Associate the test with questions
            test1.questions.add(question)
            self.stdout.write(self.style.SUCCESS(f'Linked Test {test1.gid} with Question {question.gid}'))
            

        try:
            userP = Users.objects.get(username='admin')

            professor = Professor.objects.create(
                department = 'Informatics',
                user = userP
            )

            test.professor = professor
            test.save()

            test1.professor = professor
            test1.save()

            userS = Users.objects.get(username='f3312305')
            student = Student.objects.create(
                reg_number = 'f3312305',
                year = 2023,
                user = userS
            )

            userNik = Users.objects.get(username='nikos')
            studentNik = Student.objects.create(
                reg_number = 'f3312301',
                year = 2023,
                user = userNik
            )
            
            classGr = ClassGroup.objects.create(
                class_name = '2023-2024 Full-Time Students'
            )

            classGr.professors.add(professor)
            classGr.students.add(student)
            classGr.students.add(studentNik)
            classGr.save()

            test.classGroup = classGr
            test.save()
            test1.classGroup = classGr
            test1.save()

            completedTest = CompletedTest.objects.create(
                score = 6.7,
                test = test,
                student = student
            )
            completedTestAnswer1 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 2 + 2?'),
                attribute = Attribute.objects.get(answer='2 + 2 = 4'),
                completedTest = completedTest
            )
            completedTestAnswer2 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 5 - 3?'),
                attribute = Attribute.objects.get(answer='5 - 3 = 2'),
                completedTest = completedTest
            )
            completedTestAnswer3 = CompletedTestAnswer.objects.create(
                is_correct = False,
                question = Question.objects.get(question='What is 3 * 3?'),
                attribute = Attribute.objects.get(answer='9 is a square number'),
                completedTest = completedTest
            )

            completedTestNik1 = CompletedTest.objects.create(
                score = 10.0,
                test = test,
                student = studentNik
            )
            completedTestAnswerNik1 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 2 + 2?'),
                attribute = Attribute.objects.get(answer='2 + 2 = 4'),
                completedTest = completedTestNik1
            )
            completedTestAnswerNik2 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 5 - 3?'),
                attribute = Attribute.objects.get(answer='5 - 3 = 2'),
                completedTest = completedTestNik1
            )
            completedTestAnswerNik3 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 3 * 3?'),
                attribute = Attribute.objects.get(answer='3 * 3 = 9'),
                completedTest = completedTestNik1
            )

            completedTest1 = CompletedTest.objects.create(
                score = 5.0,
                test = test1,
                student = student
            )
            completedTestAnswer11 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is the square root of 25?'),
                attribute = Attribute.objects.get(answer='5'),
                completedTest = completedTest1
            )
            completedTestAnswer12 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 25000 / 100?'),
                attribute = Attribute.objects.get(answer='250'),
                completedTest = completedTest1
            )
            completedTestAnswer13 = CompletedTestAnswer.objects.create(
                is_correct = False,
                question = Question.objects.get(question='What is 3! ?'),
                attribute = Attribute.objects.get(answer='3'),
                completedTest = completedTest1
            )
            completedTestAnswer14 = CompletedTestAnswer.objects.create(
                is_correct = False,
                question = Question.objects.get(question='How many sides are there in a square?'),
                attribute = Attribute.objects.get(answer='6 sides'),
                completedTest = completedTest1
            )

            completedTestNik2 = CompletedTest.objects.create(
                score = 7.5,
                test = test1,
                student = studentNik
            )
            completedTestAnswerNik21 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is the square root of 25?'),
                attribute = Attribute.objects.get(answer='5'),
                completedTest = completedTestNik2
            )
            completedTestAnswerNik22 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='What is 25000 / 100?'),
                attribute = Attribute.objects.get(answer='250'),
                completedTest = completedTestNik2
            )
            completedTestAnswerNik23 = CompletedTestAnswer.objects.create(
                is_correct = False,
                question = Question.objects.get(question='What is 3! ?'),
                attribute = Attribute.objects.get(answer='3'),
                completedTest = completedTestNik2
            )
            completedTestAnswerNik24 = CompletedTestAnswer.objects.create(
                is_correct = True,
                question = Question.objects.get(question='How many sides are there in a square?'),
                attribute = Attribute.objects.get(answer='4 sides'),
                completedTest = completedTestNik2
            )

            self.stdout.write(self.style.SUCCESS('Professor added successfully.'))
        except Users.DoesNotExist:
            print("User not found")

        self.stdout.write(self.style.SUCCESS('Data population complete'))
