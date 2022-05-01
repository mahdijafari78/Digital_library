from django.http import Http404
from django.shortcuts import redirect


class LoginSubMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        print(user.is_authenticated)
        if user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')
