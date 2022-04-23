from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),
    path("listing/<int:listing_id>/add_comment/",
         views.add_comment, name="comment"),
    path("listing/<int:listing_id>/bid/", views.create_bid, name="bid"),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<str:category>", views.category_view, name="category"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("create/", views.create_listing, name="create")
]
