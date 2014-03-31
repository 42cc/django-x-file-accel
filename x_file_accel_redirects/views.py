# Create your views here.
from django.views.static import serve
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from x_file_accel_redirects.models import AccelRedirect
from x_file_accel_redirects.conf import settings


def accel_view(request, prefix, filepath=''):
    try:
        redirect_config = AccelRedirect.objects.get(prefix=prefix)
    except AccelRedirect.DoesNotExist:
        return HttpResponseNotFound()

    redirect_config.process(filepath)

    if redirect_config.login_required and not request.user.is_authenticated():
        return HttpResponseForbidden()

    if settings.X_FILE_ACCEL:
        response = HttpResponse()
        if redirect_config.disposition_header:
            response['Content-Disposition'] = redirect_config.disposition_header
        response['X-Accel-Redirect'] = redirect_config.accel_path
    else:
        response = serve(
            request,
            filepath,
            redirect_config.serve_document_root,
            show_indexes=False
        )

    return response
