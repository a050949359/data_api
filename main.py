import flask
from flask import request, jsonify, render_template
from flask_restful import Api, Resource
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
from resources.hello import NameForm

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'SECRET_KEY'
api = Api(app)
api.add_resource(Users, '/users/')
api.add_resource(User, '/user/<id>')

api.add_resource(Accounts, '/accounts/')
api.add_resource(Account, '/account/<id>')

@app.route('/', methods = ["GET"])
def home():
    return "Hello World"


@app.before_request
def auth():
    pass
    # token = request.headers.get("auth")
    # if token == "567":
    #     pass
    # else:
    #     response = {
    #         "msg":"invalid token"
    #     }
    #     code = 401
    #     return response, code

# @app.errorhandler(Exception)
# def handle_error(error):
#     status_code = 500
#     if type(error).__name__ == 'NotFound':
#         status_code = 404
#     else:
#         pass
#     return {"msg":type(error).__name__ }, status_code

@app.route('/account/<account_number>/deposit', methods = ["POST"])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values["money"]
    balance = account["balance"] + int(money)
    
    sql = """
        update accounts set balance = {} where account_number = '{}'
    """

    cursor.execute(sql.format(balance, account_number))
    db.commit()
    db.close()
    response = {
        "result":True
    }

    return jsonify(response) 

@app.route('/account/<account_number>/getmoney', methods = ["POST"])
def getmoney(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values["money"]
    if int(money) > account["balance"]:
        response = {
            "result":False,
            "msg":"餘額不足"
        }

        code = 400
    else:
        balance = account["balance"] - int(money)
        
        sql = """
            update accounts set balance = {} where account_number = '{}'
        """

        cursor.execute(sql.format(balance, account_number))
        db.commit()
        db.close()
        response = {
            "result":True
        }
        code = 200

    return jsonify(response), code 

def get_account(account_number):
    db = pymysql.connect("192.168.56.102", "harold", "123456", "assignment")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """select * from accounts where account_number = '{}' and deleted = False""".format(account_number)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

@app.route('/<name>')
def index(name):
    return render_template('user.html', name=name, dict1={'a':1, 'b':3, 'c':2}, seq = [1,2,3,4,5,6])

@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name=None):
    if name is not None:
        name = '<em>Yes Man</em>'
    
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('hello.html', form=form, name=name)

if __name__ == '__main__':
    app.run(port=5000)