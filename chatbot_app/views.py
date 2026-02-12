from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .ai_service import ChatbotConfigError, get_qa_chain


def chatbot_page(request):
    """Redirect to homepage — chatbot is now a modal overlay in base.html."""
    return redirect('/?chatbot=open')


@require_POST
def chatbot_reply(request):
    message = request.POST.get("msg", "").strip()
    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    try:
        qa_chain = get_qa_chain()
    except ChatbotConfigError as exc:
        return HttpResponse(str(exc), status=500)

    result = qa_chain({"query": message})
    return HttpResponse(str(result.get("result", "")).strip())
