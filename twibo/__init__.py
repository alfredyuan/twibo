from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .views import (
        ADDView
    )

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('add_customer','/add')
    config.add_view(ADDView, route_name='add_customer', attr='get', request_method='GET', renderer='add.mak')
    config.add_view(ADDView, route_name='add_customer', attr='post', request_method='POST', renderer='add.mak')
    config.add_route('service','/engine')
    config.scan()
    return config.make_wsgi_app()
