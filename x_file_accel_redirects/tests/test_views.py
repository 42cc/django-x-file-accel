# -*- coding: utf-8 -*-
import os

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase

from mock import patch

from x_file_accel_redirects.conf import settings


class TestRedirects(TestCase):

    @patch('django.views.static.serve', return_value=HttpResponse())
    def test_accel_redirects(self, serve_mock):
        from x_file_accel_redirects.models import AccelRedirect
        settings.X_FILE_ACCEL = True
        redirect = AccelRedirect(
            prefix='email_attaches',
            filename_solver=AccelRedirect.FILENAME_SOLVERS.remainder,
            internal_path='/protected/attaches/',
            login_required=False,
        )
        redirect.save()
        filepath = 'hello/world.txt'
        url = reverse(
            'accel_view',
            kwargs=dict(prefix=redirect.prefix, filepath=filepath)
        )
        response = self.client.get(url)

        file_name = filepath.split('/')[-1]
        disposition_header = 'attachment; filename={0}'.format(file_name)
        self.assertEqual(response.get('Content-Disposition', None), disposition_header)

        accel_path = os.path.join(redirect.internal_path, filepath)
        self.assertEqual(response.get('X-Accel-Redirect', None), accel_path)

        self.assertFalse(serve_mock.called)

        # testing serving when accel is disabled
        #settings.X_FILE_ACCEL = False
        #redirect.serve_document_root = '/home/deploy/kava/static/path/'
        #redirect.save()

        #response = self.client.get(url)
        #self.assertEqual(response.get('Content-Disposition', None), None)
        #self.assertEqual(response.get('X-Accel-Redirect', None), None)
        #self.assertTrue(serve_mock.called)

        # testing login_required
        redirect.login_required = True
        redirect.save()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
