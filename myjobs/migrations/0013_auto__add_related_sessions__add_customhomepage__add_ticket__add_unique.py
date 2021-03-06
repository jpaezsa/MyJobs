# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Related_Sessions'
        db.create_table(u'myjobs_related_sessions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
        ))
        db.send_create_signal(u'myjobs', ['Related_Sessions'])

        # Adding M2M table for field mj_session on 'Related_Sessions'
        db.create_table(u'myjobs_related_sessions_mj_session', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('related_sessions', models.ForeignKey(orm[u'myjobs.related_sessions'], null=False)),
            ('session', models.ForeignKey(orm[u'sessions.session'], null=False))
        ))
        db.create_unique(u'myjobs_related_sessions_mj_session', ['related_sessions_id', 'session_id'])

        # Adding M2M table for field ms_session on 'Related_Sessions'
        db.create_table(u'myjobs_related_sessions_ms_session', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('related_sessions', models.ForeignKey(orm[u'myjobs.related_sessions'], null=False)),
            ('session', models.ForeignKey(orm[u'sessions.session'], null=False))
        ))
        db.create_unique(u'myjobs_related_sessions_ms_session', ['related_sessions_id', 'session_id'])

        # Adding model 'CustomHomepage'
        db.create_table(u'myjobs_customhomepage', (
            (u'site_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True, primary_key=True)),
            ('logo_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'myjobs', ['CustomHomepage'])

        # Adding model 'Ticket'
        db.create_table(u'myjobs_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
        ))
        db.send_create_signal(u'myjobs', ['Ticket'])

        # Adding unique constraint on 'Ticket', fields ['ticket', 'user']
        db.create_unique(u'myjobs_ticket', ['ticket', 'user_id'])

        # Adding field 'User.first_name'
        db.add_column(u'myjobs_user', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'User.last_name'
        db.add_column(u'myjobs_user', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Ticket', fields ['ticket', 'user']
        db.delete_unique(u'myjobs_ticket', ['ticket', 'user_id'])

        # Deleting model 'Related_Sessions'
        db.delete_table(u'myjobs_related_sessions')

        # Removing M2M table for field mj_session on 'Related_Sessions'
        db.delete_table('myjobs_related_sessions_mj_session')

        # Removing M2M table for field ms_session on 'Related_Sessions'
        db.delete_table('myjobs_related_sessions_ms_session')

        # Deleting model 'CustomHomepage'
        db.delete_table(u'myjobs_customhomepage')

        # Deleting model 'Ticket'
        db.delete_table(u'myjobs_ticket')

        # Deleting field 'User.first_name'
        db.delete_column(u'myjobs_user', 'first_name')

        # Deleting field 'User.last_name'
        db.delete_column(u'myjobs_user', 'last_name')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'myjobs.customhomepage': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'CustomHomepage', '_ormbases': [u'sites.Site']},
            'logo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'myjobs.emaillog': {
            'Meta': {'object_name': 'EmailLog'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'received': ('django.db.models.fields.DateField', [], {})
        },
        u'myjobs.related_sessions': {
            'Meta': {'object_name': 'Related_Sessions'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mj_session': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mj_session_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['sessions.Session']"}),
            'ms_session': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ms_session_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['sessions.Session']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        },
        u'myjobs.ticket': {
            'Meta': {'unique_together': "(['ticket', 'user'],)", 'object_name': 'Ticket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        },
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gravatar': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_response': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opt_in_employers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'password_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_completion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['myjobs']