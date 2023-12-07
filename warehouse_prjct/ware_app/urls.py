from django.urls import path
from .import views

urlpatterns = [

    path('', views.home, name='home'),
    path('signup_page', views.signup_page, name='signup_page'),
    path('signup', views.signup, name='signup'),

    path('signup_del_page', views.signup_del_page, name='signup_del_page'),
    path('signup_del', views.signup_del, name='signup_del'),

    path('admin_home', views.admin_home, name='admin_home'),
    path('customer_home', views.customer_home, name='customer_home'),
    path('delivery_home', views.delivery_home, name='delivery_home'),

    path('signin_page', views.signin_page, name='signin_page'),
    path('signin', views.signin, name='signin'),

    path('manage_registrations', views.manage_registrations,
         name='manage_registrations'),
    path('approve_customer/<int:customer_id>',
         views.approve_customer, name='approve_customer'),
    path('approve_delivery/<int:delivery_id>',
         views.approve_delivery, name='approve_delivery'),
    path('delete/customer/<int:customer_id>/',
         views.delete_customer, name='delete_customer'),
    path('delete/delivery/<int:delivery_id>/',
         views.delete_delivery, name='delete_delivery'),

    path('view_notifications', views.view_notifications,
         name='view_notifications'),
    path('delete_customer_notification', views.delete_customer_notification,
         name='delete_customer_notification'),
    path('delete_delivery_notification', views.delete_delivery_notification,
         name='delete_delivery_notification'),

    path('add_product/', views.add_product, name='add_product'),
    path('show_product', views.show_product, name='show_product'),
    path('edit_product_page/<int:pk>',
         views.edit_product_page, name='edit_product_page'),
    path('edit_product/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('view_products', views.view_products, name='view_products'),


    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('cart_delete/<int:pk>', views.cart_delete, name='cart_delete'),
    path('update_cart_item/<int:item_id>/',
         views.update_cart_item, name='update_cart_item'),

    path('checkout', views.checkout, name='checkout'),
    path('checkout/item/<int:item_id>/',
         views.checkout_item, name='checkout_item'),

    path('order-success/', views.order_success, name='order_success'),
    path('view_all_orders', views.view_all_orders, name='view_all_orders'),
    path('track_order', views.track_order, name='track_order'),

    path('order_tracking', views.order_tracking, name='order_tracking'),
    path('view_all_orders_delivery', views.view_all_orders_delivery,
         name='view_all_orders_delivery'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),

    path('update_client_delivery_status/<int:order_id>/',
         views.update_client_delivery_status, name='update_client_delivery_status'),

    path('order_tracking_admin', views.order_tracking_admin,
         name='order_tracking_admin'),



    path('customer_details_page', views.customer_details_page,
         name='customer_details_page'),
    path('edit_customer_page', views.edit_customer_page, name='edit_customer_page'),
    path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),


    path('customer/reset_password/', views.customer_reset_password,
         name='customer_reset_password'),
    path('delivery/reset_password/', views.delivery_reset_password,
         name='delivery_reset_password'),


    path('edit_customer_page_admin/<int:pk>', views.edit_customer_page_admin,
         name='edit_customer_page_admin'),


    path('customer_details_admin', views.customer_details_admin,
         name='customer_details_admin'),
    path('edit_customer_admin/<int:pk>',
         views.edit_customer_admin, name='edit_customer_admin'),
    path('delete_customer/<int:pk>',
         views.delete_customer, name='delete_customer'),


    path('order/<int:order_id>/assign-delivery/',
         views.edit_order_assign_delivery, name='assign_delivery'),


    path('delivery_details_page', views.delivery_details_page,
         name='delivery_details_page'),
    path('edit_delivery_page', views.edit_delivery_page,
         name='edit_delivery_page'),
    path('edit_delivery_user/<int:pk>', views.edit_delivery_user,
         name='edit_delivery_user'),

    path('delivery_details_admin', views.delivery_details_admin,
         name='delivery_details_admin'),
    path('delete_delivery/<int:pk>', views.delete_delivery,
         name='delete_delivery'),
    path('edit_delivery_page_admin/<int:pk>', views.edit_delivery_page_admin,
         name='edit_delivery_page_admin'),
    path('edit_delivery_admin/<int:pk>', views.edit_delivery_admin,
         name='edit_delivery_admin'),

    path('logout_admin', views.logout_admin, name='logout_admin'),
]
