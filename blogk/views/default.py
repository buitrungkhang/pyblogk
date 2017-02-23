from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember, forget

from sqlalchemy.exc import DBAPIError

from ..models import User
from ..service.entry import EntryService
from ..service.user import UserService
from ..forms import RegisterForm

import logging
log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='../templates/home_view.jinja2')
def home_view(request):
    log.debug('home view')
    entries = EntryService.get_all(request)
    return { 'entries': entries }

@view_config(route_name='auth', match_param='action=in', renderer='string', request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    log.debug('Username:%s', username)
    if username:
        user = UserService.get_by_name(request, username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers = headers)

@view_config(route_name='register', renderer='../templates/register_view.jinja2')
def register(request):
    form = RegisterForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}