import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Tag, TestTag, Question, Attribute, Users, Professor, Student, CompletedTest, CompletedTestAnswer, ClassGroup
from datetime import datetime

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        try:
            tags = Tag.objects.filter()
            tests = Test.objects.filter()

            for test in tests:
                tag = tags.get(tag_name='Semester Exams')
                testtag = TestTag.objects.create(tag=tag, test=test)
                
                if '2024' in test.test_name:
                     tag = tags.get(tag_name='2024')
                     testtag = TestTag.objects.create(tag=tag, test=test)
                     
                     if 'Jun' in test.test_name:
                        tag = tags.get(tag_name='June')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Mid-Year Exams')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                     elif 'Sep' in test.test_name:
                        tag = tags.get(tag_name='September')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Fall Exams')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='End-Term Exams')
                        testtag = TestTag.objects.create(tag=tag, test=test)
                
                elif '2025' in test.test_name:
                    tag = tags.get(tag_name='2025')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='January')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='New Year Exams')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Winter Exams')
                    testtag = TestTag.objects.create(tag=tag, test=test)
                
                if test.type == 'Computer Science':
                    tag = tags.get(tag_name='Computer Science')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='CS')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                elif test.type == 'Cybersecurity':
                    tag = tags.get(tag_name='Cybersecurity')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Cybersecurity Basics')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='InfoSec')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                elif test.type == 'Math':
                    tag = tags.get(tag_name='Math')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Mathematics')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Math Practice')
                    testtag = TestTag.objects.create(tag=tag, test=test)
                
                elif test.type == 'Medical Basic':
                    tag = tags.get(tag_name='Medical Science')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Medical')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    tag = tags.get(tag_name='Basic')
                    testtag = TestTag.objects.create(tag=tag, test=test)

                    if 'Anatomy' in test.test_name:
                        tag = tags.get(tag_name='Anatomy')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Human Body')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Intro to Anatomy')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                    elif 'Physiology' in test.test_name:
                        tag = tags.get(tag_name='Physiology')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Body Functions')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Intro to Physiology')
                        testtag = TestTag.objects.create(tag=tag, test=test) 

                    elif 'Pathology' in test.test_name:
                        tag = tags.get(tag_name='Pathology')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Diagnostics')
                        testtag = TestTag.objects.create(tag=tag, test=test)

                        tag = tags.get(tag_name='Pathology Study')
                        testtag = TestTag.objects.create(tag=tag, test=test)

        except Tag.DoesNotExist:
            print("User not found")

        self.stdout.write(self.style.SUCCESS('Data population complete'))
