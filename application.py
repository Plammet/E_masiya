from flask import Flask, render_template, request
import sys
application = Flask(__name__)


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

@application.route("/post_result", methods=['POST', 'GET'])
def go_post_result():
    name = request.form['shop_name']
    address = request.form['shop_addr']
    phone = request.form['shop_phone']
    parking = request.form['parking']
    category = request.form['category']
    link  = request.form['link']
    time = request.form['shop_time']
    noop = request.form['shop_time_no']
    special = request.form['shop_time_special']
    breaktime = request.form['shop_time_break']
    
    print(name,address,phone,parking,category,link,time,noop,special,breaktime)
    return render_template("post_result.html", time=time, noop=noop, special=special, breaktime=breaktime, link=link, parking=parking, category=category, name=name, phone=phone, address=address)
    
    
@application.route("/register_menu")
def reg_menu():
    return render_template("menu_upload.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    