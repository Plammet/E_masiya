from flask import Flask, render_template, request
from database import DBhandler
import sys

application = Flask(__name__)

DB = DBhandler()

@application.route("/")
def home():
    return render_template("main.html")

@application.route("/home")
def go_home():
    return render_template("main.html")

@application.route("/list")
def go_list():
    return render_template("lookaround.html")

@application.route("/review")
def view_review():
    return render_template("review_upload.html")

@application.route("/mystore")
def view_mystore():
    return render_template("bookmarked.html")

@application.route("/signup")
def go_signup():
    return render_template("signup.html")

@application.route("/login")
def go_login():
    return render_template("login.html")

@application.route("/shop_upload")
def go_shop_upload():
    return render_template("shop_upload.html")

@application.route("/menu_upload", methods=['POST', 'GET'])
def go_menu_upload():
    restaurant_name = request.form['restaurant_name']
    print(restaurant_name)
    return render_template("menu_upload.html", restaurant_name=restaurant_name)

@application.route("/review_upload")
def go_review_upload():
    return render_template("review_upload.html")

@application.route("/shop_list")
def view_shoplist():
    return render_template("lookaround.html")

@application.route("/post_result", methods=['POST', 'GET'])
def go_post_result():

    name = request.form['shop_name']
    address = request.form['shop_addr']
    phone = request.form['shop_phone']
    parking = request.form['parking']
    category = request.form['category']
    link  = request.form['link']
    open_time = request.form['open_time']
    close_time = request.form['close_time']
    noop = request.form['shop_time_no']
    breaktime = request.form['shop_time_break']
    global idx
    image_file= request.files['filename']
    image_file.save("static/Images/{}".format(image_file.filename))
    #교수님께 여쭤보니, .format 이 맞다고 하셔서.. ㅠㅠ
    print(name,address,phone,parking,category,link,open_time, close_time, noop, breaktime)
    return render_template("post_result.html", image_path="static/Images/"+image_file.filename, noop=noop, open_time = open_time, close_time = close_time, breaktime=breaktime, link=link, parking=parking, category=category, name=name, phone=phone, address=address)
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    