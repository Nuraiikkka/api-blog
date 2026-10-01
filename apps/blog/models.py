from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    SlugField,
    ForeignKey,
    TextField,
    ManyToManyField,
    TextChoices,
    DateTimeField,
    CASCADE, 
    SET_NULL,
)

class Category(Model):

    NAME_MAX_LEN = 100

    name = CharField(
        max_length = NAME_MAX_LEN,
        unique = True
    )
    slug = SlugField(
        unique = True
    )

class Tag(Model):
    NAME_MAX_LEN = 50

    name = CharField(
        max_length = NAME_MAX_LEN,
        unique = True
    )
    slug = SlugField(
        unique = True
    )

class Post(Model):

    TITLE_MAX_LEN = 200
    STATUS_MAX_LEN = 50

    class Status(TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    author = ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = CASCADE
    )
    title = CharField(
        max_length = TITLE_MAX_LEN
    )
    slug = SlugField(
        unique = True
    )
    body = TextField()
    category = ForeignKey(
        to = Category,
        on_delete = SET_NULL,
        null = True
    )
    tags = ManyToManyField(
        to = Tag, 
        blank = True
    )
    status = CharField(
        max_length = STATUS_MAX_LEN,
        choices = Status.choices
    )
    created_at = DateTimeField(
        auto_now_add = True
    )
    updated_at = DateTimeField(
        auto_now = True
    )

class Comment(Model):
    post = ForeignKey(
        to = Post,
        on_delete = CASCADE
    )
    author = ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = CASCADE
    )
    body = TextField()
    created_at = DateTimeField(
        auto_now_add = True
    )

