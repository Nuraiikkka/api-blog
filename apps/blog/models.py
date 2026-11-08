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
    """
    Post category.
    """

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        """
        Return the name.
        """
        return self.name


class Tag(Model):
    """
    Post tag.
    """

    NAME_MAX_LEN = 50

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True)

    def __str__(self) -> str:
        """
        Return the name.
        """
        return self.name


class Post(Model):
    """
    Blog post.
    """

    TITLE_MAX_LEN = 200
    STATUS_MAX_LEN = 50

    class Status(TextChoices):
        """
        Post statuses.
        """

        DRAFT = "draft"
        PUBLISHED = "published"

    author = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    title = CharField(max_length=TITLE_MAX_LEN)
    slug = SlugField(unique=True)
    body = TextField()
    category = ForeignKey(
        to=Category,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    tags = ManyToManyField(to=Tag, blank=True)
    status = CharField(max_length=STATUS_MAX_LEN, choices=Status.choices)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Return the title.
        """
        return self.title


class Comment(Model):
    """
    Comment on a post.
    """

    post = ForeignKey(to=Post, on_delete=CASCADE)
    author = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    body = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Return the start of the comment text.
        """
        return self.body[:50]