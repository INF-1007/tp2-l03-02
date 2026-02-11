#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test local TP2 (ORBIT-X) — pour les étudiants

But :
- Tester toutes les fonctions des exercices 1 à 5
- Afficher le nombre d'erreurs, lesquelles, et des messages clairs
- Inclure des cas particuliers et limites (vide, 0, clés manquantes, etc.)

Utilisation :
    python test_tp2_etudiants.py

⚠️ Ce fichier suppose que vous avez ces fichiers dans le même dossier :
    exercice1.py, exercice2.py, exercice3.py, exercice4.py, exercice5.py
"""

from __future__ import annotations

import math
import traceback

# -----------------------------
# Imports des exercices
# -----------------------------
try:
    import exercice1
except Exception as e:
    exercice1 = None
    _IMPORT_ERR_EX1 = e

try:
    import exercice2
except Exception as e:
    exercice2 = None
    _IMPORT_ERR_EX2 = e

try:
    import exercice3
except Exception as e:
    exercice3 = None
    _IMPORT_ERR_EX3 = e

try:
    import exercice4
except Exception as e:
    exercice4 = None
    _IMPORT_ERR_EX4 = e

try:
    import exercice5
except Exception as e:
    exercice5 = None
    _IMPORT_ERR_EX5 = e


# -----------------------------
# Mini-framework de tests
# -----------------------------

FAILURES: list[str] = []
PASSES: int = 0

# Pour afficher les ENTRÉES (inputs) du test quand ça échoue :
# - run_case enregistre les args/kwargs dans CONTEXT
# - assert_* récupère le meilleur contexte correspondant (préfixe le plus long)
CONTEXT: dict[str, dict] = {}

def _fmt_inputs(args, kwargs) -> str:
    return f"args={repr(args)} kwargs={repr(kwargs)}"

def _best_ctx(test_name: str) -> str:
    best = None
    for k in CONTEXT.keys():
        if test_name.startswith(k) and (best is None or len(k) > len(best)):
            best = k
    if best is None:
        return ""
    ctx = CONTEXT[best]
    return _fmt_inputs(ctx.get("args", ()), ctx.get("kwargs", {}))

def fail(msg: str) -> None:
    FAILURES.append(msg)

def ok(name: str) -> None:
    global PASSES
    PASSES += 1

def fmt(v) -> str:
    return repr(v)

def assert_equal(name: str, got, expected) -> None:
    if got != expected:
        ctx = _best_ctx(name)
        ctx_line = f"\n    Entrées: {ctx}" if ctx else ""
        fail(f"[{name}] Attendu: {fmt(expected)} | Obtenu: {fmt(got)}{ctx_line}")
    else:
        ok(name)

def assert_close(name: str, got: float, expected: float, tol: float = 1e-9) -> None:
    if got is None or expected is None or (isinstance(got, float) and math.isnan(got)):
        ctx = _best_ctx(name)
        ctx_line = f"\n    Entrées: {ctx}" if ctx else ""
        fail(f"[{name}] Valeur invalide: {fmt(got)}{ctx_line}")
        return
    if abs(got - expected) > tol:
        ctx = _best_ctx(name)
        ctx_line = f"\n    Entrées: {ctx}" if ctx else ""
        fail(f"[{name}] Attendu ≈ {expected} | Obtenu: {got} (tol={tol}){ctx_line}")
    else:
        ok(name)

def assert_true(name: str, cond: bool, details: str = "") -> None:
    if not cond:
        ctx = _best_ctx(name)
        ctx_line = f"\n    Entrées: {ctx}" if ctx else ""
        extra = f" | {details}" if details else ""
        fail(f"[{name}] Condition attendue vraie mais fausse{extra}{ctx_line}")
    else:
        ok(name)

def run_case(name: str, fn, *args, **kwargs):
    """
    Exécute une fonction et capture les exceptions.
    Retourne (ok_bool, result)

    🧾 Important : enregistre aussi les entrées (args/kwargs) pour l'affichage
    en cas d'échec dans les assert_*.
    """
    CONTEXT[name] = {"args": args, "kwargs": kwargs}
    try:
        res = fn(*args, **kwargs)
        return True, res
    except Exception as e:
        tb = traceback.format_exc(limit=2)
        ctx = _fmt_inputs(args, kwargs)
        fail(f"[{name}] Exception: {type(e).__name__}: {e}\n    Entrées: {ctx}\n{tb}")
        return False, None


# -----------------------------
# Tests Exercice 1
# -----------------------------

def tests_ex1():
    if exercice1 is None:
        fail(f"[IMPORT exercice1] Impossible d'importer exercice1.py: {_IMPORT_ERR_EX1}")
        return

    ok_run, res = run_case("EX1.analyser_modules/vide", exercice1.analyser_modules, {})
    if ok_run:
        assert_equal("EX1.analyser_modules/vide/module", res.get("module_plus_critique"), None)
        assert_close("EX1.analyser_modules/vide/cout_moyen", float(res.get("cout_moyen", 999)), 0.0)
        assert_close("EX1.analyser_modules/vide/temps_moyen", float(res.get("temps_moyen", 999)), 0.0)

    modules = {
        "A": (100, 10, 10),
        "B": (200, 0, 999),
        "C": (300, 20, 20),
        "D": (400, 5, 9),
    }
    ok_run, res = run_case("EX1.analyser_modules/ratio", exercice1.analyser_modules, modules)
    if ok_run:
        assert_equal("EX1.analyser_modules/ratio/module_plus_critique", res.get("module_plus_critique"), "D")
        assert_close("EX1.analyser_modules/ratio/cout_moyen", float(res.get("cout_moyen", -1)), (100+200+300+400)/4)
        assert_close("EX1.analyser_modules/ratio/temps_moyen", float(res.get("temps_moyen", -1)), (10+0+20+5)/4)

    modules2 = {"Lab": (1,1,1), "Hab": (1,1,1), "Obs": (1,1,1)}
    types = {"Lab": "science", "Obs": "science"}
    ok_run, res = run_case("EX1.regrouper_modules_par_type", exercice1.regrouper_modules_par_type, modules2, types)
    if ok_run:
        assert_equal("EX1.regrouper_modules_par_type/science", res.get("science"), ["Lab", "Obs"])

    modules3 = {"Lab": (10, 1, 1), "Hab": (20, 1, 1)}
    interventions = {"Lab": 3, "Hab": 1, "Ghost": 100}
    ok_run, res = run_case("EX1.calculer_cout_total", exercice1.calculer_cout_total, modules3, interventions)
    if ok_run:
        assert_close("EX1.calculer_cout_total", float(res), 10*3 + 20*1)


# -----------------------------
# Tests Exercice 2
# -----------------------------

def tests_ex2():
    if exercice2 is None:
        fail(f"[IMPORT exercice2] Impossible d'importer exercice2.py: {_IMPORT_ERR_EX2}")
        return

    ok_run, res = run_case("EX2.calculer_priorite/manquants", exercice2.calculer_priorite, {"id": 1})
    if ok_run:
        assert_equal("EX2.calculer_priorite/manquants", res, 0)

    itv = {"urgence": 7, "duree": 3, "critique": True}
    ok_run, res = run_case("EX2.calculer_priorite/formule", exercice2.calculer_priorite, itv)
    if ok_run:
        assert_equal("EX2.calculer_priorite/formule", res, (7*2) + 3 + 10)

    A = {"id": "A", "urgence": 10, "duree": 0, "critique": False}
    B = {"id": "B", "urgence": 10, "duree": 0, "critique": False}
    C = {"id": "C", "urgence": 11, "duree": 0, "critique": False}
    D = {"id": "D", "urgence": 1, "duree": 0, "critique": True}
    lst = [A, B, C, D]
    ok_run, res = run_case("EX2.trier_interventions", exercice2.trier_interventions, lst)
    if ok_run:
        got_ids = [x.get("id") for x in res]
        assert_equal("EX2.trier_interventions/ordre", got_ids, ["C", "A", "B", "D"])
        assert_equal("EX2.trier_interventions/original_intact", [x.get("id") for x in lst], ["A","B","C","D"])

    ok_run, res = run_case("EX2.estimer_temps_interventions/vide", exercice2.estimer_temps_interventions, [])
    if ok_run:
        assert_equal("EX2.estimer_temps_interventions/vide_total", res.get("temps_total"), 0)
        assert_close("EX2.estimer_temps_interventions/vide_moyen", float(res.get("temps_moyen", -1)), 0.0)

    lst2 = [{"duree": 1}, {"duree": 3}, {"duree": 0}]
    ok_run, res = run_case("EX2.estimer_temps_interventions/calcul", exercice2.estimer_temps_interventions, lst2)
    if ok_run:
        assert_equal("EX2.estimer_temps_interventions/calcul_total", res.get("temps_total"), 16)
        assert_close("EX2.estimer_temps_interventions/calcul_moyen", float(res.get("temps_moyen", -1)), 16/3)

    lst3 = [{"id": 1, "urgence": 30}, {"id": 2, "urgence": 31}, {"id": 3}]
    ok_run, res = run_case("EX2.identifier_interventions_urgentes", exercice2.identifier_interventions_urgentes, lst3, 30)
    if ok_run:
        assert_equal("EX2.identifier_interventions_urgentes", res, [2])


# -----------------------------
# Tests Exercice 3
# -----------------------------

def tests_ex3():
    if exercice3 is None:
        fail(f"[IMPORT exercice3] Impossible d'importer exercice3.py: {_IMPORT_ERR_EX3}")
        return

    ressources = {"oxygene": 10}
    besoin = {"oxygene": 5, "eau": 1}
    ok_run, res = run_case("EX3.verifier_ressources/manquante", exercice3.verifier_ressources, ressources, besoin)
    if ok_run:
        peut, manq = res
        assert_equal("EX3.verifier_ressources/manquante/peut", peut, False)
        assert_equal("EX3.verifier_ressources/manquante/list", manq, ["eau"])

    ressources2 = {"oxygene": 10, "eau": 4}
    besoin2 = {"oxygene": 2, "eau": 1}
    ok_run, res = run_case("EX3.mettre_a_jour_ressources", exercice3.mettre_a_jour_ressources, ressources2, besoin2, 3)
    if ok_run:
        assert_equal("EX3.mettre_a_jour_ressources/result_ox", res.get("oxygene"), 10 - 2*3)
        assert_equal("EX3.mettre_a_jour_ressources/result_eau", res.get("eau"), 4 - 1*3)
        assert_equal("EX3.mettre_a_jour_ressources/original_intact", ressources2, {"oxygene": 10, "eau": 4})

    ok_run, res = run_case("EX3.generer_alertes_ressources", exercice3.generer_alertes_ressources, {"oxygene": 49, "eau": 50}, 50)
    if ok_run:
        assert_true("EX3.generer_alertes_ressources/ox_present", "oxygene" in res)
        assert_true("EX3.generer_alertes_ressources/eau_absent", "eau" not in res)
        stock, a_cmd = res["oxygene"]
        assert_equal("EX3.generer_alertes_ressources/ox_stock", stock, 49)
        assert_equal("EX3.generer_alertes_ressources/ox_commande", a_cmd, 200-49)

    ressources3 = {"oxygene": 10}
    consommations = {
        "A": {"oxygene": 2},
        "B": {"oxygene": 0},
    }
    ok_run, res = run_case("EX3.calculer_cycles_possibles", exercice3.calculer_cycles_possibles, ressources3, consommations)
    if ok_run:
        assert_equal("EX3.calculer_cycles_possibles/A", res.get("A"), 5)
        assert_equal("EX3.calculer_cycles_possibles/B", res.get("B"), 0)

    ok_run, res = run_case("EX3.optimiser_reapprovisionnement/budget0", exercice3.optimiser_reapprovisionnement,
                           {"oxygene": 10}, {"oxygene": 100}, 0)
    if ok_run:
        assert_equal("EX3.optimiser_reapprovisionnement/budget0", res, {})

    ressources4 = {"oxygene": 10, "energie": 0}
    besoins_prevus = {"oxygene": 100, "energie": 50}
    ok_run, res = run_case("EX3.optimiser_reapprovisionnement/partiel", exercice3.optimiser_reapprovisionnement,
                           ressources4, besoins_prevus, 100)
    if ok_run:
        assert_equal("EX3.optimiser_reapprovisionnement/partiel", res, {"oxygene": 40})


# -----------------------------
# Tests Exercice 4
# -----------------------------

def tests_ex4():
    if exercice4 is None:
        fail(f"[IMPORT exercice4] Impossible d'importer exercice4.py: {_IMPORT_ERR_EX4}")
        return

    positions = [(0,0,2), (1,1,4)]
    ok_run, salle = run_case("EX4.initialiser_salle", exercice4.initialiser_salle, 3, 4, positions)
    if ok_run:
        assert_equal("EX4.initialiser_salle/dims_rows", len(salle), 3)
        assert_equal("EX4.initialiser_salle/dims_cols", len(salle[0]), 4)
        assert_equal("EX4.initialiser_salle/place_D2", salle[0][0], "D2")
        assert_equal("EX4.initialiser_salle/place_D4", salle[1][1], "D4")
        assert_equal("EX4.initialiser_salle/other_X", salle[2][3], "X")

    base = [["D2","X"],["D4","D2"]]
    ok_run, new = run_case("EX4.affecter_equipement", exercice4.affecter_equipement, base, (1,0))
    if ok_run:
        assert_equal("EX4.affecter_equipement/changed", new[1][0], "U4")
        assert_equal("EX4.affecter_equipement/original_intact", base[1][0], "D4")
        ok_run2, new2 = run_case("EX4.affecter_equipement/X", exercice4.affecter_equipement, base, (0,1))
        if ok_run2:
            assert_equal("EX4.affecter_equipement/X_unchanged", new2[0][1], "X")

    ok_run, s = run_case("EX4.calculer_score/trop_petit", exercice4.calculer_score_equipement, (2,2), 2, 3, 5)
    if ok_run:
        assert_equal("EX4.calculer_score/trop_petit", s, -1)

    ok_run, s = run_case("EX4.calculer_score/bonus", exercice4.calculer_score_equipement, (1,0), 2, 2, 5)
    if ok_run:
        assert_equal("EX4.calculer_score/bonus", s, 125)

    salle = [["D2","U4"],["M4","X"]]
    ok_run, res = run_case("EX4.trouver_meilleur/none", exercice4.trouver_meilleur_equipement, salle, 3)
    if ok_run:
        assert_equal("EX4.trouver_meilleur/none", res, None)

    salle = [
        ["D4", "X", "D4"],
        ["X",  "X", "X"],
    ]
    ok_run, res = run_case("EX4.trouver_meilleur/egalite", exercice4.trouver_meilleur_equipement, salle, 3)
    if ok_run:
        assert_equal("EX4.trouver_meilleur/egalite", res, ((0,0), 4))

    ok_run, r = run_case("EX4.rapport/empty", exercice4.generer_rapport_etat, [["X"]])
    if ok_run:
        assert_close("EX4.rapport/empty_taux", float(r.get("taux_indisponibilite", -1)), 0.0)

    salle = [
        ["D2","U2","M4"],
        ["X","D4","U4"]
    ]
    ok_run, r = run_case("EX4.rapport/calcul", exercice4.generer_rapport_etat, salle)
    if ok_run:
        assert_equal("EX4.rapport/dispo2", r.get("disponibles_2"), 1)
        assert_equal("EX4.rapport/util2", r.get("utilises_2"), 1)
        assert_equal("EX4.rapport/maint4", r.get("maintenance_4"), 1)
        assert_equal("EX4.rapport/dispo4", r.get("disponibles_4"), 1)
        assert_equal("EX4.rapport/util4", r.get("utilises_4"), 1)
        assert_close("EX4.rapport/taux", float(r.get("taux_indisponibilite", -1)), 3/5)


# -----------------------------
# Tests Exercice 5
# -----------------------------

def tests_ex5():
    if exercice5 is None:
        fail(f"[IMPORT exercice5] Impossible d'importer exercice5.py: {_IMPORT_ERR_EX5}")
        return

    # -----------------------------
    # Données communes
    # -----------------------------
    mots_cles = {
        "stable": 2,
        "optimal": 3,
        "nominal": 1,
        "ok": 1,
        "erreur": -2,
        "panne": -3,
        "defaillant": -3,
        "retard": -1,
        "surchauffe": -2,
        "fuite": -3,
    }
    mots_cles_negatifs = {
        "erreur": -2,
        "panne": -3,
        "defaillant": -3,
        "retard": -1,
        "surchauffe": -2,
        "fuite": -3,
    }

    # =========================================================
    # 1) analyser_rapport — casse + ponctuation + occurrences
    # =========================================================
    # Score attendu :
    # score = 5
    # + ok(1) + stable*2 occurrences (2*2=4) + defaillant(-3) + panne*2 (-6)
    # => 5 + 1 + 4 - 3 - 6 = 1 (borné [0,10] => 1)
    texte = "OK. Stable, stable! Defaillant: panne panne."
    ok_run, res = run_case("EX5.analyser_rapport/ponct", exercice5.analyser_rapport, texte, mots_cles)
    if ok_run:
        score, mots = res
        assert_equal("EX5.analyser_rapport/ponct_score", score, 1)
        assert_true(
            "EX5.analyser_rapport/ponct_mots",
            set(mots) == {"ok", "stable", "defaillant", "panne"},
            details=f"mots_obtenus={mots}"
        )

    # =========================================================
    # 2) analyser_rapport — texte vide / aucun mot-clé
    # =========================================================
    # Si aucun mot-clé détecté => score reste 5 (borné => 5), mots=[]
    ok_run, res = run_case("EX5.analyser_rapport/vide", exercice5.analyser_rapport, "", mots_cles)
    if ok_run:
        score, mots = res
        assert_equal("EX5.analyser_rapport/vide_score", score, 5)
        assert_equal("EX5.analyser_rapport/vide_mots", mots, [])

    ok_run, res = run_case("EX5.analyser_rapport/aucun_mot", exercice5.analyser_rapport, "bonjour tout le monde", mots_cles)
    if ok_run:
        score, mots = res
        assert_equal("EX5.analyser_rapport/aucun_mot_score", score, 5)
        assert_equal("EX5.analyser_rapport/aucun_mot_mots", mots, [])

    # =========================================================
    # 3) analyser_rapport — bornage haut / bornage bas
    # =========================================================
    texte = "optimal optimal optimal stable stable ok ok ok nominal nominal"
    ok_run, res = run_case("EX5.analyser_rapport/bornage_haut", exercice5.analyser_rapport, texte, mots_cles)
    if ok_run:
        score, _ = res
        assert_equal("EX5.analyser_rapport/bornage_haut_score", score, 10)

    texte = "panne panne panne defaillant fuite surchauffe erreur erreur"
    ok_run, res = run_case("EX5.analyser_rapport/bornage_bas", exercice5.analyser_rapport, texte, mots_cles)
    if ok_run:
        score, _ = res
        assert_equal("EX5.analyser_rapport/bornage_bas_score", score, 0)

    # =========================================================
    # 4) categoriser_rapports — seuils exacts + liste vide
    # =========================================================
    # stable => 7 (positif), nominal => 6 (neutre), panne erreur => 0 (négatif)
    rapports = ["stable", "nominal", "panne erreur"]
    ok_run, cats = run_case("EX5.categoriser_rapports/seuils", exercice5.categoriser_rapports, rapports, mots_cles)
    if ok_run:
        assert_equal("EX5.categoriser/nb_pos", len(cats.get("positifs", [])), 1)
        assert_equal("EX5.categoriser/nb_neu", len(cats.get("neutres", [])), 1)
        assert_equal("EX5.categoriser/nb_neg", len(cats.get("negatifs", [])), 1)

    ok_run, cats = run_case("EX5.categoriser_rapports/vide", exercice5.categoriser_rapports, [], mots_cles)
    if ok_run:
        assert_equal("EX5.categoriser/vide_pos", cats.get("positifs"), [])
        assert_equal("EX5.categoriser/vide_neu", cats.get("neutres"), [])
        assert_equal("EX5.categoriser/vide_neg", cats.get("negatifs"), [])

    # =========================================================
    # 5) identifier_problemes — accepte tuples ET textes + cas vide
    # =========================================================
    neg_tuples = [
        ("panne panne erreur", 0),
        ("retard erreur", 2),
    ]
    ok_run, prob = run_case("EX5.identifier_problemes/tuples", exercice5.identifier_problemes, neg_tuples, mots_cles_negatifs)
    if ok_run:
        assert_equal("EX5.problemes/tuples_panne", prob.get("panne"), 2)
        assert_equal("EX5.problemes/tuples_erreur", prob.get("erreur"), 2)
        assert_equal("EX5.problemes/tuples_retard", prob.get("retard"), 1)

    neg_textes = ["panne fuite", "erreur erreur"]
    ok_run, prob = run_case("EX5.identifier_problemes/textes", exercice5.identifier_problemes, neg_textes, mots_cles_negatifs)
    if ok_run:
        assert_equal("EX5.problemes/textes_panne", prob.get("panne"), 1)
        assert_equal("EX5.problemes/textes_fuite", prob.get("fuite"), 1)
        assert_equal("EX5.problemes/textes_erreur", prob.get("erreur"), 2)

    ok_run, prob = run_case("EX5.identifier_problemes/vide", exercice5.identifier_problemes, [], mots_cles_negatifs)
    if ok_run:
        # On attend toutes les clés à 0 (si l'étudiant a bien initialisé)
        assert_true("EX5.problemes/vide_keys", all(k in prob for k in mots_cles_negatifs.keys()), details=f"keys={list(prob.keys())}")
        assert_true("EX5.problemes/vide_zeros", all(prob[k] == 0 for k in mots_cles_negatifs.keys()), details=f"prob={prob}")

    # =========================================================
    # 6) generer_rapport_global — cas limite : aucun score
    # =========================================================
    cats_vides = {"positifs": [], "neutres": [], "negatifs": []}
    problemes_vides = {k: 0 for k in mots_cles_negatifs.keys()}
    ok_run, rep = run_case("EX5.generer_rapport_global/vide", exercice5.generer_rapport_global, cats_vides, problemes_vides)
    if ok_run:
        assert_equal("EX5.rapport_global/vide_nb_pos", rep.get("nb_positifs"), 0)
        assert_equal("EX5.rapport_global/vide_nb_neu", rep.get("nb_neutres"), 0)
        assert_equal("EX5.rapport_global/vide_nb_neg", rep.get("nb_negatifs"), 0)
        assert_close("EX5.rapport_global/vide_moy", float(rep.get("score_moyen", -1)), 0.0)
        assert_equal("EX5.rapport_global/vide_top", rep.get("top_problemes"), [])

    # =========================================================
    # 7) generer_rapport_global — moyenne + top_problemes (avec égalités)
    # =========================================================
    cats = {
        "positifs": [("stable", 7)],
        "neutres": [("nominal", 6)],
        "negatifs": [("panne erreur", 0), ("retard erreur", 2)],
    }
    problemes = {"panne": 2, "erreur": 2, "retard": 1, "fuite": 0, "surchauffe": 0, "defaillant": 0}
    ok_run, rep = run_case("EX5.generer_rapport_global/calcul", exercice5.generer_rapport_global, cats, problemes)
    if ok_run:
        assert_equal("EX5.rapport_global/nb_pos", rep.get("nb_positifs"), 1)
        assert_equal("EX5.rapport_global/nb_neu", rep.get("nb_neutres"), 1)
        assert_equal("EX5.rapport_global/nb_neg", rep.get("nb_negatifs"), 2)
        assert_close("EX5.rapport_global/moy", float(rep.get("score_moyen", -1)), (7+6+0+2)/4)

        top = rep.get("top_problemes", [])
        # Exigences minimales robustes (ordre peut varier en cas d'égalité)
        assert_true("EX5.rapport_global/top_len<=3", isinstance(top, list) and len(top) <= 3, details=f"top={top}")
        # Si top contient 3 éléments, on veut que 'retard' apparaisse (car c'est le 3e plus fréquent)
        assert_true("EX5.rapport_global/top_retard_if_3", (len(top) < 3) or ("retard" in top), details=f"top={top}")

    # =========================================================
    # 8) calculer_tendance — cas limites + pair/impair
    # =========================================================
    ok_run, t = run_case("EX5.tendance/vide", exercice5.calculer_tendance, [])
    if ok_run:
        assert_equal("EX5.tendance/vide_res", t, "stable")

    ok_run, t = run_case("EX5.tendance/un_seul", exercice5.calculer_tendance, [5])
    if ok_run:
        assert_equal("EX5.tendance/un_seul_res", t, "stable")

    # pair
    ok_run, t = run_case("EX5.tendance/amelio_pair", exercice5.calculer_tendance, [2,2, 7,7])
    if ok_run:
        assert_equal("EX5.tendance/amelio_pair_res", t, "amelioration")

    ok_run, t = run_case("EX5.tendance/degrad_pair", exercice5.calculer_tendance, [8,8, 3,3])
    if ok_run:
        assert_equal("EX5.tendance/degrad_pair_res", t, "degradation")

    # impair : n=5 => mid=2 -> first=[..2], second=[..3]
    ok_run, t = run_case("EX5.tendance/amelio_impair", exercice5.calculer_tendance, [1,1, 5,5,5])
    if ok_run:
        assert_equal("EX5.tendance/amelio_impair_res", t, "amelioration")

    ok_run, t = run_case("EX5.tendance/stable", exercice5.calculer_tendance, [5,5, 5,5])
    if ok_run:
        assert_equal("EX5.tendance/stable_res", t, "stable")

def main():
    print("=== TP2 — Tests étudiants ===\n")

    tests_ex1()
    tests_ex2()
    tests_ex3()
    tests_ex4()
    tests_ex5()

    total = PASSES + len(FAILURES)
    print("\n" + "=" * 60)
    print(f"Tests exécutés : {total}")
    print(f"✅ Réussites   : {PASSES}")
    print(f"❌ Échecs      : {len(FAILURES)}")
    print("=" * 60)

    if FAILURES:
        print("\nDétails des échecs :")
        for i, msg in enumerate(FAILURES, 1):
            print(f"\n{i}) {msg}")
        print("\n👉 Corriger les fonctions jusqu’à obtenir 0 échec.")
    else:
        print("\n🎉 Tout est bon ! (0 échec)")

if __name__ == "__main__":
    main()