from django.http import HttpResponseRedirect
from django.contrib.messages import info

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        url = request.path
        if request.user.is_anonymous and url != "/login/":
            info(request, "Please login to access this page.")
            return HttpResponseRedirect('/login')

        response = self.get_response(request)
        return response