from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

