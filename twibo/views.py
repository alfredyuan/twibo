from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from pyramid.renderers import render_to_response

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from twibo import twibo

from .Controllers import (
    CustomerController,
    LogController
    )


@view_config(route_name='home', renderer='home.mak')
def home(request):
    # try:
    #     one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # return {'one': one, 'project': 'twibo'}
    return {'customers':CustomerController.customer_list()}

@view_config(route_name='service', renderer='service.mak')
def service(request):
    return {'logs':LogController.log_list()}

@view_defaults(route_name='add_customer')
class ADDView(object):
    def __init__(self, request):
        self.request = request

    def post(self):
        params = self.request.params

        if params['tw_name'].strip()=='':
            return {'err_msg':'Twitter Screen Name cannot be empty','params':params}

        profile_pic = twibo.verifyTwitterAccount(params['tw_name'])

        if not profile_pic:
            return {'err_msg':'Twitter Account does not exist','params':params}

        if CustomerController.new_customer(params, profile_pic):
            return {'msg':'Customer '+params['tw_name']+' has been successfully registered', 'profile_pic':profile_pic};
        else:
            return {'err_msg':'This customer existed in our database already', 'params':params}

    def get(self):
        return {}


