import rethinkdb as r
connection=r.connect( "localhost", 28015).repl()
'''r.db_drop('bank').run()
r.db_create('bank').run()
'''
bank=r.db('bank')
'''customer=bank.table('customer')
r.db('bank').table_create('customer',primary_key='cif').run()
r.db('bank').table('customer').insert([
    {
        'onlineAcc': False,
        #'username':None,
        #'password': None,
        'contact':[
            {'email':'rakshanadevi98@gmail.com','mobile':'9655496644'}
        ],
        'cif':'6000000501', #format-10 digits long
        'account':[
            {'number':'12345678901'},
            {'number':'12345678902'}
         ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
        #'username':None,
        #'password': None,
        'contact':[
            {'email':'eshwarmuthusamy7@gmail.com','mobile':'8072106807'}
        ],
        'cif':'6000000502', #format-10 digits long
        'account':[
            {'number':'12345678903'},
            {'number':'12345678904'},
            {'number':'12345678905'}
         ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
        #'username':None,
        #'password': None,
        'contact':[
            {'email':'drdeepakvengy@gmail.com','mobile':'7358758342'}
        ],
        'cif':'6000000503', #format-10 digits long
        'account':[
            {'number':'12345678906'},
            {'number':'12345678907'}
         ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
        #'username':None,
        #'password': None,
        'contact':[
            {'email':'tigerchase@gmail.com','mobile':'9487316200'}
        ],
        'cif':'6000000504', #format-10 digits long
        'account':[{'number':'12345678908'}] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
        #'username':None,
        #'password': None,
        'contact':[
            {'email':'chandlerbing@gmail.com','mobile':'7502412333'}
        ],
        'cif':'6000000505', #format-10 digits long
        'account':
           [ {'number':'12345678909'}]
         #format-11 digits long, starting with 1,2 or 3
    }
]).run()
customer.sync().run()
print(r.db('bank').table('customer').run())
checked=False
#connection = r.connect(host=localhost, port=RDB_PORT)
bank=r.db('bank')'''
customer=bank.table('customer')
phone='9655496644'
mail='rakshanadevi98@gmail.com'
cif_exists=customer.filter({"cif":"6000000502"}).distinct().run()
print(cif_exists)
    #cif_exists=cif_result['cif']
if(cif_exists!=None):
    for each_cus in cif_exists:
        print(each_cus['contact'][0]['mobile'])
        print(each_cus['contact'][0]['email'])
        if(each_cus['contact'][0]['mobile']==phone and each_cus['contact'][0]['email']==mail):
            onlineAcc_exists=each_cus['onlineAcc']
            print(onlineAcc_exists)
            if(onlineAcc_exists==False):
                    checked=True
                    print("True check",checked)
            else:
                    checked= False
print( checked)'''
