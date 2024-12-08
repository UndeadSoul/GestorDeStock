class employeeClass():
    def __init__(self):
        self.id = None
        self.rut = None
        self.name = None
        self.contactnumber = None
        self.email = None
        self.password = None
    
    def setId(self, id):
        self.id=id

    def getId(self):
        return self.id
    
    def setAllData(self,id,rut,name,contactnumber,email,password):
        self.id=id
        self.rut=rut
        self.name=name
        self.contactnumber=contactnumber
        self.email=email
        self.password=password

    def getAllData(self):
        return [self.id,self.rut,self.name,self.contactnumber,self.email,self.password]