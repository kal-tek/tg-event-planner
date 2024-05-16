"""
## Static Files.

Settings for `django.contrib.staticfiles`.

### STATIC_ROOT

**Default**: None

The absolute path to the directory where `collectstatic` will collect static files
for deployment.

**Example**: `/var/www/example.com/static/`

If the `staticfiles` contrib app is enabled (as in the default project template),
the `collectstatic` management command will collect static files into this
directory. See the how-to on managing static files for more details about usage.

### STATIC_URL

**Default**: None

URL to use when referring to static files located in `STATIC_ROOT`.

**Example**: `"static/"` or `"http://static.example.com/"`

If not `None`, this will be used as the base path for asset definitions (the
Media class) and the `staticfiles` app.

It must end in a slash if set to a non-empty value.

You may need to configure these files to be served in development and will
definitely need to do so in production.

#### Note

If `STATIC_URL` is a relative path, then it will be prefixed by the server-
provided value of `SCRIPT_NAME` (or `/` if not set). This makes it easier to
serve a Django application in a subpath without adding an extra configuration
to the settings.

See:

- https://docs.djangoproject.com/en/4.2/ref/settings/#static-files
- https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles
"""

from .base_dir import BASE_PATH

STATIC_ROOT = BASE_PATH / "staticfiles"

STATIC_URL = "static/"
