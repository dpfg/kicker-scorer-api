from flask_restful import Resource, Api

class HealthCheck(Resource):
    def get(self):
        return {'alive': 'true'}
