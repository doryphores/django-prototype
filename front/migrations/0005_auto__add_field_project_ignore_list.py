# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.ignore_list'
        db.add_column('front_project', 'ignore_list', self.gf('django.db.models.fields.CharField')(default='images/content', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project.ignore_list'
        db.delete_column('front_project', 'ignore_list')


    models = {
        'front.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'assets_root': ('django.db.models.fields.CharField', [], {'default': "'assets'", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_list': ('django.db.models.fields.CharField', [], {'default': "'images/content'", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project_root': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'templates_root': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['front']
