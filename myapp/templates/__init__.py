'''def match_detail_view(request, match_id):
    #  récupérer les détails d'un match spécifique, US3
    match = get_object_or_404(Match, id=match_id)

    # Préparer le contexte avec les détails du match
    context = {
        'match': match
    }
    # Rendre la page VisualiserUnMatch.html avec les détails du match
    return render(request, 'VisualiserUnMatch.html', context)'''