from db.database import Connection

connection = Connection()

class AdminAuth:
    def login(self, username):
        query = f"SELECT username, password FROM admin WHERE username = '{username}'"
        with connection:
            responce = connection.GET(query)
            return responce

    def register(self, username, password):
        query = f"INSERT INTO admin (username, password) VALUES ('{username}','{password}');"
        with connection:
            connection.POST(query)


class AdminServiceTicketAuth:
    def create_trip(self, origin, destination, departure_date, price, capacity):
        query = f"""
        INSERT INTO trip (origin, destination, departure_date, price, capacity)
        VALUES ('{origin}', '{destination}', '{departure_date}', {price}, {capacity});
        """
        with connection:
            connection.POST(query)

    def define_chair(self, number, trip_id):
        query = f"""
        INSERT INTO chair (number, trip_id)
        VALUES ({number}, {trip_id})
        """
        with connection:
            connection.POST(query)
            
    def update_trip(self, trip_id, departure):
        query = f"UPDATE trip SET departure_date = '{departure}' WHERE id = {trip_id}"
        with connection:
            connection.POST(query)

    def last_trip(self):
        query = "SELECT id FROM trip ORDER BY id DESC LIMIT 1"
        with connection:
            responce = connection.GET(query)
            return responce

    def get_special_trip(self, trip_id):
        query = f"SELECT id FROM trip WHERE id = {trip_id} and origin != 'test'"
        with connection:
            responce = connection.GET(query)
            return responce

    def delete_trip(self, trip_id):
        query = f"DELETE FROM trip WHERE id = {trip_id}"
        with connection:
            connection.POST(query)

    def undefine_chair(self, trip_id):
        query = f"DELETE FROM chair WHERE trip_id = {trip_id};"
        with connection:
            connection.POST(query)

    def all_trips(self):
        query = f"SELECT * FROM trip WHERE origin != 'test'"
        with connection:
            responce = connection.GET(query)
            return responce

    def all_users(self):
        query = """
        SELECT id, username, wallet, count(user_id) FROM users
        LEFT JOIN ticket
        ON users.id = ticket.user_id
        WHERE username != 'test'
        GROUP BY id, username, wallet, user_id
        """
        with connection:
            responce = connection.GET(query)
            return responce

    def issued_trip(self):
        query = "SELECT * FROM trip WHERE expired = 'true'"
        with connection:
            responce = connection.GET(query)
            return responce

    def sold_ticket(self):
        query = "SELECT * FROM ticket WHERE status IN ('paid', 'reserved', 'used')"
        with connection:
            responce = connection.GET(query)
            return responce
        
    def show_transaction(self, limit):
        query = f"SELECT * FROM transaction LIMIT {limit}"
        with connection:
            responce = connection.GET(query)
            return responce