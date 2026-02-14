"""
TP2 – Exercice 1 : Analyse des modules de la station spatiale ORBIT-X

Objectif :
Analyser les modules de la station afin d'extraire des statistiques utiles
pour la planification de la maintenance.

Un module est représenté par :
    nom_module : (cout_maintenance, temps_intervention, criticite)

Exemple :
modules = {
    'Laboratoire': (120, 15, 8),
    'Habitat': (200, 10, 9),
    'Observatoire': (150, 20, 6)
}
"""

# -------------------------------------------------------------------
# 1) Analyse des modules
# -------------------------------------------------------------------


def analyser_modules(modules):
    
    """
    Analyse les modules de la station.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}

    Returns:
        dict contenant :
            - 'module_plus_critique' : str ou None
            - 'cout_moyen' : float
            - 'temps_moyen' : float
    """

    # TODO 1 : Gérer le cas où le dictionnaire est vide
    # Dans ce cas, retourner stats tel quel

    # TODO 2 : Parcourir les modules
    # - Identifier le module ayant le meilleur ratio criticite / temps_intervention
    #   ⚠️ Ignorer les modules avec temps_intervention == 0
    #   ⚠️ En cas d’égalité, conserver le premier module rencontré

    # TODO 3 : Calculer les moyennes
    # - cout_moyen = somme_couts / nombre_modules
    # - temps_moyen = somme_temps / nombre_modules

    meilleur_ratio = 0
    cout_moyen = 0
    temps_moyen = 0
    meilleur_ratio_str = None
    nb_modules = 0

    for i in modules:
        nb_modules += 1
        cout_moyen += modules[i][0]
        temps_moyen += modules[i][1]
        
        if modules[i][1] == 0:
            continue
        else:
            if meilleur_ratio < (modules[i][0] / modules[i][2]):
                meilleur_ratio = (modules[i][0] / modules[i][2])
                meilleur_ratio_str = i

        
        
        
    if nb_modules != 0:
        temps_moyen = temps_moyen / nb_modules
        cout_moyen = cout_moyen / nb_modules
    else:
        temps_moyen = 0
        cout_moyen = 0
    stats = {
        'module_plus_critique': meilleur_ratio_str,
        'cout_moyen': cout_moyen,
        'temps_moyen': temps_moyen
    }
    return stats

# -------------------------------------------------------------------
# 2) Regroupement des modules par type
# -------------------------------------------------------------------


def regrouper_modules_par_type(modules, types):
    """
    Regroupe les modules par type.

    Args:
        modules (dict): dictionnaire des modules
        types (dict): {nom_module: type}

    Returns:
        dict: {type: [liste des modules]}
    """

    modules_par_type = {}

    # TODO :
    # Pour chaque module :
    #   - Vérifier s’il existe dans le dictionnaire types
    #   - Ajouter le module dans la liste correspondant à son type
    #   - Créer la liste si elle n’existe pas encore
    # ⚠️ Ignorer silencieusement les modules sans type

    for module in modules:
        if module in types:
            if types[module] != None:
                if not types[module] in modules_par_type:

                    modules_par_type[types[module]] = [module]
                else:
                    modules_par_type[types[module]].append(module)

    return modules_par_type

# -------------------------------------------------------------------
# 3) Calcul du cout total
# -------------------------------------------------------------------


def calculer_cout_total(modules, interventions):

    """
    Calcule le coût total de maintenance prévu.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}
        interventions (dict): {nom_module: nombre_interventions}

    Returns:
        float: coût total
    """

    cout_total = 0.0

    # TODO :
    # Pour chaque module dans interventions :
    #   - Vérifier qu’il existe dans modules
    #   - Ajouter à cout_total le cout total de maintenance du module étant donné le nombre d'interventions
    # ⚠️ Ignorer les modules absents de modules

    for m in interventions:
        if m in modules:
            cout_total += interventions[m] * modules[m][0]

    return cout_total

# -------------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------------


if __name__ == "__main__":
    modules_test = {
        'Laboratoire': (120, 15, 8),
        'Habitat': (200, 10, 9),
        'Observatoire': (150, 20, 6)
    }

    types_test = {
        'Laboratoire': 'science',
        'Habitat': 'vie',
        'Observatoire': 'science'
    }

    interventions_test = {
        'Laboratoire': 2,
        'Habitat': 1
    }

    print(analyser_modules(modules_test))
    print(regrouper_modules_par_type(modules_test, types_test))
    print(calculer_cout_total(modules_test, interventions_test))
