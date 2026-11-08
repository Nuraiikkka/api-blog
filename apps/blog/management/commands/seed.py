import random
import time
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from django.utils.text import slugify
from faker import Faker

from apps.blog.models import Category, Comment, Post, Tag

User = get_user_model()


class Command(BaseCommand):
    """
    Fill the database with fake data.
    """

    DEFAULT_USERS = 20
    DEFAULT_POSTS = 100
    DEFAULT_COMMENTS = 500

    SEED_PASSWORD = "seed12345"
    EMAIL_DOMAIN = "example.com"

    INACTIVE_PERCENT = 20
    STAFF_PERCENT = 10
    PUBLISHED_PERCENT = 70
    NO_CATEGORY_PERCENT = 10

    TITLE_WORDS = 6
    BODY_PARAGRAPHS = 4
    SLUG_BASE_LEN = 40
    MAX_TAGS_PER_POST = 5

    MIN_COMMENT_SENTENCES = 1
    MAX_COMMENT_SENTENCES = 3

    CATEGORY_NAMES = (
        "Python",
        "Django",
        "DevOps",
        "Databases",
        "Frontend",
        "Testing",
        "Security",
        "Career",
    )
    TAG_NAMES = (
        "api",
        "orm",
        "docker",
        "git",
        "linux",
        "sql",
        "postgres",
        "rest",
        "jwt",
        "celery",
        "redis",
        "nginx",
        "pytest",
        "ruff",
        "async",
        "caching",
        "deployment",
        "tips",
        "tutorial",
        "beginners",
    )

    help = "Fill the database with fake data."

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command line arguments.
        """
        parser.add_argument(
            "--users",
            type=int,
            default=self.DEFAULT_USERS,
            help="Number of users to create",
        )
        parser.add_argument(
            "--posts",
            type=int,
            default=self.DEFAULT_POSTS,
            help="Number of posts to create",
        )
        parser.add_argument(
            "--comments",
            type=int,
            default=self.DEFAULT_COMMENTS,
            help="Number of comments to create",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing data before seeding",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Run the command.
        """
        users_count = options["users"]
        posts_count = options["posts"]
        comments_count = options["comments"]
        clear = options["clear"]

        if users_count < 0 or posts_count < 0 or comments_count < 0:
            raise CommandError("Numbers must not be negative.")

        start = time.perf_counter()

        if clear:
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("Old data deleted.")

        fake = Faker()
        password = make_password(self.SEED_PASSWORD)
        used_emails = set(User.objects.values_list("email", flat=True))

        users = []
        for _ in range(users_count):
            first_name = fake.first_name()
            last_name = fake.last_name()

            base = f"{first_name}.{last_name}".lower()
            email = f"{base}@{self.EMAIL_DOMAIN}"
            number = 1
            while email in used_emails:
                number += 1
                email = f"{base}{number}@{self.EMAIL_DOMAIN}"
            used_emails.add(email)

            is_active = random.randint(1, 100) > self.INACTIVE_PERCENT
            is_staff = random.randint(1, 100) <= self.STAFF_PERCENT

            users.append(
                User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_active=is_active,
                    is_staff=is_staff,
                )
            )
        User.objects.bulk_create(users)
        self.stdout.write(f"Users: {len(users)} created")

        used_slugs = set(Category.objects.values_list("slug", flat=True))
        categories = []
        for name in self.CATEGORY_NAMES:
            slug = slugify(name)
            if slug not in used_slugs:
                categories.append(
                    Category(
                        name=name,
                        slug=slug,
                    )
                )
        Category.objects.bulk_create(categories)
        self.stdout.write(f"Categories: {len(categories)} created")

        used_slugs = set(Tag.objects.values_list("slug", flat=True))
        tags = []
        for name in self.TAG_NAMES:
            slug = slugify(name)
            if slug not in used_slugs:
                tags.append(
                    Tag(
                        name=name,
                        slug=slug,
                    )
                )
        Tag.objects.bulk_create(tags)
        self.stdout.write(f"Tags: {len(tags)} created")

        need_users = posts_count > 0 or comments_count > 0
        if need_users and not User.objects.exists():
            raise CommandError("There are no users. Use --users first.")

        author_ids = list(User.objects.values_list("id", flat=True))
        all_categories = list(Category.objects.all())
        all_tags = list(Tag.objects.all())
        used_slugs = set(Post.objects.values_list("slug", flat=True))

        posts = []
        for _ in range(posts_count):
            title = fake.sentence(nb_words=self.TITLE_WORDS).rstrip(".")
            body = "\n\n".join(fake.paragraphs(nb=self.BODY_PARAGRAPHS))

            base_slug = slugify(title)[: self.SLUG_BASE_LEN]
            slug = base_slug
            number = 1
            while slug in used_slugs:
                number += 1
                slug = f"{base_slug}-{number}"
            used_slugs.add(slug)

            if random.randint(1, 100) <= self.PUBLISHED_PERCENT:
                status = Post.Status.PUBLISHED
            else:
                status = Post.Status.DRAFT

            if random.randint(1, 100) <= self.NO_CATEGORY_PERCENT:
                category = None
            else:
                category = random.choice(all_categories)

            posts.append(
                Post(
                    author_id=random.choice(author_ids),
                    title=title,
                    slug=slug,
                    body=body,
                    category=category,
                    status=status,
                )
            )
        Post.objects.bulk_create(posts)

        for post in posts:
            tags_number = random.randint(0, self.MAX_TAGS_PER_POST)
            post.tags.set(random.sample(all_tags, tags_number))
        self.stdout.write(f"Posts: {len(posts)} created")

        has_published = Post.objects.filter(status=Post.Status.PUBLISHED).exists()
        if comments_count > 0 and not has_published:
            raise CommandError("There are no published posts.")

        published_ids = list(
            Post.objects.filter(status=Post.Status.PUBLISHED).values_list(
                "id", flat=True
            )
        )

        comments = []
        for _ in range(comments_count):
            sentences_number = random.randint(
                self.MIN_COMMENT_SENTENCES, self.MAX_COMMENT_SENTENCES
            )
            comments.append(
                Comment(
                    post_id=random.choice(published_ids),
                    author_id=random.choice(author_ids),
                    body=" ".join(fake.sentences(nb=sentences_number)),
                )
            )
        Comment.objects.bulk_create(comments)
        self.stdout.write(f"Comments: {len(comments)} created")

        seconds = time.perf_counter() - start
        self.stdout.write(self.style.SUCCESS(f"Done in {seconds:.2f} seconds"))