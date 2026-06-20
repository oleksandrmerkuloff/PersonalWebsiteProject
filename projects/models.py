import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        PLANNING = "P", _("Planning")
        INPROGRESS = "I", _("In progress")
        DONE = "D", _("Done")
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    desctiption = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=ProjectStatus, default=ProjectStatus.PLANNING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
