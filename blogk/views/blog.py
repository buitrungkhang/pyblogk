from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config

from ..service.entry import EntryService
from ..forms import BlogCreateForm, BlogUpdateForm
from ..models.entry import Entry


@view_config(route_name='blog', renderer='../templates/blog_view.jinja2')
def blog_view(request):
	entry_id = int(request.matchdict.get('id', -1))
	entry = EntryService.get_by_id(request, entry_id)
	if not entry:
		return HTTPNotFound()

	return { 'entry': entry }

@view_config(route_name='blog_action', match_param='action=create', renderer='../templates/edit_blog.jinja2',
	permission='create')
def blog_create(request):
	entry = Entry()
	form = BlogCreateForm(request.POST)
	if request.method == 'POST' and form.validate():
		form.populate_obj(entry)
		request.dbsession.add(entry)
		return HTTPFound(location=request.route_url('home'))
	return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit', renderer='../templates/edit_blog.jinja2',
	permission='create')
def blog_update(request):
    blog_id = int(request.params.get('id', -1))
    entry = EntryService.get_by_id(request, blog_id)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('blog', id=entry.id,slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}