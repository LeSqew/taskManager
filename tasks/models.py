from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Status(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class File(models.Model):
	file = models.FileField(upload_to='task_files/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='files')

	def __str__(self):
		return self.file.name

class Task(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)  # Связь с пользователями
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	deadline = models.DateTimeField()
	status = models.ForeignKey(Status, on_delete=models.CASCADE)
	priority = models.IntegerField()
	difficulty = models.IntegerField()
	removed = models.BooleanField(default=False)
	
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


