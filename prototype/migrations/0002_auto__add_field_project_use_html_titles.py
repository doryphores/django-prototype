# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.use_html_titles'
        db.add_column('prototype_project', 'use_html_titles', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project.use_html_titles'
        db.delete_column('prototype_project', 'use_html_titles')


    models = {
        'prototype.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'assets_root': ('django.db.models.fields.CharField', [], {'default': "'assets'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project_root': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'templates_root': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '255', 'blank': 'True'}),
            'use_html_titles': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['prototype']
