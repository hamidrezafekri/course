from django.db import models
from django.core.exceptions import ValidationError
from socialmedia.common.models import BaseModel
from socialmedia.users.models import BaseUser
class Post(BaseModel):
    slug = models.SlugField(
        primary_key=True ,
        max_length=100
    )
    title = models.CharField(
        max_length=100  ,
        unique=True
    )
    content = models.CharField(
        max_length = 1000,
    )
    author = models.ForeignKey(
        BaseUser,
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
        return self.slug


class Subcription(models.Model):
    subscriber = models.ForeignKey(BaseUser , on_delete=models.CASCADE , related_name='sub')
    target = models.ForeignKey(BaseUser , on_delete=models.CASCADE , related_name='targets')

    class Meta:
        unique_together = ('subscriber' , 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": {"subscriber can't be equal to target"}})

    def __str__(self):
        return f"{self.subscriber.email} ,{self.target.email}"



