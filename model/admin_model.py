from auth.admin_auth import AdminServiceTicketAuth
from auth.audit_auth import Audit
from exception.ticketservice import InvalidDateTime
from auth.audit_auth import logger
import datetime


class AdminService:

    def __init__(self):
        self.auth = AdminServiceTicketAuth()
        self.audit = Audit()

    def create_trip(self, origin, destination, departure_date, price, capacity):
        try:
            departure_date = datetime.datetime.strptime(
                departure_date, "%Y-%m-%d %H:%M:%S"
            )
            if datetime.datetime.now() > departure_date:
                raise InvalidDateTime()
        except InvalidDateTime:
            print("Past date")
        except:
            print("Invalid DateTime")
        else:
            
            price = float(price)
            capacity = int(capacity)

            self.auth.create_trip(origin, destination, departure_date, price, capacity)

            trip_id = self.auth.last_trip()[0][0]

            print("Trip Created")
            
            logger.info(f"Admin Create a Trip {trip_id}")
            
            self.audit.admin("define trip", f"define trip ID {trip_id}")

            self.define_chair(capacity, trip_id)

    def define_chair(self, capacity, trip_id):
        for number in range(capacity):
            self.auth.define_chair(number + 1, trip_id)

        print("Chairs modified by capacity")
        
        logger.info(f"Admin Define Positions For Trip {trip_id}")
        
        self.audit.admin("define positions", f"define positions for trip ID {trip_id}")

    def delete_trip(self, trip_id: int):
        trip_id = int(trip_id)
        try:
            self.auth.get_special_trip(trip_id)[0][0]
        except IndexError:
            print("Trip Does not Exist")
        else:
            self.auth.undefine_chair(trip_id)
            self.audit.admin("undefine positions", f"Removing positions due to travel exclusion {trip_id}")
            
            self.auth.delete_trip(trip_id)
            self.audit.admin("delete trip", f"delete trip ID {trip_id}")

            print(f"Trip ID {trip_id} Deleted")
            
            logger.info(f"Admin Delete a Trip {trip_id}")
            
            
            
    def update_trip(self, trip_id: int, departure):
        trip_id = int(trip_id)
        
        try:
            self.auth.get_special_trip(trip_id)[0][0]
            departure_date = datetime.datetime.strptime(
                departure, "%Y-%m-%d %H:%M:%S"
            )
            if departure_date < datetime.datetime.now():
                raise InvalidDateTime()
        except IndexError:
            print("Trip Does not Exist")
        except InvalidDateTime:
            print("Can not update the trip to the past")
        except ValueError:
            print("Invalid Date Time")
        else:
            self.auth.update_trip(trip_id, departure_date)
            
            print(f"Trip ID {trip_id} Updated")
            
            logger.info(f"Trip ID {trip_id} Updated")
            
            self.audit.admin("update trip", f"Update Departure trip ID {trip_id} To {departure_date}")

    def all_trips(self):
        return self.auth.all_trips()

    def all_users(self):
        return self.auth.all_users()

    def issued_trip(self):
        return self.auth.issued_trip()

    def sold_ticket(self):
        return self.auth.sold_ticket()
    
    def show_transaction(self, limit=0):
        return self.auth.show_transaction(999999999 if limit == 0 else limit)