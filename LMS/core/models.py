from django.db import models
import secrets
import hashlib
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class UserAccountManager(BaseUserManager):
    class Meta:
        db_table = 'Users'
    def create_user(self, email, username, first_name, last_name, password):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(email, username, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

class Users(AbstractBaseUser):
    class Meta:
        db_table = 'Users'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username= models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    last_login = ""
    is_superuser = True
    is_staff = True
    is_active = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name' , 'last_name']

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
            return self.is_admin

    objects = UserAccountManager()


class Professor(models.Model):
    class Meta:
        db_table = 'Professors'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professorID = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"Professor {self.first_name} {self.last_name} - Department: {self.department}"


class Student(models.Model):
    class Meta:
        db_table = 'Students'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reg_number = models.CharField(max_length=50)
    year = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student {self.first_name} {self.last_name} - Registration Number: {self.reg_number}, Year: {self.year}"


class ClassGroup(models.Model):
    class Meta:
        db_table = 'ClassGroups'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_name = models.CharField(max_length=100)
    professors = models.ManyToManyField('Professor', related_name='classGroups')
    students = models.ManyToManyField('Student')

    def __str__(self):
        return f"ClassPerformance {self.gid} - Class: {self.class_name}"
    

class Test(models.Model):
    class Meta:
        db_table = 'Tests'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_name = models.CharField(max_length=100)
    level = models.IntegerField()
    #age = models.IntegerField()
    type = models.CharField(max_length=100)
    questions_no = models.IntegerField()
    questions_dif = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField('Question', related_name='tests')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    classGroup = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"Test {self.gid} - Type: {self.type}, Level: {self.level}, Age: {self.age}"


class Attribute(models.Model):
    class Meta:
        db_table = 'Attributes'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return f"Attribute with id {self.gid} - Answer: {self.answer}"
      

class Question(models.Model):
    class Meta:
        db_table = 'Questions'

    SINGLE_CHOICE = 'Single Choice'
    MULTIPLE_CHOICE = 'Multiple Choice'
    TEXT = 'Text'
    FILL_IN_BLANKS = 'Fill in Blanks'
    
    ANSWER_TYPE_CHOICES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TEXT, 'Text'),
        (FILL_IN_BLANKS, 'Fill in Blanks'),
    ]
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    attributes = models.ManyToManyField('Attribute', related_name='questions')
    rightAnswer = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    answerType = models.CharField(
        max_length=20,
        choices=ANSWER_TYPE_CHOICES,
        default=SINGLE_CHOICE
    )

    def __str__(self):
        return f"Question with id {self.gid} - Question: {self.question}, Tpye: {self.type}, Difficulty: {self.difficulty}"
    
    def clean(self):
        if not (1 <= self.difficulty <= 4):
            raise ValidationError('Difficulty must be between 1 and 4.')
    

class CompletedTest(models.Model):
    class Meta:
        db_table = 'CompletedTests'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    completion_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    test = models.ForeignKey(Test, related_name='completed_tests', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='completed_tests', on_delete=models.CASCADE)

    def __str__(self):
        return f"CompletedTest {self.gid} - completion_date: {self.completion_date}, score: {self.score}, Student: {self.student.gid}"
    

class CompletedTestAnswer(models.Model):
    class Meta:
        db_table = 'CompletedTestAnswers'
    
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_correct = models.BooleanField(default=False)
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, related_name='completed_test_answers', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, related_name='completed_test_answers', on_delete=models.CASCADE)
    completedTest = models.ForeignKey(CompletedTest, related_name='completed_test_answers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"CompletedTestAnswer {self.gid} - is_correct: {self.is_correct}, completedTest: {self.completedTest.gid}, attribute: {self.attribute.gid}"


class TestQuestion(models.Model):
    class Meta:
        db_table = 'tests_questions'

    weight = models.FloatField()
    question = models.ForeignKey(Question, related_name='test_questions', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='test_questions', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"TestQuestion {self.gid} - weight: {self.weight}, question: {self.question.gid}, test: {self.test.gid}"
    

class Tag(models.Model):
    class Meta:
        db_table = 'tags'

    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Tag {self.gid} - tag_name: {self.tag_name}"
    

class TestTag(models.Model):
    class Meta:
        db_table = 'tests_tags'

    tag = models.ForeignKey(Tag, related_name='test_tags', on_delete=models.CASCADE, primary_key=True)
    test = models.ForeignKey(Test, related_name='test_tags', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"TestTag - tag: {self.tag.gid}, test: {self.test.gid}"
    