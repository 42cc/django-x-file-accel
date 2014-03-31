# -*- coding: utf-8 -*-
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from x_file_accel_redirects.conf import settings


class AccelRedirect(models.Model):

    FILENAME_SOLVERS = Choices(
        (1, 'remainder', _(u'Everything after last "/" is is threated as filename')),
        (2, 'none', _(u'Do not try processing filenames (e.g. for service)')),
    )

    description = models.CharField(
        max_length=64,
    )
    prefix = models.CharField(
        _(u"URL prefix"),
        help_text=_(u'URL prefix for accel_view that will be handled with this config'),
        default='media',
        max_length=64,
        unique=True,
    )
    login_required = models.BooleanField(
        _(u"Login required"),
        help_text=_(u"Protect files with authentication"),
        default=True,
    )
    internal_path = models.CharField(
        _(u"Internal path"),
        help_text=_(
            u"Path that is served by nginx as internal to use in X-Accel-Redirect "
            u"header. Actual Accell will be "
            u"'{internal_path}/{path_in_url_after_prefix}'"
        ),
        max_length=64,
    )
    serve_document_root = models.CharField(
        _(u"Document root"),
        help_text=_(u"Path with actual files to serve manualy when settings.X_FILE_ACCEL is False"),
        default='',
        blank=True,
        max_length=64,
    )
    filename_solver = models.PositiveSmallIntegerField(
        choices=FILENAME_SOLVERS,
        default=FILENAME_SOLVERS.remainder,
    )

    class Meta:
        verbose_name = _(u'Accel-Redirect config')
        verbose_name_plural = _(u'Accel-Redirect configs')
        db_table = 'xfar_accelredirect'

    def __unicode__(self):
        return self.description

    def clean(self):
        if settings.X_FILE_ACCEL and not self.serve_document_root:
            raise ValidationError(_(u'X_FILE_ACCEL is disabled! Please set serve_document_root field.'))
        if self.prefix.find('/') >= 0:
            raise ValidationError(u"prefix should not contain slashes")

    def get_filename(self, filepath):
        if self.filename_solver == self.FILENAME_SOLVERS.remainder:
            return filepath.split('/')[-1]
        elif self.filename_solver == self.FILENAME_SOLVERS.none:
            return None
        else:
            raise ValueError(
                u'Something wrong with filename_solver value! processing of '
                u'filename_solver "%s" is not implemented' % self.filename_solver
            )

    def process(self, filepath):
        self.filepath = filepath
        self.disposition_header = "attachment; filename={0}".format(self.get_filename(filepath))
        self.accel_path = os.path.join(self.internal_path, filepath)
