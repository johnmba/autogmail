
import secrets
import string
import random

from validate_email_address import validate_email
from sqlite3 import connect


class Regdata:

    def __init__(self, username, mail_service_provider="gmail.com") -> None:
        self.name = username
        self.rand: int = None
        self.__db = self._con = connect("datahouse.db")
        self.__cur = self.__db.cursor()
        
        self.provider = mail_service_provider
    
    def generate_password(self, length:int):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break
        return password
    
    def check_mail(self, username):
        """
        check if address can receive mail
        """
        
        address = username + self.provider
        password = self.generate_password(length=12)
        sql = "SELECT address FROM emails where address = ?"

        try:
            status = False
            if not self.provider.startswith('.'):
                dot = self.provider[0]
                self.provider.lstrip(dot)
                address = f'{username}@{self.provider}'
            if self.__cur.execute(sql, address) and (addr := self.__cur.fetchone):
                status = validate_email(email=addr, verify=True)
            self.__db.close()
        except TimeoutError:
            status = "Timeout"
        finally:
            return {
                "username": username, "address": address, "password": password, "status": status
            }
        
    def user(self):
        """
        generate user name from user's name and a user can have as much as 500 user names
        """
        
        if self.rand is None:
            user =  self.check_mail(self.name) or  self.check_mail(self.name) (
            )
            return user
        random_number = random.randrange(1, self.rand)
        user = self.check_mail(
                self.name + str(random_number)
            ) or self.check_mail(
                self.name + str(random_number)
            )
        return user      
    
        
    def __call__(self, rand: int = None):
        """
        reg_data: dictionary containing all registration data
        register the generated data
        """
        self.rand = rand
        if rand is None:
            self.rand = 1000
        return self.user()
               
    
if __name__ == "__main__":
    app = Regdata(username="john")
    print(app.user())
    usr = app(rand=100)
    print(usr)
