from django.db import models


class Bots(models.Model):
    bot_id = models.CharField(max_length=10)
    command = models.CharField(max_length=20, blank=True)
    command_added = models.BooleanField(default=False)
    last_activity = models.TimeField(auto_now_add=True)
    screenshot = models.TextField()
    website = models.TextField()
    image = models.TextField()
    text = models.TextField()
    info = models.TextField()
