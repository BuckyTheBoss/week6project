import sqlite3
from flask import session


from db import Db

class Auth:
    def create_user(self, username, password):
        '''Create a user with given password'''
        db = Db()
        data = (username, password)
        db.execute('insert into user (username, password) values (?, ?)', data)


    def login(self, username, password):
        '''If we have a user with the given user name and password, return True.
        Otherwise, return False.'''
        pass


    def logout(self):
        session.pop('username', None)


    def is_logged_in(self):
        return 'username' in session


    def get_current_user(self):
        if self.is_logged_in():
            db = Db()
            data = (session['username'],)
            db.execute('select * from user where username = ?', data)
            row = db.fetchone()
            return row
        return None

    def has_user(self, username):
        db = Db()
        db.execute('select count(1) from user where username = ?', (username,))
        row = db.fetchone()
        count = row[0]
        return count > 0

    def get_by_user_id(self, user_id):
        '''Get a row containing user info for the given user id.
        Return None if there is no matching user.'''
        pass
