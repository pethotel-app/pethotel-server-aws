
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

# 호텔 검색 리스트
class HotelSearchResource(Resource) :
    @jwt_required(optional=True)
    def get(self,keyword) :

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query ='''select * from hotel
            where addr LIKE %s
            LIMIT '''+offset+''','''+limit+''';'''

            record = (f"%{keyword}%",)

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)
            resultList = cursor.fetchall()

            if len(resultList) == 0 :
                 return {"error": "검색 결과가 없습니다."}, 404

            i = 0
            for row in resultList :
                resultList[i]['longtitude'] = float(row['longtitude'])
                resultList[i]['latitude'] = float(row['latitude'])
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {'error' : str(e) } , 500

            


        return {'result' : 'success' , 'hotel' : resultList}









# 호텔 상세정보
class HotelInfoResource(Resource) :

    @jwt_required(optional=True)
    def get(self, hotelId) :


        try :
            connection = get_connection()

            query = '''select h.id,title,addr,longtitude,latitude,tel,naverUrl, small,medium,large
                    from hotel h
                    left join price p
                    on h.id = p.hotelId
                    where h.id = %s;'''


            record = (hotelId,)

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            resultList = cursor.fetchall()
            
            if resultList[0]['id'] is None :
                return{'error' : '잘못된 호텔 아이디 입니다.'} , 400

            i = 0
            for row in resultList :
                resultList[i]['longtitude'] = float(row['longtitude'])
                resultList[i]['latitude'] = float(row['latitude'])
                i = i + 1


            cursor.close()
            connection.close()



        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {'error' : str(e) } , 500

            


        return {'result' : 'success' , 'hotel' : resultList[0]}






