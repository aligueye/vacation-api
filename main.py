import datetime
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, inputs, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt, timedelta
import utils
import pytz

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
        return f"Vacation Request(author = {self.author}, status = {self.status}, \n \
                resolved by = {self.resolved_by}, request_created_at = {self.request_created_at}, \n \
                vacation_start_date = {self.vacation_start_date}, vacation_end_date = {self.vacation_end_date}"

db.create_all()

# FIXME: '' xor ""
# Input verification
vacation_request_put_args = reqparse.RequestParser()
vacation_request_put_args.add_argument("id", type=int, help="ID required")
vacation_request_put_args.add_argument("author", type=int, help="Worker ID required", required=True)
vacation_request_put_args.add_argument("status", type=str, help="Vacation info required", required=True)
vacation_request_put_args.add_argument("resolved_by", type=int, help="Manager ID required", required=True)
vacation_request_put_args.add_argument('request_created_at', type=inputs.datetime_from_iso8601, help="Creation date required", required=True)
vacation_request_put_args.add_argument('vacation_start_date', type=inputs.datetime_from_iso8601, help="Vacation start date required", required=True)
vacation_request_put_args.add_argument('vacation_end_date', type=inputs.datetime_from_iso8601, help="Vacation end date required", required=True)

vacation_request_patch_args = reqparse.RequestParser()
vacation_request_patch_args.add_argument("id", type=int)
vacation_request_patch_args.add_argument("author", type=int)
vacation_request_patch_args.add_argument("status", type=str)
vacation_request_patch_args.add_argument("resolved_by", type=int)
vacation_request_patch_args.add_argument('request_created_at', type=inputs.datetime_from_iso8601)
vacation_request_patch_args.add_argument('vacation_start_date', type=inputs.datetime_from_iso8601)
vacation_request_patch_args.add_argument('vacation_end_date', type=inputs.datetime_from_iso8601)

resource_fields = {
    'id': fields.Integer,
    'author': fields.Integer,
    'status': fields.String,
    'resolved_by': fields.Integer,
    'request_created_at': fields.DateTime,
    'vacation_start_date': fields.DateTime,
    'vacation_end_date': fields.DateTime,
}

class Vacation_Request(Resource):
    
    # Get vr by id
    @marshal_with(resource_fields)
    def get(self, vr_id):
        result = Vacation_Request_Model.query.get(vr_id)
        if not result:
            abort(404, message="Vacation Request was not found")

        return result

    # Create/Update vr
    @marshal_with(resource_fields)
    def put(self, vr_id):
        args = vacation_request_put_args.parse_args()
        start = args['vacation_start_date'].timestamp()
        end = args['vacation_end_date'].timestamp()
        now = dt.today().timestamp()
        vacation_days_used = 0

        # Check if id is unique
        result = Vacation_Request_Model.query.get(vr_id)
        if result:
            abort(400, message="Vacation Request ID is not unique")

        # Check if vacation begins in the past
        if now > start:
            abort(400, message='Vacation must take place in present')
        
        # Check if vacation starts after end date
        if start > end:
            abort(400, message='Vacation cannot start after end')

        # Gets all vacation request from author
        result = Vacation_Request_Model.query.filter_by(author = args['author']).all()

        # Counts workdays included in vacation 
        if result:
            for request in result:
                vacation_days_used += utils.work_days_used(request.vacation_start_date, request.vacation_end_date)
            
            # Checks if vacation limit has been reached by previous requests
            if vacation_days_used >= 30:
                abort(400, message="Employee has reached vacation day limit")

        # Checks if vacation limit has been reached by current requests
        vacation_days_used += utils.work_days_used(args['vacation_start_date'], args['vacation_end_date'])
        if vacation_days_used >=30:
            abort(400, message=f'Your vacation is too long. Only {30 - vacation_days_used} left')

        # Creates new instance of Vacation Request Model
        vacation_request = Vacation_Request_Model(id=vr_id, author=args['author'], status=args['status'], 
                                                  resolved_by=args['resolved_by'], request_created_at=dt.now(tz=pytz.utc), 
                                                  vacation_start_date=args['vacation_start_date'], vacation_end_date=args['vacation_end_date'])

        db.session.add(vacation_request)
        db.session.commit()

        return vacation_request

    # Update
    @marshal_with(resource_fields)
    def patch(self, vr_id):
        args = vacation_request_patch_args.parse_args()
        result = Vacation_Request_Model.query.get(vr_id)
        if not result:
            abort(404, message="Vacation Request was not found")

        if args['status']:
            result.status = args['status']
        if args['vacation_start_date']:
            result.vacation_start_date = args['vacation_start_date']
        if args['vacation_end_date']:
            result.vacation_end_date = args['vacation_end_date']

        db.session.commit()

        return 200

    # Delete vr
    def delete(self, vr_id):
        result = Vacation_Request_Model.query.get(vr_id)
        if not result:
            abort(404, message="Vacation Request was not found")

        db.session.delete(result)
        db.session.commit()

        return 200

api.add_resource(Vacation_Request, '/<string:vr_id>')

@app.route('/')
def home():
    return "<h1>Welcome to Vacation Request API</h1>"

if __name__ == '__main__':
    app.run(debug=True)