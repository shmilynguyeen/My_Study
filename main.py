from Mapping.Scoring import scoringCosine
from Mapping.Scoring import scoringDamerauLevenshsetein
import pypyodbc

class  Main(): 
    linkedinName = {}
    hooverName = {}

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
        conn  = self.getConnection()
        squery = " SELECT DISTINCT   linkedin_url ,  linkedin_Name_Clean FROM Linkedin_getURL WHERE Country ='ThaiLand'  "
        cusor = conn.cursor()
        cusor.execute(squery)
        result = cusor.fetchone()
        while result : 
            URL = result[0]
            self.linkedinName[URL] = result[1]
            result = cusor.fetchone()
        conn.close()

    def main(self): 

        # Search with linkedinName in Hoover Company Name  ! 
        for URL in self.linkedinName.keys(): 
            conn  = self.getConnection()
            linkedinName_Temp = self.linkedinName[URL]
            
            squery = " select DUNS, Company_Name_Clean from Hoover_Company_URL where Company_Name like N'%" + linkedinName_Temp +"%' "
            cusor = conn.cursor()
            cusor.execute(squery)
            result = cusor.fetchone()
            while result : 
                DUNS = result[0] # DUNS ID of Hoover Company ! 
                hooverName_Temp =  result[0]

                cosine = scoringCosine(linkedinName_Temp , hooverName_Temp)
                damLe = scoringDamerauLevenshsetein(linkedinName_Temp , hooverName_Temp)

                # Kiểm tra xem 2 tên công ty có giống nhau không ? 
                if( cosine > 0 and damLe <1):
                    squery_2 = """INSERT INTO [dbo].[Scoring_Temp]
                        ([Linkedin_URL]
                        ,[Linked_Comapny]
                        ,[DUNS]
                        ,[Hoover_Company]
                        ,[COSINE_Scoring]
                        ,[DAMLE_Scoring])
                    VALUES(?,?,?,?,?,?,?) """
                    value = [URL, linkedinName_Temp , DUNS, hooverName_Temp, cosine ,damLe]  
                    self.insertUpdateDB(squery_2, value)

                result = cusor.fetchone()
            conn.close()
if  __name__ == "__main__" : 
    mapping = Main()
    mapping.main()