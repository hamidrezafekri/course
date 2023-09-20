from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify

from socialmedia.blog.models import Subcription, Post
from socialmedia.users.models import BaseUser


def count_following(* , user: BaseUser) -> int:
    return Subcription.objects.filter(subscriber=user).count()


def count_posts(* , user:BaseUser) -> int:
    return Post.objects.filter(author = user).count()

def subscribe(* , user:BaseUser , email:str) -> QuerySet[Subcription]:
    target = BaseUser.objects.get(email = email)
    sub = Subcription(subscriber=user , target = target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*  , user:BaseUser , email: str) -> dict:
    target = BaseUser.objects.get(email = email)
    Subcription.objects.get(subscriber = user , target= target).delete()

@transaction.atomic

def create_post(* , user:BaseUser , title:str , content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author = user , title = title , content = content , slug = slugify(title)
    )
    return post