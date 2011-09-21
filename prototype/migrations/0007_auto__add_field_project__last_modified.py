# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project._last_modified'
        db.add_column('prototype_project', '_last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 9, 21, 12, 5, 19, 985000), auto_now=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project._last_modified'
        db.delete_column('prototype_project', '_last_modified')


    models = {
        'prototype.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            '_last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 9, 21, 12, 5, 19, 985000)', 'auto_now': 'True', 'blank': 'True'}),
            'data_folder': ('django.db.models.fields.CharField', [], {'default': "'data'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'static_root': ('django.db.models.fields.CharField', [], {'default': "'static'", 'max_length': '255', 'blank': 'True'}),
            'use_html_titles': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['prototype']
