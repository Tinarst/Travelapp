from db.database import Connection

connection = Connection()

class Audit:
    
    def admin(self, action, detail=None):
        query = f"INSERT INTO auditlog (actor, action, detail) VALUES ('admin', '{action}', '{detail}')"
        with connection:
            connection.POST(query)
            
    def user(self, actor, action, detail=None):
        query = f"INSERT INTO auditlog (actor, action, detail) VALUES ('{actor}', '{action}', '{detail}')"
        with connection:
            connection.POST(query)
            
            
class Log:
    
    def info(self, msg):
        query = f"INSERT INTO log (level, msg) VALUES ('INFO', '{msg}')"
        with connection:
            connection.POST(query)
            
    def warning(self, msg):
        query = f"INSERT INTO log (level, msg) VALUES ('WARNING', '{msg}')"
        with connection:
            connection.POST(query)
            
    def error(self, msg):
        query = f"INSERT INTO log (level, msg) VALUES ('ERROR', '{msg}')"
        with connection:
            connection.POST(query)
            
    
    def critical(self, msg):
        query = f"INSERT INTO log (level, msg) VALUES ('CRITICAL', '{msg}')"
        with connection:
            connection.POST(query)
            
            
logger = Log()