"""
Middleware.

Middleware is a framework of hooks into Django`s request/response processing.

It`s a light, low-level “plugin” system for globally altering Django`s
input or output.

Each middleware component is responsible for doing some specific function.
"""

MIDDLEWARE = [
    # CORS is added to the middleware stack so that the Django server can
    # respond to requests from the frontend, which is hosted on a different
    # host / port.
    #
    # See: https://github.com/adamchainz/django-cors-headers
    "corsheaders.middleware.CorsMiddleware",
    # Default Django middlewares
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
