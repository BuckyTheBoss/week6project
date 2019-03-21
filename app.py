import datetime

from flask import Flask
from flask import flash, render_template, request, url_for, session, redirect

from auth import Auth
from call import Call
from customer import Customer

app = Flask(__name__)
app.secret_key = b'J.;0ajk>,m8jkLIn89hans*jkj90($'


def is_logged_in():
    '''If there is a user currently logged in, return True.
    If not, return False.'''
    pass

def is_valid_customer_id(customer_id):
    '''If the given customer ID matches up to an actual customer record,
    return True. If not, return False.'''
    pass


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        auth = Auth()
        if auth.login(username, password):
            return redirect(url_for('show_customers'))
        else:
            flash('Could not log you in')
    return render_template('auth/login.html')


@app.route("/logout/")
def logout():
    auth = Auth()
    auth.logout()
    return redirect(url_for('login'))


@app.route("/customers/")
def show_customers():
    if not is_logged_in():
        return redirect(url_for('login'))
    customers = Customer.get_all()
    return render_template('customer/show-list.html', customers=customers)


@app.route("/customers/add/", methods=['GET', 'POST'])
def add_customer():
    '''Check for logged in.
    If GET, show the page to add a customer.
    If POST, do the following:
    1. Get data from the POST request.
    2. Also get the current user's ID.
    3. Create a new Customer object with all the above data.
    4. Save it to the database.
    5. Redirect to the /customers/ page.'''
    pass

@app.route("/customers/<int:customer_id>/edit/", methods=['GET', 'POST'])
def edit_customer(customer_id):
    '''Check for logged in customer. Check for valid customer id.
    If GET, show the page to edit the given customer.
    If POST, do the following:
    1. Get data from the POST request.
    2. Get a Customer object from the Customer class, that matches the
       given customer_id. This object will contain the OLD data.
    3. Set the values for the customer object - use the data you got
       from the POST request.
    4. Save the customer object.
    5. Redirect to /customers/ page.'''
    pass


@app.route("/customers/<int:customer_id>/")
def show_customer(customer_id):
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get a list of calls that are associated with the given customer id.
    Render the 'customer/show-one.html' template with the above data.'''
    pass


@app.route("/calls/add/", methods=['POST'])
def add_call():
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get the user_id of the currently logged-in user.
    Get the current date-time.
    Get the notes from the POST request.
    Use the above data to create a new Call object. Save it.
    Redirect to the /customers/<customer_id>/ page.'''
    pass
