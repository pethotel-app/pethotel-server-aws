








































































































































































































from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import Config
<<<<<<< HEAD

from resource.favorite import FavoriteListResource, FavoriteResource
from resource.hotel import HotelSearchRankResource, HotelSearchResource

from resource.pet import PetListResource, PetResource
from resource.reservation import ReservationResource
from resource.review import ReviewListResource

=======
from resource.benefit import CouponSearchResource, CouponUseResource, PointAddResource, PointSearchResource
from resource.hotel import HotelInfoResource, HotelSearchResource
>>>>>>> BMW
from resource.user import UserChangePasswordResource, UserIdSearchResource, UserImageResource, UserInfoResource, UserLoginResource, UserLogoutResource, UserPasswordSearchResource, UserRegisterResource, jwt_blacklist

# branch test
# branch test
# branch test
# branch test
# branch test
app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) : 
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')
<<<<<<< HEAD

api.add_resource(UserIdSearchResource, '/user/id/search')
api.add_resource(UserPasswordSearchResource, '/user/password/search')
api.add_resource(UserChangePasswordResource, '/user/change/password')

=======
api.add_resource(UserIdSearchResource, '/user/IdSearch')
api.add_resource(UserPasswordSearchResource, '/user/PasswordSearch')
api.add_resource(UserChangePasswordResource, '/user/ChangePassword')
>>>>>>> BMW
api.add_resource(UserInfoResource, '/user/info')
api.add_resource(UserImageResource, '/user/profile')
api.add_resource(PointSearchResource, '/benefit/point')
api.add_resource(PointAddResource, '/benefit/addPoint')
api.add_resource(CouponSearchResource,'/benefit/coupon')
api.add_resource(CouponUseResource, '/benefit/coupon/<int:couponId>')
api.add_resource(HotelInfoResource, '/hotel/<int:hotelId>')
api.add_resource(HotelSearchResource, '/hotel/searchList/<string:keyword>')



api.add_resource(FavoriteResource, '/favorite/<int:hotelId>')
api.add_resource(FavoriteListResource, '/favorite')

api.add_resource(HotelSearchResource, '/hotel/search')
api.add_resource(HotelSearchRankResource, '/hotel/search/rank')

# 펫
api.add_resource(PetListResource, '/pets/')
api.add_resource(PetResource, '/pets/<int:petId>')

# 리뷰
api.add_resource(ReviewListResource, '/review/<int:hotelId>')

# 예약
api.add_resource(ReservationResource, '/reservation')


if __name__ == '__main__' :
    app.run()