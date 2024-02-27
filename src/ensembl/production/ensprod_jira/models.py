#   See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import base64
import re

from django.core.exceptions import ValidationError
from django.db import models
from fernet_fields import EncryptedCharField
from jira import JIRA, exceptions as jira_exceptions


def matches_filter(jira_issue, intentions_filter):
    fields_string = " ".join(filter(None, [
        getattr(jira_issue, field_name) for field_name in jira_issue.filter_on
    ]))
    escaped_filter = re.escape(intentions_filter)
    return re.search(escaped_filter, fields_string)


class JiraCredentials(models.Model):
    class Meta:
        verbose_name = 'Jira Credential'
        verbose_name_plural = 'Jira Credentials'
        app_label = "ensembl_jira"

    cred_id = models.AutoField(primary_key=True)
    cred_name = models.CharField("Name", unique=True, max_length=150, editable=False, default='Jira')
    cred_url = models.CharField("Access Url", max_length=255, default="https://www.ebi.ac.uk/panda/jira/")
    user = models.CharField("User Name", max_length=100)
    credentials = EncryptedCharField("Token", max_length=255, db_column='credentials',
                                     help_text="https://www.ebi.ac.uk/panda/jira/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens")

    def __str__(self):
        return self.cred_name

    def connect(self):
        jira = JIRA(server=self.cred_url, token_auth=self.credentials)
        return jira

    def clean(self):
        from datetime import datetime
        try:
            jira = self.connect()
            jira.session()
            today = datetime.now().strftime("Jira_%Y%m%d_%H%M%S")
            JiraCredentials.objects.filter(cred_name="Jira").update(cred_name=f"{today}")
            self.cred_name = "Jira"
            return super().clean()
        except jira_exceptions.JIRAError as e:
            raise ValidationError('Wrong credentials, try again')


class JiraManager(models.Manager):
    _field_list = ()

    def all(self):
        jira_credentials = JiraCredentials.objects.get(cred_name="Jira")
        jira = jira_credentials.connect()
        name_map = {field['name']: field['id'] for field in jira.fields()}
        jira_issues = jira.search_issues(self.model.jira_filter, expand='renderedFields', maxResults=300)
        return [self.model(issue=jira_issue, name_map=name_map) for jira_issue in jira_issues]

    def filter(self, filter_terms):
        issues = self.all()
        if filter_terms is not None:
            issues = [x for x in issues if matches_filter(x, filter_terms)]
        return issues


class JiraFakeModel(models.Model):
    """ Readonly fake models to allow easy JIRA ticket listing integration in Django backend. """

    # TODO turn into a proper model storing ensprod_jira host, ensprod_jira query to run (allowing updates on query without having to
    #  deliver app on github.
    class Meta:
        db_table = "ensprod_jira"
        app_label = 'ensembl_jira'

    export_template_name = "admin/ensprod_jira/jira_export.html"
    export_file_name = "export.txt"
    objects = JiraManager()
    fake_id = 1

    def __init__(self, issue, name_map):
        # shortcut attributes to jira_issues ones
        super().__init__()
        self.name_map = name_map
        self.permalink = issue.permalink
        self.key = issue.key
        self.summary = issue.fields.summary
        self.description = issue.fields.description
        self.contact = issue.fields.reporter.emailAddress


class Intention(JiraFakeModel):
    jira_filter = 'project="ENSINT" AND issuetype=Story AND fixVersion in unreleasedVersions() ' \
                  'ORDER BY fixVersion DESC, affectedVersion DESC, Rank DESC'
    template = 'admin/ensprod_jira/intention.html'
    filter_on = (
        'key',
        'summary',
        'description',
        'target_version',
        'affected_teams',
        'declaring_team'
    )

    class Meta:
        proxy = True
        app_label = 'ensembl_jira'
        auto_created = True
        verbose_name = "Release Intention"

    def __init__(self, issue, name_map):
        super().__init__(issue, name_map)
        self.declaring_team = getattr(issue.fields, name_map['Declaring Team']).value
        self.affected_teams = ', '.join([team.value for team in getattr(issue.fields, name_map['Affected Team'])])
        self.target_version = issue.fields.fixVersions[0].name if issue.fields.fixVersions else 'N/A'


class KnownBug(JiraFakeModel):
    jira_filter = 'project=ENSINT AND issuetype=Bug ' \
                  ' and status not in ("Resolved", "Closed", "Under review")' \
                  ' ORDER BY affectedVersion DESC, fixVersion DESC'
    template = 'admin/ensprod_jira/knownbug.html'
    filter_on = (
        'versions_list',
    )

    class Meta:
        proxy = True
        app_label = 'ensembl_jira'
        verbose_name = "Known bug"

    def __init__(self, issue, name_map):
        super().__init__(issue, name_map)
        self.declaring_team = getattr(issue.fields, name_map['Declaring Team']).value
        self.versions_list = ', '.join(v.name for v in issue.fields.versions)
        self.fix_version = ', '.join(v.name for v in issue.fields.fixVersions)
        self.workaround = getattr(issue.renderedFields, name_map['Work Around'])
        websites = getattr(issue.fields, name_map['Website']) or []
        self.affected_sites = ', '.join(w.value for w in websites)


class RRBug(JiraFakeModel):
    class Meta:
        proxy = True
        app_label = 'ensembl_jira'
        verbose_name = "Rapid Release Bug"

    template = 'admin/ensprod_jira/rapid.html'
    export_file_name = "known_bugs.inc"
    jira_filter = 'project=ENSRR ' \
                  'AND issuetype = Bug AND status not in (Closed, Done, "In Review")' \
                  'AND resolution is EMPTY ORDER BY updatedDate DESC'
    filter_on = (
        'key',
        'summary',
        'description',
    )

    def __init__(self, issue, name_map):
        super().__init__(issue, name_map)
        self.fix_version = ', '.join(v.name for v in issue.fields.fixVersions)
        self.versions_list = ', '.join(v.name for v in issue.fields.versions)


