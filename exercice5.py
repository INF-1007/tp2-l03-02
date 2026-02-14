"""
TP2 – Exercice 5 : Analyse de journaux d’incidents (Centre ORBIT-X)

Contexte :
Les ingénieurs reçoivent des rapports texte (logs) décrivant l’état des systèmes.
On veut analyser ces textes pour :
- calculer un score global (0 à 10)
- classer les rapports en catégories
- détecter les problèmes récurrents
- générer un rapport global + une tendance

Mots-clés :
On fournit un dictionnaire {mot_cle: score} avec des scores positifs ou négatifs.
Exemple :
mots_cles = {
    'stable': 2,
    'optimal': 3,
    'erreur': -2,
    'defaillant': -3
}

Règles générales :
- L’analyse est INSENSIBLE à la casse (majuscules/minuscules)
- On cherche des mots présents dans le texte (occurrences par mots)
- Un mot-clé peut apparaître plusieurs fois : chaque occurrence compte
- Le score final est borné entre 0 et 10
"""

# -------------------------------------------------------------
# 1) Analyser un rapport
# -------------------------------------------------------------

def analyser_rapport(texte, mots_cles):
    """
    Calcule le score d’un rapport et extrait les mots-clés détectés.

    Étapes attendues :
    1) Mettre le texte en minuscules
    2) Compter les occurrences de chaque mot-clé
       (approche simple autorisée : split() + comparaison de mots)
    3) score = 5 + somme(occurrences * score_mot)
    4) borner score entre 0 et 10
    5) retourner (score, liste_mots_trouves_sans_doublons)

    Args:
        texte (str)
        mots_cles (dict): {mot: score_int}

    Returns:
        tuple: (score_int, mots_trouves_list)
    """
    score = 5
    mots_trouves = []

    # TODO 1 : normaliser texte (minuscules)
    # TODO 2 : découper en mots. Attention aussi à enlever la ponctuation basique aux extrémités (utiliser la fonction strip())S.
    # TODO 3 : pour chaque mot-clé :
    #    - mettre à jour le score
    #    - si occurrences > 0 : ajouter le mot à mots_trouves (sans doublons)
    # TODO 4 : borner score entre 0 et 10 (min/max)
    # TODO 5 : retourner (score, mots_trouves)

    text_min = texte.lower()
    
    for m in text_min:
        if not ord(m) > 96 and ord(m) < 123 and ord(m) != 32:
            text_min = text_min.replace(m, "")  

    
    text_min = text_min.split()
    for mot in text_min:
        if mot in mots_cles:
            if not mot in mots_trouves:
                mots_trouves.append(mot)
                score += mots_cles[mot]
            else:
                score += mots_cles[mot]
    if score > 10:
        score = 10
    elif score < 0:
        score = 0
    
    
    return score, mots_trouves


# -------------------------------------------------------------
# 2) Catégoriser une liste de rapports
# -------------------------------------------------------------

def categoriser_rapports(rapports, mots_cles):
    """
    Classe les rapports en 3 catégories selon leur score :

    - 'positifs' : score >= 7
    - 'neutres'  : 4 <= score <= 6
    - 'negatifs' : score <= 3

    Args:
        rapports (list): liste de chaînes
        mots_cles (dict)

    Returns:
        dict: {
            'positifs': [(texte, score), ...],
            'neutres':  [(texte, score), ...],
            'negatifs': [(texte, score), ...]
        }
    """
    categories = {'positifs': [], 'neutres': [], 'negatifs': []}

    # TODO :
    # Pour chaque texte :
    #   - faire une analyse du rapport pour en tirer le score
    #   - mettre à jour "categories"

    for p in rapports:
        phrase_m = p.lower()
        score_p = 5

        for L in phrase_m:
            if not ord(L) > 96 and ord(L) < 123 and ord(L) != 32:
                phrase_m = phrase_m.replace(L, "")
        phrase_m = phrase_m.split()

        for m in phrase_m:
            if m in mots_cles:
                score_p += mots_cles[m]
        
        if score_p >= 7:
            categories['positifs'].append((p, score_p))

        elif score_p <= 3:
            categories['negatifs'].append((p, score_p))
        
        else:
            categories['neutres'].append((p, score_p))

    
    return categories


