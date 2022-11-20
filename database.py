import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        
   # 리뷰 등록
    def insert_review(self, time_r, rating, mood, menuName, menu1_rating, spicy, img_path_r):
        review_info ={
            "time": time_r, 
            "rating": rating, 
            "mood": mood,
            "menuName": menuName,
            "menu1_rating": menu1_rating,
            "spicy": spicy,
            "img_path": img_path_r
        }
        self.db.child("review").child(menuName).set(review_info)
        print(time_r, rating, mood, menuName, menu1_rating, spicy, img_path_r)
        return True
    
    # 대표 메뉴 등록
    def insert_menu(self, menuName, price, spicy, img_path_m):
        menu_info ={
            "menuName": menuName,
            "price": price,
            "spicy": spicy,
            "img_path": img_path_m
        }
        self.db.child("menu").child(menuName).set(menu_info)
        print(menuName, price, spicy, img_path_m)
        return True
        
        
    # 맛집 등록
    def insert_restaurant(self, name, address, phone, parking, category, link, open_time, close_time, noop, breaktime, img_path):
        restaurant_info ={
            "name": name,
            "address": address,
            "phone": phone,
            "parking": parking,
            "category": category,
            "link": link,
            "open_time": open_time,
            "close_time": close_time,
            "noop": noop,
            "breaktime": breaktime,
            "img_path": img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").child(name).set(restaurant_info)
            print(name, address, phone, parking, category, link, open_time, close_time, noop, breaktime, img_path)
            return True
        else:
            return False
        
    # 맛집 이름 중복 검사 
    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            if res.key() == name:
                return False
        return True