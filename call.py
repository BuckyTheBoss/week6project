from db import Db

from auth import Auth

class Call:
    def __init__(self,customer_id,user_id,call_message,call_id=None,call_time=None):
        self.customer_id = customer_id
        self.user_id = user_id
        self.call_time = call_time
        self.call_message = call_message
        self.call_id = call_id
        self.username = Auth.get_username_by_user_id(user_id)

    def save(self):
        '''If self has been populated by database data - UPDATE.
        Otherwise - INSERT a new record.'''
        db = Db()
        if self.call_id != None:
            query = 'UPDATE phone_call SET customer_id = ?, call_message = ?, call_time = ?, user_id = ? WHERE call_id = ?'
            data = (self.customer_id, self.call_message, self.call_time, self.user_id,self.call_id)
        else:
            query = 'INSERT INTO phone_call(customer_id,user_id,call_message) VALUES(?,?,?)'
            data = (self.customer_id, self.user_id, self.call_message)
        db.execute(query, data)
        db.commit()

    def build_from_row(row):
        if row is None:
            return None
        call = Call(row[0], row[1], row[2], row[3], row[4])
        return call

    # Note: this is a CLASS function (no self!)
    def get_for_customer(customer_id, include_user=False):
        '''Return a list of Call objects for the given customer.
        (Bonus: if include_user is True, add a 'user' attribute/property
        to each Call object, containing all the info about the user who
        created the Call object.)'''
        db = Db()
        query = 'SELECT customer_id, user_id, call_message, call_id, call_time FROM phone_call WHERE customer_id = ?'
        db.execute(query, (customer_id,))
        rows = db.fetchall()
        call_list = []
        for row in rows:
            call_list.append(Call.build_from_row(row))
        return call_list


    def get(call_id):
        '''Get a single Call object that corresponds to the call id.
        If none found, return None.'''
        query = 'SELECT customer_id, user_id, call_message, call_id, call_time FROM phone_call WHERE call_id = ?'
        db = Db()
        db.execute(query,(customer_id,))
        row = db.fetchone()
        if row is None:
            return None
        return Call.build_from_row(row)

    # Note: this is a CLASS function (no self!)
    def get_all():
        '''Get a list of Call objects - one for each row in the 
        relevant table in the database.'''
        db = Db()
        db.execute('SELECT customer_id, user_id, call_message, call_id, call_time FROM phone_call')
        rows = db.fetchall()
        call_obj_list = []
        for row in rows:
            call_obj_list.append(Call.build_from_row(row))
        return call_obj_list
