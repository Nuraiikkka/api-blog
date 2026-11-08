from django.http import HttpRequest


def environment_callback(request: HttpRequest) -> list[str]:
    """
    Show the environment badge in the admin header.
    """

    return ["Development", "info"]
