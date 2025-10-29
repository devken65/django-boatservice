# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def categories_all(request):
    return Response(
        {
            "ok": True,
        }
    )
