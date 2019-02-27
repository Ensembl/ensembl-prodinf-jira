# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

DB_TYPES = {'cdna', 'compara', 'core', 'funcgen', 'otherfeatures', 'rnaseq', 'variation', 'vega', 'presite',
            'sangervega'}

DB_TYPES_CHOICES = ((db_type, db_type) for db_type in DB_TYPES)


class BaseTimestampedModel(models.Model):
    """
    Time stamped 'able' models objects, add fields to inherited objects
    """

    class Meta:
        abstract = True
        app_label = 'ensembl_production'
        ordering = ['-updated', '-created']

    #: created by user (external DB ID)
    created_by = models.IntegerField(blank=True, null=True)
    #: (auto_now_add): set when model object is created
    created_at = models.DateTimeField('Created on', auto_now_add=True, editable=False, null=True, help_text='Creation timestamp')
    #: Modified by user (external DB ID)
    modified_by = models.IntegerField(blank=True, null=True)
    #: (auto_now): set each time model object is saved in database
    modified_at = models.DateTimeField('Last Update', auto_now=True, editable=False, null=True, help_text='Last update timestamp')

class HasCurrent(models.Model):
    class Meta:
        abstract = True
        app_label = 'ensembl_production'

    is_current = models.IntegerField(default=1)


class WebData(BaseTimestampedModel):
    web_data_id = models.AutoField(primary_key=True)
    data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'web_data'

class AnalysisDescription(HasCurrent, BaseTimestampedModel):
    analysis_description_id = models.AutoField(primary_key=True)
    logic_name = models.CharField(unique=True, max_length=128)
    description = models.TextField(blank=True, null=True)
    display_label = models.CharField(max_length=256)
    db_version = models.IntegerField()
    web_data = models.ForeignKey(WebData,null=True, on_delete=models.SET_NULL)
    displayable = models.IntegerField()

    class Meta:
        db_table = 'analysis_description'
        app_label = 'ensembl_production'


class MasterAttrib(HasCurrent, BaseTimestampedModel):
    attrib_id = models.AutoField(primary_key=True)
    attrib_type_id = models.PositiveSmallIntegerField()
    value = models.CharField(max_length=80)

    class Meta:
        db_table = 'master_attrib'
        unique_together = (('attrib_type_id', 'value'),)
        app_label = 'ensembl_production'


class MasterAttribSet(HasCurrent, BaseTimestampedModel):
    attrib_set_id = models.PositiveIntegerField()
    attrib_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'master_attrib_set'
        unique_together = (('attrib_set_id', 'attrib_id'),)
        app_label = 'ensembl_production'


class MasterAttribType(HasCurrent, BaseTimestampedModel):
    attrib_type_id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'master_attrib_type'
        app_label = 'ensembl_production'


class MasterBiotype(HasCurrent, BaseTimestampedModel):
    biotype_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    is_dumped = models.IntegerField()
    object_type = models.CharField(max_length=10)
    db_type = models.CharField(max_length=128)
    attrib_type_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    biotype_group = models.CharField(max_length=10, blank=True, null=True)
    so_acc = models.CharField(max_length=64, blank=True, null=True)
    so_term = models.CharField(max_length=1023, blank=True, null=True)

    class Meta:
        db_table = 'master_biotype'
        app_label = 'ensembl_production'
        unique_together = (('name', 'object_type'),)


class MasterExternalDb(HasCurrent, BaseTimestampedModel):
    external_db_id = models.AutoField(primary_key=True)
    db_name = models.CharField(max_length=100)
    db_release = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=9)
    priority = models.IntegerField()
    db_display_name = models.CharField(max_length=255)
    type = models.CharField(max_length=18, blank=True, null=True)
    secondary_db_name = models.CharField(max_length=255, blank=True, null=True)
    secondary_db_table = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'master_external_db'
        app_label = 'ensembl_production'
        unique_together = (('db_name', 'db_release', 'is_current'),)


class MasterMiscSet(HasCurrent, BaseTimestampedModel):
    misc_set_id = models.PositiveSmallIntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=25)
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_length = models.PositiveIntegerField()

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'master_misc_set'


class MasterUnmappedReason(HasCurrent, BaseTimestampedModel):
    unmapped_reason_id = models.AutoField(primary_key=True)
    summary_description = models.CharField(max_length=255, blank=True, null=True)
    full_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'master_unmapped_reason'


class MetaKey(HasCurrent, BaseTimestampedModel):
    meta_key_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    is_optional = models.IntegerField(default=0)
    db_type = models.CharField(max_length=72)
    description = models.TextField(blank=True, null=True)
    is_multi_value = models.IntegerField()

    class Meta:
        db_table = 'meta_key'
        app_label = 'ensembl_production'
