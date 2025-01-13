import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Tag, TestTag, Question, Attribute, Users, Professor, Student, CompletedTest, CompletedTestAnswer, ClassGroup
from datetime import datetime

import uuid
from django.core.management.base import BaseCommand
from core.models import Test, Tag, TestTag

class Command(BaseCommand):
    help = 'Updates test tags for specific tests'

    def handle(self, *args, **kwargs):
        try:
            tags = Tag.objects.all()
            test_mapping = {
                "2024 Sep Exams Math": ["2024", "September", "Exams", "Math", "Mathematics", "End-Term Exams", "Fall Exams"],
                "2024 June Exams Math": ["2024", "June", "Exams", "Math", "Mathematics", "Mid-Year Exams"],
                "2024 Sep Exams Cybersecurity": ["2024", "September", "Exams", "Cybersecurity", "Cybersecurity Basics", "InfoSec", "End-Term Exams", "Fall Exams"],
                "2024 Sep Exams Computer Science": ["2024", "September", "Exams", "Computer Science", "CS", "End-Term Exams", "Fall Exams"],
                "2025 Jan Exams Computer Science": ["2025", "January", "Exams", "Computer Science", "CS", "New Year Exams", "Winter Exams"],
                "Anatomy Basics": ["Anatomy", "Basics", "Medical Science", "Human Body", "Intro to Anatomy", "Body Systems"],
                "2024 Jun Exams Computer Science": ["2024", "June", "Exams", "Computer Science", "CS", "Mid-Year Exams"],
                "Advanced Pathology Concepts": ["Pathology", "Advanced", "Concepts", "Medical Science", "Diagnostics", "Pathology Study", "Clinical Pathology"],
                "2025 Jan Exams Biology": ["2025", "January", "Exams", "Biology", "Bio Exams", "New Year Exams", "Winter Exams", "Biology Concepts"],
                "Physiology Fundamentals": ["Physiology", "Fundamentals", "Human Body", "Body Functions", "Intro to Physiology", "Biological Processes"],
                "2024 Jun Exams Cybersecurity": ["2024", "June", "Exams", "Cybersecurity", "Cybersecurity Basics", "InfoSec", "Mid-Year Exams"],
                "2025 Jan Exams Cybersecurity": ["2025", "January", "Exams", "Cybersecurity", "Cybersecurity Basics", "InfoSec", "New Year Exams", "Winter Exams"],
            }

            for test_name, tag_names in test_mapping.items():
                try:
                    test = Test.objects.get(test_name=test_name)
                    for tag_name in tag_names:
                        tag = tags.get(tag_name=tag_name)
                        TestTag.objects.get_or_create(tag=tag, test=test)
                except Test.DoesNotExist:
                    print(f"Test '{test_name}' not found.")
                except Tag.DoesNotExist:
                    print(f"One or more tags for '{test_name}' not found.")

            self.stdout.write(self.style.SUCCESS('Test tags updated successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
