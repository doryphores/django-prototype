# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Project.assets_root'
        db.delete_column('prototype_project', 'assets_root')

        # Adding field 'Project.static_root'
        db.add_column('prototype_project', 'static_root', self.gf('django.db.models.fields.CharField')(default='static', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Project.assets_root'
        db.add_column('prototype_project', 'assets_root', self.gf('django.db.models.fields.CharField')(default='assets', max_length=255, blank=True), keep_default=False)

        # Deleting field 'Project.static_root'
        db.delete_column('prototype_project', 'static_root')


    models = {
        'prototype.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'data_root': ('django.db.models.fields.CharField', [], {'default': "'data'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'static_root': ('django.db.models.fields.CharField', [], {'default': "'static'", 'max_length': '255', 'blank': 'True'}),
            'use_html_titles': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['prototype']
