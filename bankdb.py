import rethinkdb as r
connection=r.connect( "localhost", 28015).repl()
#cif- format - 10 digits long
#pan- format - 10 characters long
#account number- format-11 digits long, starting with 1,2 or 3
r.db_drop('bank').run()
r.db_create('bank').run()

bank=r.db('bank')
customer=bank.table('customer')
r.db('bank').table_create('customer',primary_key='cif').run()
r.db('bank').table('customer').insert([
    {
        'onlineAcc': False,
	    'dob': '24/08/1998',
        #'username':None,
        #'password': None,
        'pan':'AAAPL1234C',
 	    'cname':'Pavarakshana',
        'address' : None,
        'contact':
        {
            'email':'rakshanadevi98@gmail.com',
            'mobile':'9655496644'
        }
        ,
        'cif':'6000000501', #format-10 digits long
        'account':
        [
            {
                'number':'12345678901',
                'type':'Savings',
                'balance':8000,
                'minlimit':2000,
                'debitcardno':4591500135782859,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'25/10/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'07/08/2016',
                        'fromacc':'12345678906',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            },
            {
                'number':'12345678902',
                'type':'Current',
                'balance':30000,
                'minlimit':5000,
                'debitcardno':4591500135782879,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'08/08/2017',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'02/04/2017',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'01/06/2017',
                        'fromacc':'12345678901',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            }
         ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
	    'dob':'07/11/1997',
        #'username':None,
        #'password': None,
	    'pan':'AAAPL1234D',#10 characters
 	    'cname':'Eshu Diamond',
        'address' : None,
        'contact':
            {
                'email':'eshwar.muthusamy7@gmail.com',
                'mobile':'8072106807'
            },
        'cif':'6000000502', #format-10 digits long
        'account':
        [
            {
                'number':'12345678903',
                'type':'Savings',
                'balance':8000,
                'minlimit':2000,
                'debitcardno':4591500235982549,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'05/05/2017',
                        'toacc':'12345678905',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'05/08/2017',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'03/07/2017',
                        'fromacc':'12345678902',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            },
            {
                'number':'12345678904',
                'type':'Current',
                'balance':30000,
                'minlimit':5000,
                'debitcardno':4591500135781477,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'03/07/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'01/07/2017',
                        'fromacc':'12345678906',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            },
            {
                'number':'12345678905',
                'type':'FD',
                'balance':30000,
                'period':3,
                'branch':'Avadi',
                'ifsc':'IBOB0002201',
                'transaction':[]
            }
         ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
	    'dob':'12/09/1997',
        #'username':None,
        #'password': None,
	    'pan':'AAAPL1234E',
 	    'cname':'Deepak Vengatesh',
        'address' : None,
        'contact':
        {
            'email':'drdeepakvenky@gmail.com',
            'mobile':'7358758342'
        },
        'cif':'6000000503', #format-10 digits long
        'account':
        [
            {
                'number':'12345678906',
                'type':'Savings',
                'balance':50000,
                'minlimit':2000,
                'debitcardno':7491500235982549,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'01/02/2017',
                        'toacc':'12345678903',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'02/03/2017',
                        'toacc':'12345678904',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'03/04/2017',
                        'fromacc':'12345678902',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            },
            {
                'number':'12345678907',
                'type':'Current',
                'balance':100000,
                'minlimit':5000,
                'debitcardno':7591500135781477,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'04/05/2017',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'05/06/2017',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'06/07/2017',
                        'fromacc':'12345678902',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            }
        ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
	    'dob':'01/08/1998',
        #'username':None,
        #'password': None,
	    'pan':'AAAPL1234R',
 	    'cname':'Dharaa',
        'address' : None,
        'contact':
        {
            'email':'rcdharaa@gmail.com',
            'mobile':'9445155377'
        },
        'cif':'6000000504', #format-10 digits long
        'account':
        [
            {
                'number':'12345678908',
                'type':'Savings',
                'balance':75000,
                'minlimit':2000,
                'debitcardno':4547500235982549,
                'branch':'AnnaNagar',
                'ifsc':'IBOB0021094',
                'transaction':
                [
                    {
                        'date':'04/08/2017',
                        'toacc':'12345678903',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'05/11/2017',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':5000
                    },
                    {
                        'date':'07/08/2016',
                        'fromacc':'12345678903',
                        'toacc':'None',
                        'amt':10000
                    }
                ]
            }
        ] #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
	    'dob':'18/08/1998',
        #'username':None,
        #'password': None,
	    'pan':'AAAPL1234W',
 	    'cname':'Janani',
        'address' : None,
        'contact':
        {
            'email':'kumarakrishnanjanani@gmail.com',
            'mobile':'9884088715'
        },
        'cif':'6000000505', #format-10 digits long
        'account':
        [
            {
                'number':'12345678909',
                'type':'Savings',
                'balance':70000,
                'minlimit':2000,
                'debitcardno':9391500235982549,
                'branch':'Avadi',
                'ifsc':'IBOB0002201',
                'transaction':
                [
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':5000
                    }
                ]
            }
        ]

         #format-11 digits long, starting with 1,2 or 3
    },
    {
        'onlineAcc': False,
	    'dob':'31/12/1998',
        #'username':None,
        #'password': None,
	    'pan':'AAAPL1234Z',
 	    'cname':'Iswarya',
        'address' : None,
        'contact':
        {
            'email':'sankaraniswarya@gmail.com',
            'mobile':'9500096140'
        },
        'cif':'6000000506', #format-10 digits long
        'account':
        [
            {
                'number':'12345678910',
                'type':'Savings',
                'balance':70000,
                'minlimit':2000,
                'debitcardno':9391500235982549,
                'branch':'Avadi',
                'ifsc':'IBOB0002201',
                'transaction':
                [
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678906',
                        'fromacc':'None',
                        'amt':2000
                    },
                    {
                        'date':'07/08/2016',
                        'toacc':'12345678901',
                        'fromacc':'None',
                        'amt':5000
                    }
                ]
                }
            ]

         #format-11 digits long, starting with 1,2 or 3
    }
]).run()
customer.sync().run()
# print(r.db('bank').table('customer').run())
# checked=False
# #connection = r.connect(host=localhost, port=RDB_PORT)
# bank=r.db('bank')
# customer=bank.table('customer')
# phone='9655496644'
# mail='rakshanadevi98@gmail.com'
# cif_exists=customer.filter({"cif":"6000000502"}).distinct().run()
# print(cif_exists)
#     #cif_exists=cif_result['cif']
# if(cif_exists!=None):
#     for each_cus in cif_exists:
#         print(each_cus['contact'][0]['mobile'])
#         print(each_cus['contact'][0]['email'])
#         if(each_cus['contact'][0]['mobile']==phone and each_cus['contact'][0]['email']==mail):
#             onlineAcc_exists=each_cus['onlineAcc']
#             print(onlineAcc_exists)
#             if(onlineAcc_exists==False):
#                     checked=True
#                     print("True check",checked)
#             else:
#                     checked= False
# print( checked)
