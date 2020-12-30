import smartpy as sp
#KT1QccH45jTEZzyNwSHqR3yMwu2VpMpzALUe--> Delphinet

whitelist_id_t = sp.TNat
users_t = sp.big_map(tkey = sp.TAddress, tvalue = whitelist_id_t)

class Contrat(sp.Contract):
    def __init__(self,admin , issuer):
        self.init(TJM = sp.map(),
                  time = sp.map(),
                  op = sp.map(),
                  cli= sp.map(),
                  id = sp.map(),
                  validation = sp.map(),
                  count = 0,
                  users = users_t, 
                  admin = admin,
                  issuer = issuer,
                  
                  )


        
    def assertAdmin(self):
        sp.verify((sp.sender == self.data.admin), message = "only admin may update")
        
    def assertUser(self,user):
        
        sp.verify(self.data.users[user] == sp.nat(2))
        return user
        
    def assertOp(self,user):
        
        sp.verify(self.data.users[user] == sp.nat(0))
        return user
    
    def assertRessource(self,user):
        
        sp.verify(self.data.users[user] == sp.nat(1))
        return user
    
    
   

        
    def assertNotIssuer(self, user):
        sp.verify(~(self.data.issuer == user), message = "issuer is not a user")
        return user   
    
    def addUserWhitelist(self, user, whitelist_id):
        
        sp.if (whitelist_id.is_some()):
            self.data.users[user] = whitelist_id.open_some()
            
        sp.else:
            del self.data.users[user]

            
            
    @sp.entry_point
    def validateContrat(self):
        self.assertUser(sp.sender)
        self.data.validation[0]= True
        

    @sp.entry_point
    def add_all(self, all):
        
        self.data.op[self.data.count] = all.op 
        self.data.cli[self.data.count] =  all.cli
        self.data.TJM[self.data.count] = all.TJM
        self.data.time[self.data.count] =   all.temp
        self.data.id[self.data.count] = all.id
        self.data.validation[self.data.count] = False
        self.data.count +=1
        self.data.users[sp.address("tz1YDrxgE7aoDXN1FSWnzpCDYN7wRJuGVHZ9")]= sp.nat(2)
    @sp.entry_point
    def setAdmin(self, new_admin):
        self.assertAdmin()
        self.data.admin = new_admin
    
    @sp.entry_point
    def addUser(self, new_user_params):
        self.assertAdmin()
        new_user = self.assertNotIssuer(new_user_params.new_user)
        self.addUserWhitelist(new_user, new_user_params.new_user_whitelist)
        
 
  

    

   
@sp.add_test(name = "Testing giving Cryptobot a new name")
def test():
    test_bot =  Contrat(sp.address("tz1YDrxgE7aoDXN1FSWnzpCDYN7wRJuGVHZ9"),sp.address("tz1YDrxgE7aoDXN1FSWnzpCDYN7wRJuGVHZ9"))
    scenario = sp.test_scenario()
    scenario += test_bot
    
    # Test change_name function below
    
    scenario += test_bot.addUser(
            new_user = sp.address("tz1djN1zPWUYpanMS1YhKJ2EmFSYs6qjf4bW"), 
            new_user_whitelist = sp.some(2)
            ).run(sender = sp.address("tz1YDrxgE7aoDXN1FSWnzpCDYN7wRJuGVHZ9"))
            
    scenario += test_bot.addUser(
            new_user = sp.address("tz31YDrxgE7aoDXN1FSDczpCDYN7wRJuGVHZ9"), 
            new_user_whitelist = sp.some(1)
            ).run(sender = sp.address("tz1YDrxgE7aoDXN1FSWnzpCDYN7wRJuGVHZ9"))       
    
    
    scenario += test_bot.add_all(TJM=sp.nat(200),temp = sp.nat(30),op = sp.address("tz1ePT7nRT9ANnjzcdbREJHWmfEBJnS7rWtK"),cli = sp.address("tz1ePT7nRT9ANnjzcdbREJHWmfEBJnS7rWtK"), id = "id_contrat").run(sender = sp.address("tz1djN1zPWUYpanMS1YhKJ2EmFSYs6qjf4bW"))
    
    
    
    scenario += test_bot.validateContrat().run(sender =sp.address("tz1djN1zPWUYpanMS1YhKJ2EmFSYs6qjf4bW"))

    


  