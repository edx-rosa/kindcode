from django.shortcuts import render
from creations.models import Creation

def homePage(request):
    activeKind = request.GET.get("kind")
    items = Creation.objects.filter(isPublished=True)
    if activeKind in {"blog", "app", "art", "workshop"}:
        items = items.filter(kind=activeKind)
    ctx = {
        "activeKind": activeKind,
        "items": items,  # you can slice later e.g. [:24]
    }
    return render(request, "core/home.html", ctx)
