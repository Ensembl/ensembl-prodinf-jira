CHANGELOG - Ensembl Prodinf Jira Extract
========================================
2.0.5
-----
- Extends JIRA query limit to 1000 items
2.0.4
-----
- Update ensembl-djcore dependency to range from pypi
2.0.0
-----
- update Connection credentials to Token base
1.2.0
-----
- Added Business Rules to allow only one credentials operating at a time
- fixes 500 erros when issue with credentials and fernet token
v1.1.2
------
- Change auth system to use authentication token
v1.1.1
------
- Updated templates to accommodate dark themes
- Fixe Intentions issue types retrieval (Epic -> Stories)
v1.0
------
- Moved from initial production services monolithic application (https://github.com/Ensembl/ensembl-production-services)
- Django standard layout / templates integration (enable backend skinning)
- Changed namespace to `ensembl.production.jira` 
- Changed app name to `ensembl_jira` 
- Updated layout to fit expected Portable APP layout (css / files locations / Patterns)
