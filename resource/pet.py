from flask import request
from flask_restful import Resource

from mysql_connection import get_connection
from mysql.connector import Error
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

class PetListResource(Resource) : 
    



    @jwt_required()
    def post(self) :




        # 1. 클라이언트가 보내준 데이터가 있으면
        #    그 데이터를 받아준다.
        data = request.get_json()

        # 1-1 헤더에JWT 토큰이 있으면 토큰 정보를 받아준다
        user_id = get_jwt_identity()



        # 2. 이 레시피정보를 DB에 저장해야한다.
        
        try :
            ### 1. DB에 연결
            connection = get_connection()

            ### 2. 쿼리문 만들기
            # todo : image처리
            query = '''insert into pet
                    (userId,name,classification,species,age,weight,gender)
                    values
                    (%s,%s,%s,%s,%s,%s.%s);'''
            ### 3. 쿼리에 매칭되는 변수 처리 해준다. 튜플로!
            record = ( user_id,data['name'],data['classification'],
                      data['species'],data['age'],data['weight'],data['gender'] )

            ### 4. 커서를 가져온다.
            cursor=connection.cursor()

            ### 5. 쿼리문을 커서로 실행한다.
            cursor.execute(query, record)

            ### 6. 커밋을 해줘야 DB에 완전히 반영된다.
            connection.commit()

            ### 7. 자원 해제
            cursor.close()
            connection.close()

        except Error as e :

            print(e)
            cursor.close()
            connection.close()

            return{"result" : "fail", "error" : str(e)} , 500



        # API를 끝낼때는
        # 클라이언트에 보내줄 정보(json)와 http 상태 코드를
        # 리턴한다.
        return {"result" : "success"} , 200