# -------------------------------------------------------------
# 3) Identifier les problèmes récurrents dans les rapports négatifs
# -------------------------------------------------------------

def identifier_problemes(rapports_negatifs, mots_cles_negatifs):
    """
    À partir des rapports négatifs, compter combien de fois chaque mot-clé négatif apparaît.

    Args:
        rapports_negatifs (list): liste de tuples (texte, score) OU liste de textes
        mots_cles_negatifs (dict): {mot_negatif: score_negatif}

    Returns:
        dict: {mot_negatif: nombre_occurrences_total}
    """
    problemes = {}

    # TODO 1 : initialiser problemes avec 0 pour chaque mot négatif
    # TODO 2 : parcourir les rapports négatifs :
    #   - si l’élément est un tuple, récupérer texte = element[0]
    #   - analyser le texte (minuscules + split)
    #   - compter les occurrences de chaque mot_negatif
    #   - incrémenter problemes[mot]

    phrase_m = []

    for mot in mots_cles_negatifs:
        problemes[mot] = 0
    
    for p in rapports_negatifs:
        print(p)
        if type(p) == tuple:
            
            t = p[0]
            for L in p[0]:
                if not ord(L) > 96 and ord(L) < 123 and ord(L) != 32:
                    t = t.replace(L, "")
            t = t.lower()
            phrase_m.append(t.split())
        else:
            

            for L in p:
                if not ord(L) > 96 and ord(L) < 123 and ord(L) != 32:
                    p = p.replace(L, "")
            p = p.lower()
            phrase_m.append(p.split())
      
    

    for i in range(len(phrase_m)):
        for m in phrase_m[i]:

            if m in mots_cles_negatifs:
                problemes[m] += 1
        
    print(phrase_m)
    return problemes


# -------------------------------------------------------------
# 4) Générer un rapport global
# -------------------------------------------------------------

def generer_rapport_global(categories, problemes):
    """
    Génère un résumé global.

    Contenu attendu :
    - nb_positifs, nb_neutres, nb_negatifs
    - score_moyen (moyenne de tous les scores)
    - top_problemes : liste des 3 mots négatifs les plus fréquents (du plus fréquent au moins fréquent)

    Args:
        categories (dict) : résultat de categoriser_rapports
        problemes (dict)  : résultat de identifier_problemes

    Returns:
        dict
    """
    rapport = {
        'nb_positifs': 0,
        'nb_neutres': 0,
        'nb_negatifs': 0,
        'score_moyen': 0.0,
        'top_problemes': []
    }

    # TODO 1 : récupérer tous les scores et calculer la moyenne (gérer le cas avec 0 rapports)
    # TODO 2 : trouver les 3 problèmes les plus fréquents sans utiliser sorted(), un tri simple type “sélection des max” est suffisant.)
    
    rapport['nb_positifs'] = len(categories['positifs'])
    rapport['nb_neutres'] = len(categories['neutres'])
    rapport['nb_negatifs'] = len(categories['negatifs'])

    score_t = 0
    nombre_p = 0
    for c in categories:
        for p in categories[c]:
            score_t += p[1]
            nombre_p += 1

    if nombre_p != 0:
        rapport['score_moyen'] += score_t / nombre_p

    else:
        rapport['score_moyen'] = 0
        return rapport
   
    problemes_2 = problemes.copy()

    
    if len(problemes_2) <= 3:
        x = len(problemes_2)
    else:
        x = 3
    while x != 0:
        score_temporaire = None
        m_temporaire = None

        for m in problemes_2:

            if score_temporaire != None:
                
                if score_temporaire < problemes_2[m]:
                    score_temporaire = problemes_2[m]
                    m_temporaire = m

            else:
                score_temporaire = problemes_2[m]
                m_temporaire = m

        rapport['top_problemes'].append(m_temporaire)
        score_temporaire = problemes_2.pop(m_temporaire)
        x -= 1
    return rapport


