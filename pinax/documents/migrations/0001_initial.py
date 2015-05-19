# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import pinax.documents.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(upload_to=pinax.documents.models.uuid_filename)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentSharedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('document', models.ForeignKey(to='documents.Document')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('parent', models.ForeignKey(blank=True, null=True, to='documents.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='FolderSharedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('folder', models.ForeignKey(to='documents.Folder')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('bytes_used', models.BigIntegerField(default=0)),
                ('bytes_total', models.BigIntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='storage')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(to='documents.Folder', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+'),
        ),
        migrations.AlterUniqueTogether(
            name='foldershareduser',
            unique_together=set([('folder', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentshareduser',
            unique_together=set([('document', 'user')]),
        ),
    ]
