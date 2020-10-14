from datetime import datetime
import uuid
from mongoengine import connect
from models import *

connect("iot", host="mongodb+srv://root:0NqePorN2WDm7xYc@cluster0.fvp4p.mongodb.net/iot?retryWrites=true&w=majority")

class Table:
    table_id = None
    session_id = None
    session_start = None
    session_end = None
    states = []

    def __init__(self, table_id):
        self.table_id = table_id
        self.states.append(0)

    def start_session(self, state):
        # create UUID
        self.session_id = uuid.uuid4()
        time_now = datetime.now()
        self.session_start = time_now
        self.states.append(state)

    def end_session(self):
        time_now = datetime.now()
        self.session_end = time_now
        self.states.append(0)

    def reset_session(self):
        self.table_id = None
        self.session_id = None
        self.session_start = None
        self.session_end = None
        self.states = []

    def update_db(self, session_status=""):
        if session_status == "":
            # pull the current session with uuid
            # update just the state, replace entire list
            session = Session.objects.get(sessionId=self.session_id)
            current_states = self.states
            session.update(set__states=current_states)
            return

        if session_status == "start":
            # update a new object 
            session = Session(
                sessionId = self.session_id,
                sessionStart = self.session_start,
                sessionEnd = self.session_end,
                states = self.states,
                tableId = self.table_id
            )
            test = session.save()

            return

        if session_status == "end":
            # pull the current session with uuid
            # add session_end, replace list
            session = Session.objects.get(sessionId=self.session_id)
            current_states = self.states
            session.update(set__states=current_states, set__sessionEnd = self.session_end)
            self.reset_session()
            return
        
        return
        

    def did_change_state(self, new_state):
        last_state = self.states[-1]

        if new_state != last_state:

            # A to XX
            if last_state == 0:
                self.start_session(new_state)
                self.update_db('start')
            
            # not A to XX
            else:
                # XX to A
                if new_state == 0:
                    self.end_session()
                    self.update_db('end')

                # XX to XX
                else:
                    self.states.append(new_state)
                    self.update_db()

    def print_states(self):
        return self.session_id, self.session_start, self.session_end, self.states