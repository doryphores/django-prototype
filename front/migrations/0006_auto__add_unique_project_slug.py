# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Project', fields ['slug']
        db.create_unique('front_project', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Project', fields ['slug']
        db.delete_unique('front_project', ['slug'])


    models = {
        'front.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'assets_root': ('django.db.models.fields.CharField', [], {'default': "'assets'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_list': ('django.db.models.fields.CharField', [], {'default': "'images/content'", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project_root': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'templates_root': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['front']
