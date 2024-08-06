import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Question, Attribute

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Create a test of type "math"
        test = Test.objects.create(
            gid=uuid.uuid4(),
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
                ]
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
                ]
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
                ]
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
                self.stdout.write(self.style.SUCCESS(f'Linked Question {question.gid} with Attribute {attribute.gid}'))

            # Associate the test with questions
            test.questions.add(question)
            self.stdout.write(self.style.SUCCESS(f'Linked Test {test.gid} with Question {question.gid}'))

        self.stdout.write(self.style.SUCCESS('Data population complete'))
