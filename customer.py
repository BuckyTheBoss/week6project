from db import Db


class Customer:
    def __init__(self, first_name, last_name, phone, email,
                 address1, address2, postal_code, city, country,
                 customer_id=None, added_by=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.customer_id = customer_id
        self.added_by = added_by

    def save(self):
        '''If self has been populated by database data - UPDATE.
        Otherwise - INSERT a new record.'''
        db = Db()
        if self.customer_id != None:
            query = 'UPDATE customer SET first_name = ?, last_name = ?, phone = ?, email = ?, address1 = ?, address2 = ?, postal_code = ?, city = ?, country = ?, added_by = ? WHERE customer_id = ?'
            data = (self.first_name, self.last_name, self.phone, self.email,self.address1, self.address2, self.postal_code, self.city, self.country, self.added_by, self.customer_id)
        else:
            query = 'INSERT INTO customer(first_name, last_name, phone, email, address1, address2, postal_code, city, country) VALUES(?,?,?,?,?,?,?,?,?)'
            data = (self.first_name, self.last_name, self.phone, self.email, self.address1, self.address2, self.postal_code, self.city, self.country)
        db.execute(query, data)
        db.commit()

    def build_from_row(row):
        if row is None:
            return None
        customer = Customer(row[0], row[1], row[2], row[3], row[4],
                            row[5], row[6], row[7], row[8], row[9])
        if len(row) >= 11:
            customer.customer_id = row[9]
            customer.added_by = row[10]
        return customer

    # Note: this is a CLASS function (no self!)
    def get(customer_id):
        '''Get a single Customer object that corresponds to the customer id.
        If none found, return None.'''
        query = 'select first_name, last_name, phone, email, address1, address2, postal_code, city, country, customer_id, added_by from customer where customer_id = ?'
        db = Db()
        db.execute(query,(customer_id,))
        row = db.fetchone()
        if row is None:
            return None
        return Customer.build_from_row(row)

    # Note: this is a CLASS function (no self!)
    def get_all():
        '''Get a list of Customer objects - one for each row in the 
        relevant table in the database.'''
        db = Db()
        db.execute('select first_name, last_name, phone, email, address1, address2, postal_code, city, country, customer_id, added_by from customer')
        rows = db.fetchall()
        cust_obj_list = []
        for row in rows:
            cust_obj_list.append(Customer.build_from_row(row))
        return cust_obj_list