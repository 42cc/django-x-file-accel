# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccelRedirect'
        db.create_table('xfar_accelredirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('prefix', self.gf('django.db.models.fields.CharField')(default='media', unique=True, max_length=64)),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('internal_path', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('serve_document_root', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
            ('filename_solver', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('x_file_accel_redirects', ['AccelRedirect'])


    def backwards(self, orm):
        # Deleting model 'AccelRedirect'
        db.delete_table('xfar_accelredirect')


    models = {
        'x_file_accel_redirects.accelredirect': {
            'Meta': {'object_name': 'AccelRedirect', 'db_table': "'xfar_accelredirect'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'filename_solver': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_path': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "'media'", 'unique': 'True', 'max_length': '64'}),
            'serve_document_root': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['x_file_accel_redirects']