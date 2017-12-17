from Mapping.Scoring import scoringCosine
from Mapping.Scoring import scoringDamerauLevenshsetein

class  Mapping(): 
    linkedinName = []
    hooverName = []

     ## Get connection string
    def getConnection(self):
        connection = pypyodbc.connect('Driver={SQL Server};'

                                     'Server=27.0.12.57;'

                                      'Database=VINTELLO_STAGING;'

                                      'uid=spider_user;pwd=Spider@123')
        return connection
    ### Execute command insert or update :D     
    def insertUpdateDB(self , query, value): 
        connection = self.getConnection()
        cursor = connection.cursor()
        SQLCommand = query
        cursor.execute(SQLCommand , value)
        connection.commit()
        connection.close()

    def getLinkedCompanyName(self) : 
        squery = """ """

    