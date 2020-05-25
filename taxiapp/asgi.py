"""
ASGI config for taxiapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/

Question:  Try to answer the “why” along with the “what” and “how”. For example, why did we use Redis over an in-memory
layer for Django Channels?

"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxiapp.settings')

application = get_asgi_application()
