from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Creation(models.Model):
    KIND_CHOICES = [
        ("blog", "Blog"),
        ("app", "App"),
        ("art", "Art"),
        ("workshop", "Workshop"),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="blog")
    summary = models.TextField(blank=True)
    bodyMarkdown = models.TextField(blank=True)  # simple for now; render later
    coverUrl = models.URLField(blank=True)       # switch to ImageField later if you want
    publishedAt = models.DateTimeField(auto_now_add=True)
    isPublished = models.BooleanField(default=True)

    # room to grow without migrations
    metaJson = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-publishedAt"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:180]
        super().save(*args, **kwargs)

    def getAbsoluteUrl(self):
        return reverse("creationDetail", kwargs={"slug": self.slug})

    def getPrevNext(self):
        prevItem = Creation.objects.filter(
            isPublished=True, publishedAt__lt=self.publishedAt
        ).order_by("-publishedAt").first()
        nextItem = Creation.objects.filter(
            isPublished=True, publishedAt__gt=self.publishedAt
        ).order_by("publishedAt").first()
        return prevItem, nextItem
