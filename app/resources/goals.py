from flask import jsonify
from app import db, app
from app.resources import ProtectedResource
from app.models import MatchGoal
from datetime import datetime

class GoalResource(ProtectedResource):
    MATCH_COMPLETION_DELAY_SEC = 60 * 5 # 5 minutes

    def delete(self, goal_id):
        goal = MatchGoal.query.get(goal_id)
        if goal is None:
            return {"message" : "could not find goal"}, 400

        match = goal.get_match()
        last_goal_datetime = match.goals[-1].created
        completedInSec = (datetime.utcnow() - last_goal_datetime).total_seconds()

        if match.completed and completedInSec > GoalResource.MATCH_COMPLETION_DELAY_SEC:
            return { "message" : "match is completed"}, 400

        match.completed = False
        db.session.delete(goal)
        db.session.commit()

        return ""