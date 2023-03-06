<<<<<<< HEAD
=======

>>>>>>> BMW
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

<<<<<<< HEAD
class HotelSearchResource(Resource) :
    # 검색한 호텔 리스트 가져오기
    def get(self) :
        keyword = request.args.get('keyword')
=======
# 호텔 검색 리스트
class HotelSearchResource(Resource) :
    @jwt_required(optional=True)
    def get(self,keyword) :

>>>>>>> BMW
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

<<<<<<< HEAD
            query = '''select f.hotelId, h.title, h.imgUrl, ifnull(avg(r.rating),0) as avg, ifnull(count(r.hotelId),0) as cnt,
                    if(f.userId is null, 0, 1) as 'favorite'
                    from yh_project_db.hotel h
                    left join yh_project_db.follows f on f.hotelId = h.id and f.userId= 2
                    left join yh_project_db.reviews r on r.hotelId = h.id
                    where h.title like '%''' + keyword + '''%' or h.addr like '%''' + keyword + '''%'
                    group by h.id
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, )

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['avg'] = float(row['avg'])
=======
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
>>>>>>> BMW
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

<<<<<<< HEAD
            return {"error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200
    
    # 검색어 저장
    def put(self) :
        keyword = request.args.get('keyword')
=======
            return {'error' : str(e) } , 500

            


        return {'result' : 'success' , 'hotel' : resultList}









# 호텔 상세정보
class HotelInfoResource(Resource) :

    @jwt_required(optional=True)
    def get(self, hotelId) :

>>>>>>> BMW

        try :
            connection = get_connection()

<<<<<<< HEAD
            query = '''insert into yh_project_db.keyword(keyword)
                    values(%s);'''

            record = (keyword, )

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
    
class HotelSearchRankResource(Resource) :
    # 검색어 순위 가져오기
    def get(self) :
        today = request.args.get('today')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select keyword, ifnull(count(keyword),0) as cnt, createdAt
                    from yh_project_db.keyword
                    group by keyword having createdAt like '%''' + today + '''%'
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, )

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

=======
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



>>>>>>> BMW
        except Error as e :
            print(e)
            cursor.close()
            connection.close()

<<<<<<< HEAD
            return {"error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200
=======
            return {'error' : str(e) } , 500

            


        return {'result' : 'success' , 'hotel' : resultList[0]}






>>>>>>> BMW
