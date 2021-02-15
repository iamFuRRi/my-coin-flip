from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet, BalanceViewSet, GameViewSet, RoundViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'balances', BalanceViewSet)
router.register(r'games', GameViewSet)
router.register(r'rounds', RoundViewSet)

urlpatterns = [
    # REST API ENDPOINTS
    path('api/', include(router.urls)),

    # GAME ENDPOINTS
    path('users/<int:pk>/games/', GameViewSet.as_view({'get': 'games'})),
    path('users/<int:pk>/games/<int:pk_game>/', GameViewSet.as_view({'get': 'get_game'})),
    path('users/<int:pk>/games/<int:pk_game>/rounds/', RoundViewSet.as_view({'get': 'rounds'})),
    path('users/<int:pk>/games/<int:pk_game>/rounds/<int:pk_round>/', RoundViewSet.as_view({'get': 'get_round'})),

    # GET USER BALANCE
    path('users/<int:pk>/balance/', BalanceViewSet.as_view({'get': 'get_balance'}), name='balance'),

    # START NEW GAME
    path('users/<int:pk>/games/start_game/', GameViewSet.as_view({'post': 'start_game'})),

    # START NEW ROUND
    path('users/<int:pk>/games/<int:pk_game>/start_round/', RoundViewSet.as_view({'post': 'start_round'})),

    # API TOKEN AUTH
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth-token/', views.obtain_auth_token),
]
