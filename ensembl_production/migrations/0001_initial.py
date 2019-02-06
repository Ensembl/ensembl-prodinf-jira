# Generated by Django 2.1.5 on 2019-02-01 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisDescription',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('analysis_description_id', models.AutoField(primary_key=True, serialize=False)),
                ('logic_name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('display_label', models.CharField(max_length=256)),
                ('db_version', models.IntegerField()),
                ('displayable', models.IntegerField()),
            ],
            options={
                'db_table': 'analysis_description',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterAttrib',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('attrib_id', models.AutoField(primary_key=True, serialize=False)),
                ('attrib_type_id', models.PositiveSmallIntegerField()),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'master_attrib',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterAttribSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('attrib_set_id', models.PositiveIntegerField()),
                ('attrib_id', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'master_attrib_set',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterAttribType',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('attrib_type_id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'master_attrib_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterBiotype',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('biotype_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('is_dumped', models.IntegerField()),
                ('object_type', models.CharField(max_length=10)),
                ('db_type', models.CharField(max_length=128)),
                ('attrib_type_id', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('biotype_group', models.CharField(blank=True, max_length=10, null=True)),
                ('so_acc', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'master_biotype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterExternalDb',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('external_db_id', models.AutoField(primary_key=True, serialize=False)),
                ('db_name', models.CharField(max_length=100)),
                ('db_release', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(max_length=9)),
                ('priority', models.IntegerField()),
                ('db_display_name', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, max_length=18, null=True)),
                ('secondary_db_name', models.CharField(blank=True, max_length=255, null=True)),
                ('secondary_db_table', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'master_external_db',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterMiscSet',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('misc_set_id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=25, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('max_length', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'master_misc_set',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MasterUnmappedReason',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('unmapped_reason_id', models.AutoField(primary_key=True, serialize=False)),
                ('summary_description', models.CharField(blank=True, max_length=255, null=True)),
                ('full_description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'master_unmapped_reason',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('meta_id', models.AutoField(primary_key=True, serialize=False)),
                ('species_id', models.PositiveIntegerField(blank=True, null=True)),
                ('meta_key', models.CharField(max_length=40)),
                ('meta_value', models.TextField()),
            ],
            options={
                'db_table': 'meta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WebData',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('web_data_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'web_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MetaKey',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('is_current', models.IntegerField(default=1)),
                ('meta_key_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('is_optional', models.IntegerField(default=0)),
                ('db_type', models.CharField(max_length=72)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_multi_value', models.IntegerField()),
            ],
            options={
                'db_table': 'meta_key',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WebDataElement',
            fields=[
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('web_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='elements', serialize=False, to='ensembl_production.WebData')),
                ('data_key', models.CharField(max_length=32)),
                ('data_value', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'web_data_element',
                'managed': False,
            },
        ),
    ]
