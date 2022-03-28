from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('customer', views.customer, name='customer'),
    path('admin_view', views.admin_view, name='admin_view'),
    path('contact_us', views.contact_view, name='contact_us'),
    path('new_category', views.new_category, name='new_category'),
    path('new_product', views.new_product, name='new_product'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('user/<str:username>', views.user, name='user'),
    path('deposit/<str:username>', views.deposit, name='deposit'),
    path('withdraw/<str:username>', views.withdraw, name='withdraw'),
    path('checkout/<str:username>', views.checkout, name='checkout'),
    path('delete_category/<str:name>', views.delete_category, name='delete_category'),
    path('user/edit_profile/<str:username>', views.edit_profile, name='edit_profile'),
    path('delete_cart/<str:prod>', views.delete_cart, name='delete_cart'),
    path('approve/<str:serial>', views.approve_purchase, name='approve'),
    path('approve_all', views.approve_all, name='approve_all'),
    path('user/confirm_received/<str:serial>', views.confirm_received, name='confirm_received'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logout, name='logout'),
]
