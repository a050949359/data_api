from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("gender")
parser.add_argument("birth")
parser.add_argument("note")

class Users(Resource):
    def db_init(self):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        print(Resource)
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """select * from users where deleted = False"""
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        response = {
            'data': users
        }

        for user in users:
            dt = user['birth']
            user['birth'] = dt.strftime("%Y/%m/%d %H:%M:%S")

        return make_response(jsonify(response), 200)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-1-1",
            "note": arg["note"]
        }

        sql = """
            insert into users
            (name, gender, birth, note)
            values('{}','{}','{}','{}');
        """.format(user["name"],user["gender"],user["birth"],user["note"])
        reault = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }

        return jsonify(response)

class User(Resource):
    def get(self, id):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """select * from users where id = '{}' and deleted = False""".format(id)
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        response = {
            'data': users
        }

        for user in users:
            dt = user['birth']
            user['birth'] = dt.strftime("%Y/%m/%d %H:%M:%S")

        return jsonify(response)

    def patch(self, id):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        arg = parser.parse_args()

        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-1-1",
            "note": arg["note"]
        }

        query = []
        for key,value in user.items():
            if value != None:
                query.append(key + '=' + "'{}'".format(value))
        query = ",".join(query)
        sql = """UPDATE users SET {} where id = '{}' and deleted = False""".format(query, id)
        print(sql)
        result = cursor.execute(sql)
        users = cursor.fetchall()
        db.commit()
        db.close()
        response = {
            'result': True
        }

        return jsonify(response)

    def delete(self, id):
        db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """UPDATE users set deleted = True where id = '{}' and deleted = False""".format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        
        response = {
            'result': True
        }

        return jsonify(response)

        # db = pymysql.connect("192.168.56.102", "harold", "123456", "flask_demo")
        # cursor = db.cursor(pymysql.cursors.DictCursor)
        # sql = """delete from users where id = '{}'""".format(id)
        # cursor.execute(sql)
        # db.commit()
        # db.close()
        
        # response = {
        #     'result': True
        # }

        # return jsonify(response)