from flask import Flask, redirect, render_template, request, url_for, flash, session
from database import DBhandler
from time import time
import itertools
import hashlib
import random
import sys
import os
import math

application = Flask(__name__)
application.secret_key = os.urandom(24)

DB = DBhandler()

@application.route("/")
def home():
    all_data=DB.get_all_data()
    item = dict(sorted(all_data.items(), key=lambda x:x[1]['bookmarked'], reverse = True))
    randomRes = random.choice(list(item.keys()))
    
    data = dict(itertools.islice(item.items(), 0, 3))
    
    return render_template("main.html", data=data, randomRes=randomRes)


@application.route("/home", methods=['POST', 'GET'])
def go_home():
    return redirect(url_for('home'))

#찜한 맛집 조회 화면
@application.route("/mystore")
def view_mystore():
    
    if 'id' in session:
        user = session['id']
        bookmarked = DB.get_bookmarked_by_userID(user)
        
        data=DB.get_all_data()
        
        return render_template(
            "bookmark.html",
            data = data,
            bookmarked = bookmarked
        )
    
    else:
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('go_login'))
    
    
#회원가입 화면
@application.route("/signup")
def go_signup():
    return render_template("signup.html")

#회원가입
@application.route("/signup_post", methods=['POST'])
def register_user():
    ID = request.form['id']
    pw = request.form['pw']
    pwcheck = request.form['pwcheck']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if pw != pwcheck:
        flash("check your password!")
        return render_template("signup.html")
    else:
        if DB.insert_user(ID, pw_hash):
            return render_template("login.html")
        else:
            flash("user ID already exist!")
            return render_template("signup.html")
    

#로그인 화면
@application.route("/login")
def go_login():
    return render_template("login.html")

