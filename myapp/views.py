from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Match, Bet, Team
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from SuperBowl.utils import convert_email_to_username
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BetForm, MatchForm, TeamForm, PlayerForm
from django.contrib.auth.forms import UserCreationForm
from .forms import ExtendedUserCreationForm
from django.db.models import Sum, Case, When, DecimalField
from django.db.models.functions import TruncMonth


def create_account_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ExtendedUserCreationForm()
    return render(request, 'create_account.html', {'form': form})




def home_view(request):
    # Fetch all upcoming matches
    upcoming_matches = Match.objects.filter(match_time__gte=datetime.now())

    # Fetch all matches for categorization
    all_matches = Match.objects.all()

    # Example of categorizing matches (you can modify the logic as needed)
    matches_1_and_2 = all_matches[:2]  # First two matches
    matches_3_and_4 = all_matches[2:4]# Next two matches
    matches_5_and_6 = all_matches[4:6]
    matches_7_and_8 = all_matches[6:8]
    matches_9_and_10 = all_matches[8:10]
    # Continue for other sets of matches as needed

    # Pass these sets to the template
    context = {
        'upcoming_matches': upcoming_matches,
        'matches_1_and_2': matches_1_and_2,
        'matches_3_and_4': matches_3_and_4,
        'matches_5_and_6': matches_5_and_6,
        'matches_7_and_8': matches_7_and_8,
        'matches_9_and_10': matches_9_and_10,
        # Continue for other sets
    }
    return render(request, 'index.html', context)


def all_matches_view(request):
    # US2
    # Récupérer tous les matchs depuis la base de données
    now = timezone.now()
    all_matches = Match.objects.all()

    past_matches = Match.objects.filter(match_time__lt=now, status='Terminé')
    current_matches = Match.objects.filter(match_time__lte=now, match_time__gte=now - timezone.timedelta(hours=2),
                                           status='En cours')
    upcoming_matches = Match.objects.filter(match_time__gt=now, status='À venir')

    # Vous pouvez trier les matchs en fonction de leur statut si vous avez un champ 'status' dans votre modèle

    # past_matches = all_matches.filter(status='Passed')
    # current_matches = all_matches.filter(status='Current')
    # upcoming_matches = all_matches.filter(status='Upcoming')

    # Préparer le contexte avec les matchs
    context = {
        'past_matches': past_matches,
        'current_matches': current_matches,
        'upcoming_matches': upcoming_matches
    }
    # Rendre la page viewAllMatches.html avec les matchs
    return render(request, 'viewAllMatches.html', context)



def match_detail_view(request, match_id):
    #  récupérer les détails d'un match spécifique, US3
    match = get_object_or_404(Match, id=match_id)

    # Préparer le contexte avec les détails du match
    context = {
        'match': match
    }
    # Rendre la page VisualiserUnMatch.html avec les détails du match
    return render(request, 'VisualiserUnMatch.html', context)


@login_required
def place_bet_view(request, match_id):
    # placer un pari sur un match  US4
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.match = match
            bet.user = request.user
            bet.save()
            return redirect('some_view')
    else:
        form = BetForm()

    context = {
        'form': form,
        'match': match
    }

    return render(request, 'PlaceBet.html', context)
    '''return render(request, 'PlaceBet.html', {'match_id': match_id},context)'''

@login_required
def betting_page_view(request):
    if request.method == 'POST':
        match_id = request.POST.get('matchSelect')
        team_id = request.POST.get('teamSelect')
        bet_amount = request.POST.get('betAmount')

        selected_match = Match.objects.get(id=match_id)
        selected_team = Team.objects.get(id=team_id)

        new_bet = Bet(
            user=request.user,
            match=selected_match,
            chosen_team=selected_team,
            amount=bet_amount
        )
        new_bet.full_clean()  # Validate the bet before saving
        new_bet.save()

        # Redirect to place bet view with the match id
        return redirect('myapp:place_bet', match_id=match_id)

    matches = Match.objects.all()
    teams = Team.objects.all()
    return render(request, 'Parier.html', {'matches': matches, 'teams': teams})


@login_required
def finalize_bet_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        # Assuming the form sends match_id, chosen_team_id, and bet_amount
        chosen_team_id = request.POST.get('chosen_team_id')
        bet_amount = request.POST.get('bet_amount')

        # Create and save the bet
        new_bet = Bet(
            user=request.user,
            match=match,
            chosen_team_id=chosen_team_id,
            amount=bet_amount
        )
        new_bet.full_clean()  # This will raise a ValidationError if the data is incorrect
        new_bet.save()

        # Redirect to a confirmation page or any other page
        return redirect('some_success_page')

    # If it's not POST request, redirect to betting page or show an error
    return redirect('betting_page')


