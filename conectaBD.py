import psycopg2

# Este se ejecuta aqui mismo


class db:
    def __init__ (self):
         self.conn = psycopg2.connect(database="proyecto",
                        user="postgres",
                        host="localhost",
                        password="123",
                        port="5432")
         self.cur = self.conn.cursor()
        
        #self.conn = psycopg2.connect(database="bf0woobuhcquehmyupzj",
         #               user="uu5hzcftam1qjhvv2zta",
          #              host="bf0woobuhcquehmyupzj-postgresql.services.clever-cloud.com",
           #             password="bi3kj2lAy1jltL9tFvCO",
            #            port="5432")
        #self.cur = self.conn.cursor()

    def ingresadatos(self, str1):
        try:
            self.cur.execute(str1)
            self.conn.commit()
            return True
        except Exception as id:
            self.cur.execute("ROLLBACK")
            self.conn.commit()
            print(id)
            return False

    def cerrarconeta(self):
        self.conn.close()
