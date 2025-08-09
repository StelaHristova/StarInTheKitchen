from django.shortcuts import render


def permission_denied_view(request, exception):
    return render(request, '403.html', {'reason': str(exception)}, status=403)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)