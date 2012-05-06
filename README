Introduction
============
The purpose of this library is to provide Django applications that share an auth database across multiple SLDs (second-level domains, i.e.
example.com, example2.com) to provide single-sign-on functionality for their users when one site is the "master" site. One use-case where 
this may be useful is for services who provide social networking integration and OAuth login for their users, but also provide integrated services 
for other sites and want to avoid separate application account setup and configuration for each "satellite" site.


Installation
============

Dependencies
------------

:PyCrypto: https://www.dlitz.net/software/pycrypto/

:django.contrib.auth: https://docs.djangoproject.com/en/1.3/topics/auth/ "Django Auth Documentation"

:django.contrib.sessions: https://docs.djangoproject.com/en/1.3/topics/http/sessions/ "Django Session Documentation"


More coming soon.

Required Settings
-----------------

``SSO_TOKEN_EXPIRES``: Time after which token is no longer valid (in seconds). Default is 5.