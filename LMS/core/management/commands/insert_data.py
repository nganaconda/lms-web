import uuid
from django.core.management.base import BaseCommand
from core.models import Professor, Student, ClassGroup
from datetime import datetime

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        students = Student.objects.all().order_by('reg_number')
        professors = Professor.objects.all()

        classg = ClassGroup.objects.create(
            class_name = 'ClassGroup 1 - 2024'
        )

        member_no = 0
        for student in students:
            if student.year != 2023:
                if 0 <= member_no <= 4:
                    if member_no == 0:
                        for professor in professors:
                            if professor.professorID != 'p3150021':
                                classg.professors.add(professor)
                        classg.save()

                    classg.students.add(student)
                    classg.save()
                
                if 5 <= member_no <= 9:
                    if member_no == 5:
                        classg = ClassGroup.objects.create(
                            class_name = 'ClassGroup 2 - 2024'
                        )

                        for professor in professors:
                            if professor.professorID != 'p3150021':
                                classg.professors.add(professor)
                        classg.save()

                    classg.students.add(student)
                    classg.save()

                if 10 <= member_no <= 14:
                    if member_no == 10:
                        classg = ClassGroup.objects.create(
                            class_name = 'ClassGroup 3 - 2024'
                        )

                        for professor in professors:
                            if professor.professorID != 'p3150021':
                                classg.professors.add(professor)
                        classg.save()

                    classg.students.add(student)
                    classg.save()

                if 15 <= member_no <= 19:
                    if member_no == 15:
                        classg = ClassGroup.objects.create(
                            class_name = 'ClassGroup 4 - 2024'
                        )

                        for professor in professors:
                            if professor.professorID != 'p3150021':
                                classg.professors.add(professor)
                        classg.save()

                    classg.students.add(student)
                    classg.save()
                
                member_no += 1

