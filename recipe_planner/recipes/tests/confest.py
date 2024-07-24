# import os
# import pytest
# from django.conf import settings

# os.environ['DJANGO_SETTINGS_MODULE'] = 'recipe_planner.settings'

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('TEST_DB_NAME', 'recipes'),
#         'USER': os.environ.get('DB_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
