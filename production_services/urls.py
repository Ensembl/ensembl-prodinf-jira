# -*- coding: utf-8 -*-
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from django.contrib import admin
from django.conf.urls import url, include
from ensembl_production_db.api.urls import schema_view

urlpatterns = [
    # Production Admin
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^', admin.site.urls),
    # Production DB API
    url(r'^production_db/api/', include('ensembl_production_db.api.urls')),
    url(r'^production_db/api/schema', schema_view),
]

admin.site.site_header = "Ensembl Production Services"
admin.site.site_title = "Ensembl Production Services"
admin.site.index_title = "Welcome to Ensembl Production Services"
