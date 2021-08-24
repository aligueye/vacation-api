from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with, inputs, abort
from flask_sqlalchemy import SQLAlchemy
import utils

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Vacation request database model
class Vacation_Request_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    resolved_by = db.Column(db.Integer, nullable=False)
    request_created_at = db.Column(db.DateTime(), nullable=False)
    vacation_start_date = db.Column(db.DateTime(), nullable=False)
    vacation_end_date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'Vacation Request(author = {self.author}, status = {self.status}, ' + \
               f'resolved by = {self.resolved_by}, request_created_at = {self.request_created_at}, ' + \
               f'vacation_start_date = {self.vacation_start_date}, vacation_end_date = {self.vacation_end_date}\n'

db.create_all()

# Input verification/formatting
request_args = reqparse.RequestParser()
request_args.add_argument('id', type=int, help='ID required', required=True)
request_args.add_argument('author', type=int, help='Worker ID required', required=True)
request_args.add_argument('status', type=str, help='Vacation info required', required=True)
request_args.add_argument('resolved_by', type=int, help='Manager ID required', required=True)
request_args.add_argument('request_created_at', type=inputs.datetime_from_iso8601, required=True)
request_args.add_argument('vacation_start_date', type=inputs.datetime_from_iso8601, help='Vacation start date required', required=True)
request_args.add_argument('vacation_end_date', type=inputs.datetime_from_iso8601, help='Vacation end date required', required=True)

resource_fields = {
    'id': fields.Integer,
    'author': fields.Integer,
    'status': fields.String,
    'resolved_by': fields.Integer,
    'request_created_at': fields.DateTime,
    'vacation_start_date': fields.DateTime,
    'vacation_end_date': fields.DateTime,
}

# Basic CRUD for Vacation Request
# @ 'vacation/'
class Vacation_Request(Resource):
    
    # Get Vacation Request
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.get(args['id'])
        if not result:
            abort(404, message='Vacation request was not found')

        return result

    # Create Vacation Request
    @marshal_with(resource_fields)
    def put(self):
        args = request_args.parse_args()
        start = args['vacation_start_date'].timestamp()
        end = args['vacation_end_date'].timestamp()
        vacation_days_used = 0

        # Check if status is approved, pending, or rejected
        if args['status'] not in utils.VALID_STATUS:
            abort(400, message='Vacation request status invalid')

        # Check if id is unique
        result = Vacation_Request_Model.query.get(args['id'])
        if result:
            abort(400, message='Vacation request ID is not unique')
        
        # Check if vacation starts after end date
        if start > end:
            abort(400, message='Vacation cannot start after end')

        # Gets and counts all vacation request from author
        result = Vacation_Request_Model.query.filter_by(author = args['author']).all()

        if result:
            for request in result:
                vacation_days_used += utils.work_days_used(request.vacation_start_date, request.vacation_end_date)
            vacation_days_used += utils.work_days_used(args['vacation_start_date'], args['vacation_end_date'])

            # Checks if vacation limit has been reached by previous requests
            if vacation_days_used >= 30:
                abort(400, message='Employee has reached vacation day limit')

        # Creates new instance of Vacation Request Model
        vacation_request = Vacation_Request_Model(id=args['id'], author=args['author'], status=args['status'], 
                                                  resolved_by=args['resolved_by'], request_created_at=args['request_created_at'], 
                                                  vacation_start_date=args['vacation_start_date'], vacation_end_date=args['vacation_end_date'])

        db.session.add(vacation_request)
        db.session.commit()

        return vacation_request

    # Update Vacation Request
    @marshal_with(resource_fields)
    def patch(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.get(args['id'])
        if not result:
            abort(404, message='Vacation request was not found')

        if args['status']:
            if args['status'] in utils.VALID_STATUS:
                result.status = args['status']
            else:
                abort(400, message=f'Invalid status was used')

        db.session.commit()

        return result

    # Delete Vacation Request
    @marshal_with(resource_fields)
    def delete(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.get(args['id'])
        if not result:
            abort(404, message='Vacation request was not found')

        db.session.delete(result)
        db.session.commit()

        return 200

# Resource for employees to see vacation requests
# @ 'vacation/employee/
class Vacation_Request_Employee(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.filter_by(author=args['author']).all()
        if not result:
            abort(404, message='No vacation request exist under worker id')
        
        return result

#  Resource for employees to see requests filtered by status
# @ 'vacation/employee/filter
class Vacation_Request_Employee_Filter(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        if args['status'] in utils.VALID_STATUS:
            result = Vacation_Request_Model.query.filter_by(author=args['author'], status=args['status']).all()
        else:
            abort(400, message='Invalid status was used, must be \'pending\', \'approved\', or \'rejected\'')
        if not result:
            abort(404, message='No vacation requests matching filter criteria')

        return result


# Resource for workers to see remaining vacation days
# @ 'vacation/employee/remaining/'
class Vacation_Request_Remaining(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        count = 0
        result = Vacation_Request_Model.query.filter_by(author=args['author']).all()
        if not result:
            return 30
        
        for request in result:
            count += utils.work_days_used(request.vacation_start_date, request.vacation_end_date)

        return 30 - count, 200


# Resource for managers see request from their employees 
# @ 'vacation/manager/'
class Vacation_Request_Manager(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.filter_by(resolved_by=args['resolved_by']).all()
        if not result:
            abort(404, message='No vacation requests under manager id')

        return result

# Resource for managers to filter requests
# @ 'vacation/manager/filter
class Vacation_Request_Manager_Filter(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        if args['status'] in utils.VALID_MGT_STATUS:
            result = Vacation_Request_Model.query.filter(Vacation_Request_Model.resolved_by==args['resolved_by'], Vacation_Request_Model.status==args['status']).all()
        else:
            abort(400, message='Invalid status was used, must be \'pending\' or \'approved\'')
        if not result:
            abort(404, message=f'No vacation requests with given status under manager id')

        return result

# Resource for managers to see overlapping requests
# @ 'vacation/manager/overlap
class Vacation_Request_Manager_Overlap(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request_args.parse_args()
        result = Vacation_Request_Model.query.filter(Vacation_Request_Model.resolved_by==args['resolved_by'], Vacation_Request_Model.vacation_start_date < args['vacation_end_date'], Vacation_Request_Model.vacation_end_date > args['vacation_start_date']).all()
        
        if not result or len(result) == 1:
            abort(404, message='No vacation request overlapping with given vacation request')
        
        return result

api.add_resource(Vacation_Request, '/vacation/')
api.add_resource(Vacation_Request_Employee, '/vacation/employee')
api.add_resource(Vacation_Request_Employee_Filter, '/vacation/employee/filter')
api.add_resource(Vacation_Request_Remaining, '/vacation/employee/remaining')
api.add_resource(Vacation_Request_Manager, '/vacation/manager')
api.add_resource(Vacation_Request_Manager_Filter, '/vacation/manager/filter')
api.add_resource(Vacation_Request_Manager_Overlap, '/vacation/manager/overlap')

@app.route('/')
def home():
    return '<h1>Welcome to Vacation Request API</h1>'

if __name__ == '__main__':
    app.run(debug=True)