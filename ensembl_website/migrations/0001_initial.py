# Generated by Django 2.1.7 on 2019-04-23 13:01

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelpLink',
            fields=[
                ('help_link_id', models.AutoField(primary_key=True, serialize=False)),
                ('page_url', django_mysql.models.SizedTextField(blank=True, null=True, size_class=1)),
            ],
            options={
                'db_table': 'help_link',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HelpRecord',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Update')),
                ('help_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=255)),
                ('keyword', django_mysql.models.SizedTextField(blank=True, null=True, size_class=1)),
                ('data', models.TextField()),
                ('status', django_mysql.models.EnumField(choices=[('draft', 'draft'), ('live', 'live'), ('dead', 'dead')])),
                ('helpful', models.IntegerField(blank=True, null=True)),
                ('not_helpful', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'help_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FaqRecord',
            fields=[
            ],
            options={
                'verbose_name': 'FAQ',
                'proxy': True,
                'indexes': [],
            },
            bases=('ensembl_website.helprecord',),
        ),
        migrations.CreateModel(
            name='LookupRecord',
            fields=[
            ],
            options={
                'verbose_name': 'Lookup',
                'proxy': True,
                'indexes': [],
            },
            bases=('ensembl_website.helprecord',),
        ),
        migrations.CreateModel(
            name='MovieRecord',
            fields=[
            ],
            options={
                'verbose_name': 'Movie',
                'proxy': True,
                'indexes': [],
            },
            bases=('ensembl_website.helprecord',),
        ),
        migrations.CreateModel(
            name='ViewRecord',
            fields=[
            ],
            options={
                'verbose_name': 'Page',
                'proxy': True,
                'indexes': [],
            },
            bases=('ensembl_website.helprecord',),
        ),
    ]
