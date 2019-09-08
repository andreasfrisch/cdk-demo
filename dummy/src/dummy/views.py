import textwrap

from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render

from dummy.settings import ENVIRONMENT, VERSION, DEBUG, SECRET


class RootPageView(View):
    def dispatch(request, *args, **kwargs):
        response_text = textwrap.dedent('''\
            <html>
            <head>
                <title>Greetings to the world</title>
            </head>
            <body>
                <h1>Greetings to the world</h1>
                <h2>Version: %s</h2>
                <p>Environment: %s</p>
                <p>Debug: %s</p>
                <p>Secret: %s</p>
                <hr>
            </body>
            </html>
        ''' % (VERSION, ENVIRONMENT, DEBUG, SECRET))
        return HttpResponse(response_text)

def home(request):
    """
    Handle request for main page
    """
    template = "index.html"
    return render(request, template)
