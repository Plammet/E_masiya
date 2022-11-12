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

@application.route("/menu_upload")
def go_menu_upload():
    return render_template("menu_upload.html")

@application.route("/post_result", methods=['POST', 'GET'])
def go_post_result():
    name = request.form['shop_name']
    address = request.form['shop_addr']
    phone = request.form['shop_phone']
    parking = request.form['parking']
    category = request.form['category']
    link  = request.form['link']
    image_file = request.files["menuImage"]
    image_file.save("static/image/{}".format(image_file.src))
    return render_template("post_result.html", link=link, parking=parking, category=category, name=name, phone=phone, address=address)
    
    
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
    