from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql

parser = reqparse.RequestParser()
parser.add_argument("balance")
parser.add_argument("account_number")

class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        db, cursor = self.db_init()
        sql = """select * from accounts where deleted = False"""
        cursor.execute(sql)
        accounts = cursor.fetchall()
        db.close()
        response = {
            'data': accounts
        }

        return jsonify(response)
    
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
        }

        sql = """
            insert into accounts
            (balance, account_number)
            values('{}', '{}');
        """.format(account["balance"], account["account_number"])

        reault = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }

        return jsonify(response)
    
class Account(Resource):
    def db_init(self):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """select * from accounts where id = '{}' and deleted = False""".format(id)
        cursor.execute(sql)
        account = cursor.fetchall()
        db.close()
        response = {
            'data': account
        }

        return jsonify(response)

    def patch(self, id):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        arg = parser.parse_args()

        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
        }
        query = []
        for key,value in account.items():
            if value != None:
                query.append(key + '=' + "'{}'".format(value))
        query = ",".join(query)
        sql = """UPDATE accounts SET {} where id = '{}' and deleted = False""".format(query, id)
        print(sql)
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': result
        }

        return jsonify(response)
    
    # def patch(self, id):
    #     db, cursor = self.db_init()
    #     arg = parser.parse_args()

    #     account = {
    #         "balance": arg["balance"],
    #         "account_number": arg["account_number"],
    #     }

    #     query = 'balance = balance + {}'.format(arg["balance"])
    #     sql = """UPDATE accounts SET {} where id = '{}' and deleted = False""".format(query, id)

    #     result = cursor.execute(sql)
    #     db.commit()
    #     db.close()
    #     response = {
    #         'result': True
    #     }

        return jsonify(response)
    
    def delete(self, id):
        db, cursor = self.db_init()
        sql = """UPDATE accounts set deleted = True where id = '{}' and deleted = False""".format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        
        response = {
            'result': True
        }

        return jsonify(response)