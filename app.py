import datetime

from flask import Flask
from flask import flash, render_template, request, url_for, session, redirect

from auth import Auth
from call import Call
from customer import Customer

app = Flask(__name__)
app.secret_key = b'J.;0ajk>,m8jkLIn89hans*jkj90($'


def is_logged_in():
    return 'username' in session


def is_valid_customer_id(customer_id):
    '''If the given customer ID matches up to an actual customer record,
    return True. If not, return False.'''
    customers = Customer.get_all()
    for cust in customers:
        if cust.customer_id == customer_id:
            return True
    return False


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        auth = Auth()
        if auth.login(username, password):
            session['username'] = username
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
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        auth = Auth()
        current_user = auth.get_current_user()
        current_user = current_user['user_id']
        cust = Customer(request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone'), request.form.get('email'),
                 request.form.get('address1'), request.form.get('address2'), request.form.get('postal_code'), request.form.get('city'), request.form.get('country'), added_by=current_user)
        cust.save()
        return redirect(url_for('show_customers'))
    return render_template('customer/add.html')


@app.route("/customers/<int:customer_id>/edit/", methods=['GET', 'POST'])
def edit_customer(customer_id):
    '''Check for logged in user. Check for valid customer id.
    If GET, show the page to edit the given customer.
    If POST, do the following:
    1. Get data from the POST request.
    2. Get a Customer object from the Customer class, that matches the
       given customer_id. This object will contain the OLD data.
    3. Set the values for the customer object - use the data you got
       from the POST request.
    4. Save the customer object.
    5. Redirect to /customers/ page.'''
    if not is_logged_in():
        return redirect(url_for('login'))
    if not is_valid_customer_id(customer_id):
        #flash message saying no cust exists
        return redirect(url_for('show_customers'))
    if request.method == 'POST':
        auth = Auth()
        current_user = auth.get_current_user()
        current_user = current_user['user_id']
        cust = Customer(request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone'), request.form.get('email'),
                 request.form.get('address1'), request.form.get('address2'), request.form.get('postal_code'), request.form.get('city'), request.form.get('country'), customer_id ,current_user)
        cust.save()
        return redirect(url_for('show_customers'))

    customer = Customer.get(customer_id)
    print(customer.email)
    return render_template('customer/edit.html', customer=customer)



@app.route("/customers/<int:customer_id>/")
def show_customer(customer_id):
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get a list of calls that are associated with the given customer id.
    Render the 'customer/show-one.html' template with the above data.'''
    if not is_valid_customer_id(customer_id):
        #flash message saying no cust exists
        return redirect(url_for('show_customers'))
    if not is_logged_in():
        #flash message saying log in
        return redirect(url_for('login'))
    customer = Customer.get(customer_id)
    calls = Call.get_for_customer(customer_id)
    return render_template('customer/show-one.html', customer=customer, calls=calls)


@app.route("/calls/add/<int:customer_id>", methods=['POST'])
def add_call(customer_id):
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get the user_id of the currently logged-in user.
    Get the current date-time.
    Get the notes from the POST request.
    Use the above data to create a new Call object. Save it.
    Redirect to the /customers/<customer_id>/ page.'''
    if not is_valid_customer_id(customer_id):
        #flash message saying no cust exists
        return redirect(url_for('show_customers'))
    if not is_logged_in():
        #flash message saying log in
        return redirect(url_for('login'))
    auth = Auth()
    current_user = auth.get_current_user()
    current_user = current_user['user_id']
    call_message = request.form.get('call_message', None)
    call = Call(customer_id,current_user,call_message)
    call.save()
    return redirect(url_for('show_customer', customer_id=customer_id))
