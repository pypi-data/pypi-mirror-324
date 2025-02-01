from django.db import models

class HoneypotAdminLog(models.Model):
    ip = models.GenericIPAddressField()
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} - {self.username} - {self.timestamp}"


class XSSPayload(models.Model):
    ip = models.GenericIPAddressField()
    payload = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} - {self.payload} - {self.timestamp}"
