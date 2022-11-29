import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # 리뷰를 작성할 때마다 해당 메뉴 별점, 매장 청결도 갱신
    def update_rate(self, restaurant, menu, rating, clean):
        info = self.db.child("restaurant").child(restaurant).child("menu").child(menu).get()
        value = info.val()
        
        # 메뉴 별점 갱신
        rate_update = {}
        
        count = value['review_count']
        new_rate = (value['rate']*count + float(rating)) / (count+1)
        
        rate_update['rate'] = new_rate
        rate_update['review_count'] = count+1
        
        self.db.child("restaurant").child(restaurant).child("menu").child(menu).update(rate_update)
        
        
        #매장 청결도 갱신
        info = self.db.child("restaurant").child(restaurant).get()
        value = info.val()
        
        clean_update = {}
        
        count = value['review_count']
        new_clean = (value['clean_rate'] * count + float(clean)) / (count+1)
        
        clean_update['clean_rate'] = new_clean
        clean_update['review_count'] = count+1
        
        self.db.child("restaurant").child(restaurant).update(clean_update)
        
        return True
    
   # 리뷰 등록
    def insert_review(self, restaurant, user, time_r, rating, menuName, menu1_rating, spicy, reviewText, img_path_r):
        review_info ={
            "time": time_r, 
            "menu1_rating": menu1_rating,
            "spicy": spicy,
            "reviewText": reviewText,
            "img_path": img_path_r,
        }
        ####################################################
        ## 이거 set 대신 push로 바꿔서 키 따로 안만들어도 잘 돌아갈거에요!
        ####################################################
        self.db.child("restaurant").child(restaurant).child("menu").child(menuName).child("review").push(review_info)
        print(time_r, rating, menuName, menu1_rating, spicy, reviewText, img_path_r)
        return True
    
    # 대표 메뉴 등록
    def insert_menu(self, name, menuName, price, spicy, img_path_m):
        menu_info ={
            "menuName": menuName,
            "price": price,
            "spicy": spicy,
            "img_path": img_path_m,
            "review_count": 0,
            "rate": 0,
        }
        if self.menu_duplicate_check(name, menuName):
            self.db.child("restaurant").child(name).child("menu").child(menuName).set(menu_info)
            print(name, menuName, price, spicy, img_path_m)
            return True
        else:
            return False
        
        
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
            "img_path": img_path,
            "review_count": 0,
            "clean_rate" : 0
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
        
        if restaurants.val() is None:
            return True
        
        for res in restaurants.each():
            if res.key() == name:
                return False
        return True
    
    def menu_duplicate_check(self, name, menuName):
        menus = self.db.child("restaurant").child(name).child("menu").get()
        if menus.val() is None:
            return True
        
        for menu in menus.each():
            value = menu.val()
            
            if value['menuName'] == menuName: 
                return False
        return True 
    
    ########맛집 이름으로 restaurant 테이블에서 정보 가져오기
    def get_shop_byname(self,name):
        restaurants = self.db.child("restaurant").get()
        target_value=""
        
        for res in restaurants.each():
            value = res.val()
                
            if value['name']==None:
                return None
            if value['name']==name:
                target_value=value
        return target_value
    
    
    ###별점 평균 계산
    def get_avgrate_byname(self,name):
        menus=self.db.child("restaurant").child(name).child("menu").get()
        if menus.val() is None:
            return 0
        
        rate = 0.0
        count = 0
        
        for menu in menus.each():
            value = menu.val()
            
            if value['rate'] is not 0:
                rate += float(value['rate'])
                count += 1
        
        if count == 0 :
            return 0
        
        else:
            return round(rate/count, 2)
    
    ######식당이름으로 review 접근하기 --> 메뉴 이름으로 메뉴마다의 리뷰를 보게 하는 것이 더 좋을 것 같다...?
    def get_review_byname(self,name,menuName):
        menus=self.db.child("restaurant").child(name).child("menu").get()
        target_value=""
            
        for res in menus.each():
            value=res.val()
                
            if value['menuName']==menuName:
                target_value=value
        return target_value
    
    # 모든 식당 데이터 반환(메인화면에서 필요)
    def get_all_data(self):
        data=self.db.child("restaurant").get()
            
        return data.val()
    
    # 맛집 등록 테이블에서 데이터 가져오기
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
    

        