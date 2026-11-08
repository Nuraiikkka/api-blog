from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import action, display

from apps.blog.models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Category admin.
    """

    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """
    Tag admin.
    """

    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Comment admin.
    """

    list_display = ("short_body", "post", "author", "created_at")
    list_filter = [("created_at", RangeDateTimeFilter)]
    list_filter_submit = True
    search_fields = ("body", "author__email", "post__title")
    list_select_related = ("post", "author")
    autocomplete_fields = ("post", "author")

    @display(description="Comment")
    def short_body(self, obj: Comment) -> str:
        """
        Show the first 50 characters of the comment.
        """
        return obj.body[:50]


class CommentInline(TabularInline):
    """
    Comments shown inside the post page.
    """

    model = Comment
    extra = 0
    tab = True
    per_page = 10
    autocomplete_fields = ("author",)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    """
    Post admin.
    """

    list_display = (
        "title",
        "author",
        "category",
        "status_label",
        "tags_list",
        "created_at",
    )
    list_filter = ["status", "category", ("created_at", RangeDateTimeFilter)]
    list_filter_submit = True
    search_fields = ("title", "body", "author__email")
    list_select_related = ("author", "category")
    autocomplete_fields = ("author", "category", "tags")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]
    actions = ["make_published", "make_draft"]
    warn_unsaved_form = True

    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "status")}),
        ("Content", {"fields": ("body",), "classes": ["tab"]}),
        ("Relations", {"fields": ("category", "tags"), "classes": ["tab"]}),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Load tags with one extra query instead of one per post.
        """
        return super().get_queryset(request).prefetch_related("tags")

    @display(
        description="Status",
        label={
            Post.Status.DRAFT: "warning",
            Post.Status.PUBLISHED: "success",
        },
    )
    def status_label(self, obj: Post) -> str:
        """
        Show the status as a colored badge.
        """
        return obj.status

    @display(description="Tags")
    def tags_list(self, obj: Post) -> str:
        """
        Show tag names separated by commas.
        """
        return ", ".join(tag.name for tag in obj.tags.all())

    @action(description="Publish selected posts")
    def make_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Set status Published for selected posts.
        """
        count = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f"{count} posts published.")

    @action(description="Move selected posts to draft")
    def make_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Set status Draft for selected posts.
        """
        count = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f"{count} posts moved to draft.")
