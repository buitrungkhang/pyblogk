import sqlalchemy as sa
from ..models.entry import Entry

class EntryService(object):

	@classmethod
	def get_all(cls, request):
		query = request.dbsession.query(Entry)
		return query.order_by(sa.desc(Entry.created))

	@classmethod
	def get_by_id(cls, request, id):
		query = request.dbsession.query(Entry)
		return query.get(id)