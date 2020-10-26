from datetime import datetime, timedelta
import uuid
from mongoengine import connect
from models import Table as TableMongo
from models import Session

connect("iot", host="mongodb+srv://root:0NqePorN2WDm7xYc@cluster0.fvp4p.mongodb.net/iot?retryWrites=true&w=majority")

class Table:
    table_id = None
    session_id = None
    session_start = None
    session_end = None
    states = None
    coords = []
    # coords = [TL, TR, BL, BR]

    def __init__(self, table_id, coords):
        self.table_id = table_id
        self.states = [0]
        self.coords = coords

    def start_session(self, state):
        # create UUID
        self.session_id = uuid.uuid4()
        time_now = datetime.now() + timedelta(hours=8)
        self.session_start = time_now
        print(self.states)
        self.states.append(state)

    def end_session(self):
        time_now = datetime.now() + timedelta(hours=8)
        self.session_end = time_now
        self.states.append(0)
        
        print(self.states)

    def reset_session(self):
        self.session_id = None
        self.session_start = None
        self.session_end = None
        self.states = [0]
        print(self.states)

    def update_db(self, session_status=""):
        if session_status == "":
            # pull the current session with uuid
            # update just the state, replace entire list
            session = Session.objects.get(sessionId=self.session_id)
            current_states = self.states
            session.update(set__states=current_states)

            # update the table state
            table_object = TableMongo.objects.get(table=self.table_id)
            current_state = self.states[-1]
            table_object.update(set__state=current_state)
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
            session.save()

            # update the table state
            table_object = TableMongo.objects.get(table=self.table_id)
            current_state = self.states[-1]
            table_object.update(set__state=current_state)

            return

        if session_status == "end":
            # pull the current session with uuid
            # add session_end, replace list
            session = Session.objects.get(sessionId=self.session_id)
            current_states = self.states
            session.update(set__states=current_states, set__sessionEnd = self.session_end)
            self.reset_session()

            # update the table state
            table_object = TableMongo.objects.get(table=self.table_id)
            current_state = self.states[-1]
            table_object.update(set__state=current_state)
            return
        
        return
        

    def did_change_state(self, new_state):
        last_state = self.states[-1]

        if new_state != last_state:
            # 0 to 2
            if last_state == 0 and new_state == 2:
                self.start_session(new_state)
                self.update_db('start')
            
            # after session start
            # anything to 0
            elif last_state == 0 and new_state == 1:
                return
            else:
                # anything to 0
                if new_state == 0:
                    if self.is_valid_session():
                        self.end_session()
                        self.update_db('end')
                    else:
                        return

                # anything 1 to 2, or 2 to 1
                else:
                    if self.is_valid_session():
                        # means from 1 to 2, high chance means that
                        # someone left and the person immediately joins
                        # this is 1 - 2
                        if new_state == 2:
                            self.end_session()
                            self.update_db('end')

                            # new session for the fast guy
                            self.reset_session()
                            self.start_session(new_state)
                            self.update_db('start')
                        else: # this is 2 - 1
                            self.states.append(new_state)
                            self.update_db()
                    else: # if not valid
                        return

    def is_valid_session(self):
        # KIVVVVVV
        time_now = datetime.now() + timedelta(hours=8)
        time_difference = time_now - self.session_start
        return time_difference.total_seconds() >= 180


    def within_coordinates(self, x, y):
        bl_x, bl_y = self.coords[2][0], self.coords[2][1]
        tr_x, tr_y = self.coords[1][0], self.coords[1][1]

        if (x > bl_x and x < tr_x and y < bl_y and y > tr_y):
            return True
        else : 
            return False

    def print_states(self):
        return self.table_id, self.session_id, self.session_start, self.session_end, self.states, self.coords