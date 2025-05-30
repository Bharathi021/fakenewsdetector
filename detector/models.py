from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class NewsArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_fake = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Article by {self.user.username}"