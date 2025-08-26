from django.shortcuts import render, get_object_or_404
from .models import Creation

def listCreations(request):
    kind = request.GET.get("kind")  # ?kind=blog/app/art/workshop
    qs = Creation.objects.filter(isPublished=True)
    if kind in {"blog", "app", "art", "workshop"}:
        qs = qs.filter(kind=kind)
    return render(request, "creations/list.html", {"items": qs, "activeKind": kind})

def creationDetail(request, slug):
    item = get_object_or_404(Creation, slug=slug, isPublished=True)
    prevItem, nextItem = item.getPrevNext()
    return render(
        request,
        "creations/detail.html",
        {"item": item, "prevItem": prevItem, "nextItem": nextItem},
    )
