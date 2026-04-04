from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.deprecation import MiddlewareMixin

class AdminAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            user = request.user
            if not user.is_authenticated or not user.is_staff:
                return redirect('/')  # hoặc raise Http404() nếu muốn hiển thị 404
        return None
