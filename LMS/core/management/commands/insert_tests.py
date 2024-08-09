import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Question, Attribute, Users, Professor, Student, TestScore, ClassGroup

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
            questions_dif=4
        )
        self.stdout.write(self.style.SUCCESS(f'Created Test: {test.gid}'))

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

        try:
            userP = Users.objects.get(username='admin')

            professor = Professor.objects.create(
                department = 'Informatics',
                user = userP
            )

            test.professor = professor
            test.save()

            userS = Users.objects.get(username='f3312305')

            student = Student.objects.create(
                reg_number = 'f3312305',
                year = 2023,
                user = userS
            )
            
            classGr = ClassGroup.objects.create(
                class_name = '2023-2024 Full-Time Students',

            )
            classGr.professors.add(professor)
            classGr.students.add(student)
            classGr.save()

            test.classGroup = classGr
            test.save()

            testscore = TestScore.objects.create(
                result = 9.0,
                test = test,
                student = student
            )

            self.stdout.write(self.style.SUCCESS('Professor added successfully.'))
        except Users.DoesNotExist:
            print("User not found")

        self.stdout.write(self.style.SUCCESS('Data population complete'))
