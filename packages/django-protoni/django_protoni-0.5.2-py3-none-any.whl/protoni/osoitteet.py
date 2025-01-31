# -*- coding: utf-8 -*-

from importlib.metadata import entry_points

from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView


class Index(RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    if 'django.contrib.auth' in settings.INSTALLED_APPS \
    and not self.request.user.is_authenticated:
      return settings.LOGIN_URL
    else:
      return settings.LOGIN_REDIRECT_URL
    # def get_redirect_url
  # class Index


urlpatterns = [
  path('', Index.as_view(), name='index'),
]


# Lisää kiinteät näkymät.
for entry_point in entry_points(group='django.nakymat'):
  try:
    moduuli = entry_point.load()
  except (ImportError, AttributeError):
    pass
  else:
    urlpatterns.append(
      path(
        entry_point.name + '/',
        include(moduuli)
      )
    )
    # else
  # for entry_point in entry_points


# Lisää asennetut osoitteistot.
for entry_point in entry_points(group='django.osoitteisto'):
  urlpatterns.append(
    path(
      entry_point.name + '/',
      include((entry_point.module_name, entry_point.name)),
    )
  )
  # for entry_point in entry_points
