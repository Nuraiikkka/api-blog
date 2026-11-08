from typing import Any

from django.db.models import Count, Q
from django.http import HttpRequest

from apps.blog.models import Comment, Post

LATEST_POSTS_COUNT = 5


def environment_callback(request: HttpRequest) -> list[str]:
    """
    Show the environment badge in the admin header.
    """
    return ["Development", "info"]


def dashboard_callback(request: HttpRequest, context: dict[str, Any]) -> dict[str, Any]:
    """
    Add statistics and latest posts to the admin dashboard.
    """
    stats = Post.objects.aggregate(
        total=Count("id"),
        published=Count("id", filter=Q(status=Post.Status.PUBLISHED)),
        draft=Count("id", filter=Q(status=Post.Status.DRAFT)),
    )
    latest_posts = Post.objects.select_related("author").order_by("-created_at")[
        :LATEST_POSTS_COUNT
    ]

    context["kpi"] = [
        {"title": "Posts", "value": stats["total"]},
        {"title": "Published", "value": stats["published"]},
        {"title": "Drafts", "value": stats["draft"]},
        {"title": "Comments", "value": Comment.objects.count()},
    ]
    context["table"] = {
        "headers": ["Title", "Author", "Status", "Created"],
        "rows": [
            [
                post.title,
                post.author.email,
                post.status,
                post.created_at.strftime("%Y-%m-%d"),
            ]
            for post in latest_posts
        ],
    }
    return context
