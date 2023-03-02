from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import Config
from resource.benefit import CouponSearchResource, CouponUseResource, PointAddResource, PointSearchResource
from resource.hotel import HotelInfoResource, HotelSearchResource
from resource.user import UserChangePasswordResource, UserIdSearchResource, UserImageResource, UserInfoResource, UserLoginResource, UserLogoutResource, UserPasswordSearchResource, UserRegisterResource, jwt_blacklist


app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) : 
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

# 유저
api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')
api.add_resource(UserIdSearchResource, '/user/IdSearch')
api.add_resource(UserPasswordSearchResource, '/user/PasswordSearch')
api.add_resource(UserChangePasswordResource, '/user/ChangePassword')
api.add_resource(UserInfoResource, '/user/info')
api.add_resource(UserImageResource, '/user/profile')
api.add_resource(PointSearchResource, '/benefit/point')
api.add_resource(PointAddResource, '/benefit/addPoint')
api.add_resource(CouponSearchResource,'/benefit/coupon')
api.add_resource(CouponUseResource, '/benefit/coupon/<int:couponId>')
api.add_resource(HotelInfoResource, '/hotel/<int:hotelId>')
api.add_resource(HotelSearchResource, '/hotel/searchList/<string:keyword>')


if __name__ == '__main__' :
    app.run()