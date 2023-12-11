from django.urls import path
from . import views

app_name = 'myapp'  # Namespace for app

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('miser/', views.betting_page_view, name='betting_page'),
    path('viewAllMatches/', views.all_matches_view, name='view_all_matches'),
    path('match/<int:match_id>/', views.match_detail_view, name='match_detail'),
    path('placeBet/<int:match_id>/', views.place_bet_view, name='place_bet'),


    path('userDashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('bettingHistory/', views.betting_history_view, name='betting_history'),
    path('adminDashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('createTeamsAndPlayers/', views.create_teams_and_players_view, name='create_teams_and_players'),
    path('scheduleTeams/', views.schedule_teams_view, name='schedule_teams'),

    path('editTeam/<int:team_id>/', views.edit_team_view, name='edit_team'),
    path('deleteTeam/<int:team_id>/', views.delete_team_view, name='delete_team'),
    path('finalize_bet/<int:match_id>/', views.finalize_bet_view, name='finalize_bet'),
    path('create_account/', views.create_account_view, name='CreateMyAccount'),
    path('updateBet/<int:bet_id>/', views.update_bet_view, name='update_bet'),
    path('deleteBet/<int:bet_id>/', views.delete_bet_view, name='delete_bet'),
    path('parier/', views.parier_view, name='parier'),
    path('place_bets/', views.place_bets_view, name='place_bets'),
    path('confirm_bets/', views.confirm_bets_view, name='confirm_bets'),

]

'''path('login/', views.login_view, name='login'),
    path('passwordReset/', views.password_reset_view, name='password_reset'),'''


