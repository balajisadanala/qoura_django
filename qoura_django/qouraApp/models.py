from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    description = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_questions', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_questions', blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Q{self.id}: {self.question[:50]}..."
    class Meta:
        ordering = ['-updated_at']

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_answers', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_answers', blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"A{self.id} to Q{self.question.id}"

    class Meta:
        ordering = ['-updated_at']