from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()



class Message(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="author_messages")
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author.username
    
    @classmethod
    def last_10_message(cls):
        query = cls.objects.order_by('-timestamp').all()[:10]
        return query
