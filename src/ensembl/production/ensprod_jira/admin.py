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

from datetime import datetime

from cryptography.fernet import InvalidToken
from django import forms
from django.contrib import admin, messages
from django.contrib.admin.views.main import ChangeList
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from fernet_fields import EncryptedCharField

from ensembl.production.djcore.admin import SuperUserAdmin
from ensembl.production.ensprod_jira.models import Intention, KnownBug, RRBug, JiraCredentials


@admin.register(JiraCredentials)
class CredentialsAdmin(admin.ModelAdmin, SuperUserAdmin):
    formfield_overrides = {
        EncryptedCharField: {'widget': forms.widgets.PasswordInput},
    }
    list_display = ('cred_name', 'cred_url', 'user')

    def save_prev(self, request, object_id):
        today = datetime.now().strftime("Jira_%Y%m%d_%H%M%S")
        JiraCredentials.objects.filter(cred_id=object_id).update(cred_name=f"{today}")
        messages.warning(request,
                         mark_safe(f"Credentials are invalid, please renew <br/>Previous saved in {today}"))

    def get_queryset(self, request):
        if ('add' or 'change') in request.GET:
            print("I n here")
            return super().get_queryset(request)
        else:
            print("I nTTT here")
            return super().get_queryset(request).only('cred_name', 'cred_url', 'user')

    def changelist_view(self, request, extra_context=None):
        try:
            return super().changelist_view(request, extra_context)
        except Exception as e:
            messages.warning(request, f"Invalid Token {e}")
            return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_add'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(request, object_id, form_url, extra_context)
        except InvalidToken as e:
            self.save_prev(request, object_id)
            return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_add'))


class JiraChangeList(ChangeList):
    title = "Blablabla"


class JiraAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/ensembl_jira/filter.js',)

    readonly_fields = []
    change_list_template = 'jira_issue_list.html'
    export_template_name = "intentions_export.html"
    export_file_name = "export.txt"
    title = "Jira Export"

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path('export', self.admin_site.admin_view(self.export_view), name='%s_%s_export' % info)
        ]
        return my_urls + urls

    def has_add_permission(self, request):
        # No add
        return False

    def has_delete_permission(self, request, obj=None):
        # No delete
        return False

    def has_view_permission(self, request, obj=None):
        # View allowed to anyone from staff
        return request.user.is_staff

    def has_module_permission(self, request):
        # Allow module access to staff
        return request.user.is_staff

    def changelist_view(self, request, extra_context=None):
        intentions = []
        try:
            intentions = self.model._default_manager.all()
            export_view_name = 'admin:' + '_'.join([self.model._meta.app_label, self.model._meta.model_name, 'export'])
        except Exception as e:
            export_view_name = None
            print("exception ", e)
            messages.warning(request, f"Something is wrong with JIRA connexion: {e}")
        extra_context = {
            'intentions': intentions,
            'export_view_name': export_view_name,
            'title': self.title
        }
        return super().changelist_view(request, extra_context)

    def export_view(self, request):
        context = dict(
            intentions=self.model._default_manager.filter(request.POST['intentions_filter'])
        )
        response = TemplateResponse(request, self.model.export_template_name, context, 'application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.model.export_file_name)
        return response


@admin.register(Intention)
class IntentionAdmin(JiraAdmin):
    title = "Ensembl Intentions Export"


@admin.register(KnownBug)
class KnownBugAdmin(JiraAdmin):
    title = "Ensembl Known Bugs Export"


@admin.register(RRBug)
class RRBugAdmin(JiraAdmin):
    title = "Rapid Release Bugs Export"
