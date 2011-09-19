# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Rename 'data_root' field to 'data_folder'
        db.rename_column('prototype_project', 'data_root', 'data_folder')


    def backwards(self, orm):
        
        # Rename 'data_folder' field to 'data_root'
        db.rename_column('prototype_project', 'data_folder', 'data_root')


    models = {
        'prototype.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'data_folder': ('django.db.models.fields.CharField', [], {'default': "'data'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'static_root': ('django.db.models.fields.CharField', [], {'default': "'static'", 'max_length': '255', 'blank': 'True'}),
            'use_html_titles': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['prototype']
