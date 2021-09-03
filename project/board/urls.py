from django.urls import path
from .views import PostsView, PostDetailView, PostCreate, PostDelete, PostUpdate, BoardLogoutView, BoardLoginView, profile, signup, accept, delete_reaction, verify, reactions_to_my_posts, my_reactions, PostWRDetailView

urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('<int:pk>', PostDetailView.as_view(), name='post'),
    path('login/', BoardLoginView.as_view(), name='login'),
    path('logout/', BoardLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('verification/', verify, name='verification'),
    path('add/', PostCreate.as_view(), name='add'),
    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('accounts/profile/', profile, name='profile'),
    path('reactions/', reactions_to_my_posts, name='reactions'),
    path('my_reactions/', my_reactions, name='my_reactions'),
    path('postwr/<int:pk>', PostWRDetailView.as_view(), name='postwr'),
    path('deleter/<int:pk>', delete_reaction, name='deleter'),
    path('accept/<int:pk>', accept, name='accept'),

]
