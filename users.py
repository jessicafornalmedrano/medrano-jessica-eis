# users.py
from connector import Connector

class Users:

    @staticmethod
    def check_user(username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        try:
            Connector.cursor.execute(query, (username, password))
            result = Connector.cursor.fetchone()
            if result is None:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error checking user: {e}")
            return False
