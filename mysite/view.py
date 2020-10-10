from django.shortcuts import redirect


def index(request):
    """
    Redirect to the index page.
    """
    return redirect("polls:index")
