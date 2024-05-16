"""
AUTH_USER_MODEL.

Default: 'auth.User'

The model to use to represent a User.

See "Substituting a custom User model":
https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#auth-custom-user

Warning: You cannot change the AUTH_USER_MODEL setting during the lifetime of a project
(i.e. once you have made and migrated models that depend on it) without serious effort.

It is intended to be set at the project start, and the model it refers to must be
available in the first migration of the app that it lives in.
"""

AUTH_USER_MODEL = "api.User"
