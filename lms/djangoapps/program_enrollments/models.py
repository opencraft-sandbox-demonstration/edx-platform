# -*- coding: utf-8 -*-
"""
Django model specifications for the Program Enrollments API
"""
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class ProgramEnrollments(TimeStampedModel):  # pylint: disable=model-missing-unicode
    """
    This is a model for Program Enrollments from the registrar service

    .. pii:
    """
    STATUSES = (
        ('enrolled', _(u'enrolled')),
        ('pending', _(u'pending')),
        ('suspended', _(u'suspended')),
        ('withdrawn', _(u'withdrawn')),
    )

    class Meta(object):
        app_label = "program_enrollments"

    user = models.ForeignKey(
        User,
        null=True,
        blank=True
    )
    email = models.EmailField()
    external_user_key = models.CharField(
        db_index=True,
        max_length=255,
        null=True
    )
    program_uuid = models.UUIDField(db_index=True, null=False)
    curriculum_uuid = models.UUIDField(db_index=True, null=False)
    status = models.CharField(max_length=9, choices=STATUSES)
    historical_records = HistoricalRecords()

    @classmethod
    def retire_user(cls, user_id):
        """
        With the parameter user_id, blank out the external_user_key
        This is to fulfill our GDPR obligations

        Return True if there is data to be blanked
        Return False if there is no matching data
        """
        enrollments = cls.objects.filter(user=user_id)
        if not enrollments:
            return False

        enrollments.update(external_user_key=None, email=None)
        return True
