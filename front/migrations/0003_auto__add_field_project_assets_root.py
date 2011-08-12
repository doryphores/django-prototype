# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.assets_root'
        db.add_column('front_project', 'assets_root', self.gf('django.db.models.fields.CharField')(default='assets', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project.assets_root'
        db.delete_column('front_project', 'assets_root')


    models = {
        'front.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'assets_root': ('django.db.models.fields.CharField', [], {'default': "'assets'", 'max_length': '255', 'blank': 'True'}),
            'css_ignore': ('django.db.models.fields.TextField', [], {'default': "'print.css'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project_root': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'templates_root': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['front']
