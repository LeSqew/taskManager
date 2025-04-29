from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task

# Create your models here.
class ScrumTable(models.Model):
	isMainTable = models.BooleanField(default=False)
	name = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	deadline = models.DateTimeField()
	Tasks = models.ManyToManyField(Task, related_name='scrum_tables', blank=True)
	assigned_users = models.ManyToManyField(User, related_name='scrum_tables', blank=True)
	assigned_tables = models.ManyToManyField('self', related_name='assigned_tables', blank=True)
	class Meta:
		db_table = 'tasks_ScrumTable'