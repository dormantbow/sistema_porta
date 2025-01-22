from django.db import models

class Door(models.Model):
    door_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)  # True: Aberta, False: Fechada
    is_scheduled = models.BooleanField(default=False)

class AccessHistory(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=50)  # 'open', 'close', 'schedule'
    timestamp = models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
