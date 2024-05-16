"""
ROOT_URLCONF.

Default: Not defined.

A string representing the full Python import path to your root URLconf,
for example "app.urls".

Can be overridden on a per-request basis by setting the attribute urlconf
on the incoming HttpRequest object.

See how Django processes a request for details:
https://docs.djangoproject.com/en/dev/topics/http/urls/#how-django-processes-a-request
"""

# You should not need to change this value.
ROOT_URLCONF = "event_planner.urls"
