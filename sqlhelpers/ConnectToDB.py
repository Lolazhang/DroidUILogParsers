import MySQLdb
class ConnectToDB:
    def __init__(self):
        
        self.username="li"
        self.password="abcd1234"
        
        #self.read(res)
    def importSource(self,schema):
        cursor=self.db.cursor()
        sql=open(schema).read()
        cursor.execute(sql)
        cursor.close()
    def connect(self,dbname):
        self.db=MySQLdb.connect(host='localhost',user=self.username,passwd=self.password,db=dbname)
        self.cursor=self.db.cursor()        
        
      
        
    
        
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
    def read(self,res):
        f=file(res,'r')
        while True:
            line=f.readline()
            if not line:
                break
            content=line.strip().split('=')
            item=content[0]
            value=content[1]
            #print item,value
            if item=='user':
                self.username=value
            if item=='password':
                self.password=value
        
    
