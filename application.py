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
    name = request.form['name']
    print(name)
    return render_template("menu_upload.html", name=name)

@application.route("/review_upload", methods=['POST', 'GET'])
def go_review_upload():
    return render_template("review_upload.html")


@application.route("/shop_list")
def view_shoplist():
    return render_template("lookaround.html")

# 리뷰 등록
@application.route("/post_review_upload", methods=['POST', 'GET'])
def go_post_review_upload():
    time_r=request.form['time_r']
    rating=request.form['rating']
    mood=request.form['mood']
    menuName=request.form['menuName']
    menu1_rating=request.form['menu1-rating']
    spicy=request.form['spicy']
    reviewText=request.form['reviewText']
    global idx
    image_file_r = request.files['filename']
    image_file_r.save("static/Images/{}".format(image_file_r.filename))
    
    if DB.insert_review(time_r, rating, mood, menuName, menu1_rating, spicy, image_file_r.filename):
        return render_template("post_review_upload.html", image_path_r="static/Images/"+image_file_r.filename, time_r=time_r, rating=rating, mood=mood, menuName=menuName, menu1_rating=menu1_rating, spicy=spicy, reviewText=reviewText)

# 메뉴 등록
@application.route("/post_menu_upload", methods=['POST', 'GET'])
def go_post_menu_upload():
    name = request.form['name']
    menuName=request.form['menuName']
    price=request.form['price']
    spicy=request.form['spicy']
    etc=request.form['etc']
    global idx
    image_file_m = request.files['filename']
    image_file_m.save("static/Images/{}".format(image_file_m.filename))
    if DB.insert_menu(menuName, price, spicy, image_file_m.filename):
        return render_template("post_menu_upload.html", image_path_m="static/Images/"+image_file_m.filename, name=name, menuName=menuName, price=price, spicy=spicy, etc=etc)


# 맛집 등록
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
    image_file = request.files['filename']
    image_file.save("static/Images/{}".format(image_file.filename))
    
    if DB.insert_restaurant(name, address, phone, parking, category, link, open_time, close_time, noop, breaktime, image_file.filename):
        return render_template("post_result.html", image_path="static/Images/"+image_file.filename, name = name, address = address, phone = phone, parking = parking, category = category, link = link, open_time = open_time, close_time = close_time, noop = noop, breaktime = breaktime)
    else:
        return "Restaurant name already exist!"
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    