#로그인
@application.route("/post_login", methods=['POST'])
def login_user():
    id_ = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('list_restaurants'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")


    
#로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('list_restaurants')) #로그아웃 후 이동할 페이지


#맛집 등록 화면
@application.route("/shop_upload")
def go_shop_upload():
    return render_template("shop_upload.html")

#메뉴 업로드 화면
@application.route("/menu_upload/<name>/", methods=['POST', 'GET'])
def go_menu_upload(name):
    print(name)
    return render_template("menu_upload.html", name=name)

#메뉴 조회 화면
@application.route("/menus/<name>/")
def go_menu(name):
    data=DB.get_shop_byname(str(name))
    return render_template("menu_list.html", data=data)

#리뷰 업로드 화면(식당)
@application.route("/review_upload/<name>/")
def go_review_upload(name):
    data=DB.get_shop_byname(str(name))
    return render_template("review_upload.html", data=data, menuName="")

#리뷰 업로드 화면(식당, 메뉴)
@application.route("/review_upload/<name>/<menuName>/")
def go_review_upload_with_menu(name, menuName):
    data=DB.get_shop_byname(str(name))
    return render_template("review_upload.html", data=data, menuName=menuName)

#맛집 리스트(지도)
@application.route("/shop_map")
def view_shoplist():    
    return render_template("lookaround.html")

#######맛집 세부 화면 --> 동적 라우팅############
@application.route("/shop_detail/<name>/")
def view_shop_detail(name):
    
    data=DB.get_shop_byname(str(name))
    avg_rate=DB.get_avgrate_byname(str(name))
    if_bookmarked = 0
    
    if 'id' in session:
        user = DB.get_users_byID(session['id']).val()
        
        if 'bookmarked' in user:
            for bookmark in user['bookmarked']:
                if bookmark == name:
                    if_bookmarked = 1
        
    return render_template("shop_detail.html",data=data, avg_rate=avg_rate, bookmarked = if_bookmarked)


# 맛집 찜하기 기능
@application.route("/bookmark/<nextPage>/<name>")
def bookmark(nextPage, name):
    if 'id' in session:
        user = session['id']
        DB.bookmark(user, name)
        
        if nextPage == 'detail':
            return redirect(url_for('view_shop_detail', name=name))
    
        else:
            return redirect(url_for('list_restaurants'))
    
    else:
        flash("로그인이 필요한 기능입니다")
        return redirect(url_for('go_login'))

# 찜 해제하기 기능
@application.route("/bookmark_delete/<nextPage>/<name>")
def bookmark_delete(nextPage, name):
    if 'id' in session:
        user = session['id']
        DB.bookmark_delete(user, name)
        
        if nextPage == 'detail':
            return redirect(url_for('view_shop_detail', name=name))
    
        else:
            return redirect(url_for('list_restaurants'))
    
    else:
        flash("오류가 발생했습니다. 식당 정보 화면으로 돌아갑니다.")
        return redirect(url_for('view_shop_detail', name=name))
     

######맛집 세부 화면 - 리뷰 리스트 조회 화면 --> 동적 라우팅 : 식당 -> 메뉴 -> 리뷰#####
@application.route("/review_list/<name>/<menuName>/")
def view_review(name,menuName):
    
    data=DB.get_shop_byname(str(name))
    
    return render_template("review_list.html", data=data, menuName=menuName)


# 리뷰 등록
@application.route("/post_review_upload", methods=['POST', 'GET'])
def go_post_review_upload():

    restaurant=request.form['restaurant']
    time_r=request.form['time_r']
    clean_rating=request.form['rating']
    menuName=request.form['menuName']
    menu1_rating=request.form['menu1-rating']
    spicy=request.form['spicy']
    reviewText=request.form['reviewText']
   
    global idx
    
    timenow = str(int(time()))
    image_file_r = request.files['filename']
    imageName = restaurant + timenow + image_file_r.filename
    image_file_r.save("static/Images/{}".format(imageName))
    
    if DB.insert_review(restaurant, time_r, clean_rating, menuName, menu1_rating, spicy, reviewText, imageName):
        DB.update_rate(restaurant, menuName, menu1_rating, clean_rating)
        ################################################################################################### 
        # 일단은 이렇게 두고, 나중에 reviewList 페이지가 완성되면 reviewList 페이지로 이동하도록 변경하면 좋을것같아요 #
        ###################################################################################################
        return redirect(url_for('view_review', name=restaurant, menuName = menuName))
        
# 메뉴 등록
@application.route("/post_menu_upload", methods=['POST', 'GET'])
def go_post_menu_upload():
    name = request.form['name']
    menuName=request.form['menuName']
    price=request.form['price']
    spicy=request.form['spicy']
    global idx
    
    timenow = str(int(time()))
    image_file_m = request.files['filename']
    image_file_m.save("static/Images/{}".format(image_file_m.filename))
    if DB.insert_menu(name, menuName, price, spicy, image_file_m.filename):
        return redirect(url_for('view_shop_detail', name = name))
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
        return render_template("post_result.html", image_path="static/Images/"+image_file.filename, name = name, 
                               address = address, phone = phone, parking = parking, category = category, link = link, 
                               open_time = open_time, close_time = close_time, noop = noop, breaktime = breaktime)
    else:
        return "Restaurant name already exist!"
    
# 맛집 리스트 가져오기
# 맛집 리스트 화면 페이징
@application.route("/list")
def list_restaurants():
    page = request.args.get("page", 0, type = int)
    category=request.args.get("category","all")
    limit = 3
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    
    if category=="all":
        data = DB.get_restaurants()
    else:
        data = DB.get_restaurants_bycategory(category)

    tot_count = len(data)
    print("category",category,tot_count)
    
    if tot_count<=limit:
        data=dict(list(data.items())[:tot_count])
    else:
        data=dict(list(data.items())[start_idx:end_idx])

    data=dict(sorted(data.items(),key=lambda x:x[1]['name'],reverse=False))
    
    bookmarked = {}
    if 'id' in session:
        user = session['id']
        
        bookmarked = DB.get_bookmarked_by_userID(user)
    
    return render_template(
        "list.html",
        datas = data.items(),
        total = tot_count,
        limit = limit,
        page = page,
        page_count = math.ceil(tot_count/3),
        category=category,
        bookmarked = bookmarked
    )


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    
    
