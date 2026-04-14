from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .matcher import get_best_match


def chatbot_page(request):
    """Redirect to homepage — chatbot is now a modal overlay in base.html."""
    return redirect('/?chatbot=open')


@require_POST
def chatbot_reply(request):
    message = request.POST.get("msg", "").strip()
    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    answer = get_best_match(message)
    return HttpResponse(answer)
