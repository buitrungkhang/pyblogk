from ..models.user import User

class UserService(object):
	
	@classmethod
	def get_by_name(cls, request, name):
		query = request.dbsession.query(User)
		return query.filter(User.name == name).first()