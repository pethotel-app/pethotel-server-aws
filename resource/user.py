from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password

# 회원가입
class UserRegisterResource(Resource) :
    def post(self) :
        # { "name": "김이름,
        # "phone": "010-1234-5678",
        # "email": "abcd@naver.com""
        # "password": "1234"}

        data = request.get_json()

        try :
            validate_email( data["email"] )
        except EmailNotValidError as e :
            print(str(e))
            return {'error' : str(e)}, 400

        if len(data["password"]) < 4 or len(data["password"]) > 20 :
            return {'error' : '비밀번호 길이 확인'}, 400

        hashed_password = hash_password(data["password"])

        try :
            connection = get_connection()
            query = '''insert into user
                    (name, phone, email, password)
                    values
                    (%s, %s, %s, %s);'''
            
            record = (data["name"], data["phone"], data["email"], hashed_password)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            # 회원가입한 유저의 id값 가져오기
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500

        access_token = create_access_token(user_id)
        return {"result" : "success", "access_token" : access_token}, 200

# 로그인
class UserLoginResource(Resource) :
    def post(self) :
        # {"email": "abcd@naver.com",
        # "password": "1234"}

        data = request.get_json()

        try :
            connection = get_connection()

            query = '''select *
                    from user
                    where email = %s ;'''

            record = (data["email"], )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            if len(result_list) == 0 :
                return {"error" : "회원가입한 사람이 아닙니다"} , 400

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500


        check = check_password( data['password'], result_list[0]['password'] )

        if check == False :
            return {"error" : "비밀번호가 일치하지 않습니다"} , 400

        access_token = create_access_token( result_list[0]['id'] )

        return {"result" : "success", "access_token" : access_token}, 200

# 로그아웃
jwt_blacklist = set()
class UserLogoutResource(Resource) :
    @jwt_required()
    def post(self) :
        
        jti = get_jwt()['jti']

        jwt_blacklist.add(jti)

        return {'result' : 'success'}, 200

# 회원탈퇴
class UserInfoDeleteResource(Resource) :
    @jwt_required()
    def delete(self) :
        jti = get_jwt()['jti']
        jwt_blacklist.add(jti)

        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''delete from user
                    where id = %s ;'''

            record = (user_id, )

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success"}, 200

# 회원정보 조회
class UserInfoResource(Resource) :
    @jwt_required()
    def get(self) :
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''select name, phone, email
                    from user
                    where id = %s ;'''

            record = ( user_id, )

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"result" : "fail", "error" : str(e)}, 500

        if len(result_list) == 0 :
            return {"error" : "잘못된 유저 아이디"}, 400

        return {"result" : "success", "user" : result_list[0]}, 200

# 아이디찾기
class UserIdSearchResource(Resource) :
    def post(self) :
        # { "name": "김이름,
        # "phone": "010-1234-5678"}

        data = request.get_json()

        try :
            connection = get_connection()

            query = '''select email
                    from user
                    where name = %s and phone = %s ; '''

            record = (data["name"], data["phone"])

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success", "email" : result_list}, 200

# 비밀번호찾기
class UserPasswordSearchResource(Resource) :
    def post(self) :
        pass