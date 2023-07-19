from django.db import models


class Auth(models.Model):
    content = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)