from flask import Flask, render_template, request
from database import DBhandler
from time import time
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

#찜한 맛집 조회 화면
@application.route("/mystore")
def view_mystore():
    return render_template("bookmarked.html")

#회원가입 화면
@application.route("/signup")
def go_signup():
    return render_template("signup.html")

#로그인 화면
@application.route("/login")
def go_login():
    return render_template("login.html")

#맛집 등록 화면
@application.route("/shop_upload")
def go_shop_upload():
    return render_template("shop_upload.html")

#메뉴 업로드 화면
@application.route("/menu_upload", methods=['POST', 'GET'])
def go_menu_upload():
    name = request.form['name']
    print(name)
    return render_template("menu_upload.html", name=name)

#리뷰 업로드 화면
@application.route("/review_upload", methods=['POST', 'GET'])
def go_review_upload():
    return render_template("review_upload.html")

#맛집 리스트
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
    
    timenow = str(int(time()))
    image_file_r = request.files['filename']
    image_file_r.save("static/Images/{}".format(timenow + image_file_r.filename))
    
    if DB.insert_review(time_r, rating, mood, menuName, menu1_rating, spicy, reviewText, image_file_r.filename):
        
        ################################################################################################### 
        # 일단은 이렇게 두고, 나중에 reviewList 페이지가 완성되면 reviewList 페이지로 이동하도록 변경하면 좋을것같아요 #
        ###################################################################################################
        
        return render_template("post_review_upload.html", image_path_r="static/Images/"+timenow+image_file_r.filename,time_r=time_r, rating=rating, mood=mood, menuName=menuName, menu1_rating=menu1_rating, spicy=spicy, reviewText=reviewText)

# 메뉴 등록
@application.route("/post_menu_upload", methods=['POST', 'GET'])
def go_post_menu_upload():
    name = request.form['name']
    menuName=request.form['menuName']
    price=request.form['price']
    spicy=request.form['spicy']
    etc=request.form['etc']
    global idx
    
    timenow = str(int(time()))
    image_file_m = request.files['filename']
    image_file_m.save("static/Images/{}".format(timenow + image_file_m.filename))
    if DB.insert_menu(name, menuName, price, spicy, etc, image_file_m.filename):
        
        ##################################################################################################### 
        # 일단은 이렇게 두고, 나중에 shop_detail 페이지가 완성되면 shop_detail 페이지로 이동하도록 변경하면 좋을것같아요 #
        #####################################################################################################
        
        return render_template("post_menu_upload.html", image_path_m="static/Images/"+timenow + image_file_m.filename, name=name, menuName=menuName, price=price, spicy=spicy, etc=etc)
    else:
        return "Menu name already exist!"


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
        return render_template("post_result.html", image_path="static/Images/"+ name + image_file.filename, name = name, address = address, phone = phone, parking = parking, category = category, link = link, open_time = open_time, close_time = close_time, noop = noop, breaktime = breaktime)
    else:
        return "Restaurant name already exist!"
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    