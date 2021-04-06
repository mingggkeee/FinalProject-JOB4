# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bookmark(models.Model):
    id = models.OneToOneField('User', models.DO_NOTHING, db_column='id', primary_key=True)
    letter = models.ForeignKey('Letter', models.DO_NOTHING)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'BOOKMARK'
        unique_together = (('id', 'letter'),)


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'COMPANIES'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    industry = models.ForeignKey('Industry', models.DO_NOTHING)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'COMPANY'


class Industry(models.Model):
    industry_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'INDUSTRY'


class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    id = models.ForeignKey('User', models.DO_NOTHING, db_column='id')
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'INTEREST'


class Letter(models.Model):
    letter_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=10000, blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    task = models.ForeignKey('Task', models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'LETTER'


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'QUESTION'


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'TASK'


# ========== custom admin page ==========
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    class Meta:
        app_label = 'myaccount'

    def create_user(self, id, password=None):
        if not id:
            raise ValueError('Users must have an email address')

        user = self.model(
            id=id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None):
        user = self.create_user(
            id,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)
    birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)

    username = models.CharField(
        max_length=20,
        null=True,
        default='annonymous'
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

    objects = MyUserManager()

    USERNAME_FIELD = 'id'

    class Meta:
        managed = False
        app_label = 'myaccount'
        db_table = 'USER'

    def __str__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# ========== custom admin page ==========