'''def create_account_view(request):
    # créer un compte utilisateur US7
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # You can log the user in here if you want
            # then redirect to 'home' or any other page
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_account.html', {'form': form})'''


def password_reset_view(request):
    # réinitialiser le mot de passe US8
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        try:
            # Assurez-vous que l'email et le nom correspondent à un utilisateur
            user = User.objects.get(email=email, first_name=name.split()[0], last_name=name.split()[-1])
            # Implémentez la logique pour envoyer l'email de réinitialisation
            send_mail(
                'Réinitialisation de votre mot de passe',
                'Voici le lien pour réinitialiser votre mot de passe.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, 'password-reset-confirm.html')
        except User.DoesNotExist:
            # Gérer l'erreur si l'utilisateur n'est pas trouvé
            pass

    return render(request, 'password-reset.html')


@login_required
def user_dashboard_view(request):
    user_bets = Bet.objects.filter(user=request.user)

    # Group and sum bets by month
    monthly_data = user_bets.annotate(month=TruncMonth('date_placed')).values('month').annotate(
        total_amount=Sum(Case(
            When(is_winner=True, then='amount'),
            default=0,
            output_field=DecimalField()
        ))
    ).order_by('month')

    # Formatting for JavaScript
    labels = [data['month'].strftime("%b %Y") for data in monthly_data]
    data = [float(data['total_amount']) for data in monthly_data]  # Convert to float

    context = {
        'user_bets': user_bets,
        'labels': labels,
        'data': data
    }

    return render(request, 'EspaceUtilisateur.html', context)
'''def user_dashboard_view(request):
    # afficher le tableau de bord de l'utilisateur US9
        user_bets = Bet.objects.filter(user=request.user)

        # Préparer les données pour le graphique (par exemple, les gains/mois)
        # Vous pouvez adapter cela en fonction des données exactes que vous avez
        labels = ["Jan", "Fév", "Mar", "Avr", "Mai"]
        data = [120, 190, 300, 500, 700]  # Exemple de données

        context = {
            'user_bets': user_bets,
            'labels': labels,
            'data': data
        }

        return render(request, 'EspaceUtilisateur.html', context)'''


@login_required
def betting_history_view(request):
    # afficher l'historique des paris de l'utilisateur US10
        # Récupérer les paris de l'utilisateur
    user_bets = Bet.objects.filter(user=request.user).order_by('-date_placed')
    context = {'user_bets': user_bets}
    return render(request, 'HistoriqueMises.html', context)


def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teams = Team.objects.all()
    matches = Match.objects.all()
    # Other objects you want to manage can be included here

    context = {
        'teams': teams,
        'matches': matches,
        # Include other context variables here
    }
    return render(request, 'EspaceAdministrateur.html', context)

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def edit_team_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            # Redirect to a success page, e.g., the admin dashboard
            return redirect('admin_dashboard')
    else:
        form = TeamForm(instance=team)
    return render(request, 'edit_team.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_team_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
        # Redirect after deletion, e.g., to the admin dashboard
        return redirect('admin_dashboard')
    return render(request, 'delete_team_confirm.html', {'team': team})


def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def create_teams_and_players_view(request):
    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        player_form = PlayerForm(request.POST, request.FILES)
        if 'teamName' in request.POST and team_form.is_valid():
            team_form.save()
        elif 'playerName' in request.POST and player_form.is_valid() and 'teamSelect' in request.POST:
            player_form.save()

    else:
        team_form = TeamForm()
        player_form = PlayerForm()

    teams = Team.objects.all()  # Pour peupler le dropdown des équipes
    return render(request, 'CréationsEquipesEtJoueurs.html', {'team_form': team_form, 'player_form': player_form,'teams': teams})


def schedule_teams_view(request):
    # planifier les matchs des équipes US13
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici
            form.save()
            return redirect('quelque_part')  # Redirigez vers une autre page si nécessaire
    else:
        form = MatchForm()

    return render(request, 'AffectationEquipes.html', {'form': form})


'''def login_view(request):
    # la connexion des utilisateurs
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = convert_email_to_username(email)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Adresse e-mail ou mot de passe incorrect")

        return render(request, 'LogIn.html')'''



