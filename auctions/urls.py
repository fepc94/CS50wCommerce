from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>/", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>/", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>/", views.remove_watchlist, name="remove_watchlist"),
    path("add_comment/<int:listing_id>/", views.add_comment, name='add_comment'),
    path("place_bid/<int:listing_id>/", views.set_bid, name='set_bid'),
    path("close_listing/<int:listing_id>/", views.close_listing, name='close_listing'),
    path("categories", views.categories, name='categories'),
    path("category/<str:cat>", views.list_by_category, name='list_by_category'),
]
