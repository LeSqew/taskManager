from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Status(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class Task(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)  # Связь с пользователями
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	deadline = models.DateTimeField()
	status = models.ForeignKey(Status, on_delete=models.CASCADE)
	priority = models.IntegerField(
		validators=[
			MinValueValidator(1, message='Приоритет должен быть не менее 1'),
			MaxValueValidator(100, message='Приоритет должен быть не более 100')
		]
	)
	difficulty = models.IntegerField(
		validators=[
			MinValueValidator(1, message='Сложность должна быть не менее 1'),
			MaxValueValidator(100, message='Сложность должна быть не более 100')
		]
	)
	removed = models.BooleanField(default=False)
	sprint = models.ForeignKey('tables.Sprint', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
	
	def __str__(self):
		return self.title

	def soft_delete(self):
		"""Метод для мягкого удаления задачи"""
		self.removed = True
		self.save()

	@classmethod
	def get_active_tasks(cls):
		"""Получить все активные (неудаленные) задачи"""
		return cls.objects.filter(removed=False)


