import os, tempfile, pytest, logging, unittest

from datetime import datetime, timedelta
from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import (
    create_recommendation,
    get_recommendation,
    get_recommendation_by_request,
    create_request,
    get_request,
    get_student_requests,
    accept_request,
    reject_request,
    cancel_request
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class RecommendationUnitTests(unittest.TestCase):
    def test_new_recommendation(self):
        recommend = Recommendation(1,1,"This is a recommendation")
        assert recommend.reqID == 1 
        assert recommend.staffID == 1 
        assert recommend.dateSubmitted.date() == datetime.today().date()
        assert recommend.comments == "This is a recommendation"

    
    def test_recommend_toJSON(self):
        recommend = Recommendation(1,1,"This is a recommendation")
        actual_json = recommend.toJSON()
        actual_json.pop('dateSubmitted')
        expected_json = {
            'recID': None,
            'reqID': 1,
            'staffID': 1,
            'comments':"This is a recommendation"
            }
        self.assertDictEqual(actual_json, expected_json)
        
class RecommendationIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
    
    def test_create_recommendation_accepted(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(1,2,deadline, "Unit Test Test")
        request.status = Status.ACCEPTED
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertTrue (rec)
    
    def test_create_recommendation_pending(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(1,2,deadline, "Unit Test Test")
        request.status = Status.PENDING
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertFalse (rec)
    
    def test_create_recommendation_cancelled(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(1,2,deadline, "Unit Test Test")
        request.status = Status.CANCELLED
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertFalse (rec)

    def test_create_recommendation_expired(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(1,2,deadline, "Unit Test Test")
        request.status = Status.EXPIRED
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertFalse (rec)
    
    def test_create_recommendation_rejected(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(3,2,deadline, "Unit Test Test")
        request.status = Status.REJECTED
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertFalse (rec)

    def test_create_recommendation_completed(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(1,2,deadline, "Unit Test Test")
        request.status = Status.COMPLETED
        rec = create_recommendation(request.reqID,1,"This is a recommendation")
        self.assertFalse (rec)
    
    def test_get_recommendations_by_r_equest(self):
        deadline = datetime.now() + timedelta(days=5)
        request = create_request(3,2,deadline, "Unit Test Test")
        request.status = Status.ACCEPTED
        rec  = create_recommendation(request.reqID,3,"I see your UnitTest but will it pass") 
        recommend = get_recommendation_by_request(request.reqID)
        assert recommend.reqID == request.reqID
        assert recommend.staffID == 3
        assert recommend.dateSubmitted == datetime.today().date()
        assert recommend.comments == "I see your UnitTest but will it pass"

        

  