# -------------------------------------------------------------
# 5) Calculer une tendance à partir d’un historique
# -------------------------------------------------------------

def calculer_tendance(historique_scores):
    """
    Calcule une tendance à partir d’une liste de scores (dans le temps).

    Règle simple :
    - Si moyenne de la 2e moitié > moyenne de la 1re moitié : 'amelioration'
    - Si moyenne de la 2e moitié < moyenne de la 1re moitié : 'degradation'
    - Sinon : 'stable'

    Cas particuliers :
    - si historique vide : 'stable'
    - si un seul élément : 'stable'

    Args:
        historique_scores (list): ex [4,5,6,7,8]

    Returns:
        str: 'amelioration' | 'degradation' | 'stable'
    """

    # TODO :
    # - Gérer les cas vides / 1 élément
    # - Couper en deux moitiés
    # - Comparer les moyennes
    
    if len(historique_scores) <= 0:
        return 'stable'
    moitier_1 = historique_scores[0: len(historique_scores) // 2 ]
    moitier_2 = historique_scores[len(historique_scores) // 2 : len(historique_scores)]

    moyen_1 = 0
    moyen_2 = 0
    for i in range(len(moitier_1)):
        moyen_1 += moitier_1[i]
        moyen_2 += moitier_2[i]
    if len(moitier_1) > 0 and len(moitier_2) > 0:
        moyen_1 /= len(moitier_1)
        moyen_2 /= len(moitier_2)
    else:
        moyen_1 = 0
        moyen_2 = 0

    if moyen_1 < moyen_2:
        return 'amelioration'
    elif moyen_2 <moyen_1:
        return 'degradation'
    else:
        return 'stable'
# -------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------

if __name__ == "__main__":
    mots_cles = {
        'stable': 2,
        'optimal': 3,
        'nominal': 1,
        'ok': 1,
        'erreur': -2,
        'panne': -3,
        'defaillant': -3,
        'retard': -1,
        'surchauffe': -2,
        'fuite': -3
    }

    mots_cles_negatifs = {
        'erreur': -2,
        'panne': -3,
        'defaillant': -3,
        'retard': -1,
        'surchauffe': -2,
        'fuite': -3
    }

    # Grande liste de rapports (volontairement variée)
    rapports = [
        "Système stable et nominal. Tout est OK.",
        "Température stable, fonctionnement optimal, état OK.",
        "Erreur de communication détectée. Retard sur la séquence.",
        "Panne capteur pression. Système defaillant.",
        "Surchauffe moteur. Erreur erreur. Risque panne.",
        "Nominal, mais léger retard sur l'alignement.",
        "Fuite détectée dans le circuit secondaire. Panne possible.",
        "OK. Stable.",
        "Defaillant: panne panne panne sur module X.",
        "Rapport: fonctionnement optimal et stable, nominal.",
        "Surchauffe et fuite. Erreur critique.",
        "Tout nominal, tout ok.",
        "Retard retard retard. Erreur de synchronisation.",
        "Panne électrique. Système defaillant. Surchauffe.",
        "Stable, mais une erreur isolée.",
    ]

    print("=== Test analyse_rapport (exemples) ===")
    for i in [0, 2, 4, 8, 10]:
        s, mots = analyser_rapport(rapports[i], mots_cles)
        print(f"Rapport {i} -> score={s}, mots={mots}")

    print("\n=== Catégorisation ===")
    categories = categoriser_rapports(rapports, mots_cles)
    print("Nb positifs :", len(categories['positifs']))
    print("Nb neutres  :", len(categories['neutres']))
    print("Nb negatifs :", len(categories['negatifs']))

    print("\n=== Problèmes récurrents (sur négatifs) ===")
    problemes = identifier_problemes(categories['negatifs'], mots_cles_negatifs)
    print(problemes)

    print("\n=== Rapport global ===")
    global_ = generer_rapport_global(categories, problemes)
    print(global_)

    print("\n=== Tendance (historique) ===")
    historique = [3, 4, 4, 5, 6, 6, 7, 7, 8, 8]
    print("Historique :", historique)
    print("Tendance :", calculer_tendance(historique))

