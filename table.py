from datetime import datetime
import uuid

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
        self.states.append('A')

    def update_db(self, session=""):
        if session == "":
            # pull the current session with uuid
            # update just the state, replace entire list
            
            return

        if session == "start":
            # update a new object 

            return

        if session == "end":
            # pull the current session with uuid
            # add session_end, replace list

            return
        
        return
        

    def did_change_state(self, new_state):
        last_state = self.states[-1]

        if new_state != last_state:

            # A to XX
            if last_state == 'A':
                self.start_session(state)
                self.update_db('start')
            
            # not A to XX
            else:
                # XX to A
                if new_state == 'A':
                    self.end_session()
                    self.update_db('end')

                # XX to XX
                else:
                    self.states.append(new_state)
                    self.update_db()


                

            




        



    