from django.db import models


class StatusHistory(models.Model):
    " Stores time based status updates for each remote box in the project's config. "
    nickname = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    date_checked = models.DateTimeField(auto_now_add=True)
    box_status = models.BooleanField(default=False)
    processes_output = models.TextField(null=True, blank=True)
