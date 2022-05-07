from django.urls import path
from .import views
urlpatterns = [

    path('',views.home,name='home'),
    path('register',views.registerPage,name="register"),
    path('login',views.loginpage,name="login"),
    path('productslist',views.productslist,name='productslist'),
    path('dashboard',views.dashboard,name="admindashboard"),
    path('dashboard/publishedreview',views.publishedreview,name="publishedreview"),
    path('dashboard/underreview',views.underreview,name="underreview"),
    path('dashboard/rejectedreview',views.rejectedreview,name="rejectedreview"),
    path('/products/<product_id>',views.purchaseproduct,name="buy"),
    path('reviews/<product_id>',views.writereviews,name="reviews"),
    path(r'^reviews/<int:product_id>/<str:status>$',views.viewreviews,name="viewreviews"),
    path('logout',views.logout,name='logout')
]