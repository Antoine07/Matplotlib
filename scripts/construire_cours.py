"""Génère les deux blocs et leurs carnets modèles, sans modifier les copies personnelles."""
from pathlib import Path
import csv
import html
import json
from contenu_cours import BLOCKS, MONTHLY

R = Path(__file__).resolve().parents[1]

def write(path, text):
    p=R/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

def code(s):
    return '<div class="code-block"><span class="code-label">Python · sandbox-notebook</span><pre tabindex="0"><code>'+html.escape(s)+'</code></pre></div>'

def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def details(title,body):return '<details><summary>'+title+'</summary>'+body+'</details>'

def figure(name,alt,caption='Figure obtenue avec les données et le code du cours.'):
    return f'<figure class="plot-figure"><img src="../assets/{name}.png" alt="{html.escape(alt,quote=True)}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

def head(title,prefix='..',quiz=False):
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f8f2"><title>{title} — Le labo Matplotlib</title><link rel="stylesheet" href="{prefix}/assets/site.css"><link rel="stylesheet" href="{prefix}/assets/tableau.css"><link rel="stylesheet" href="{prefix}/assets/matplotlib.css"><script src="{prefix}/assets/cours.js" defer></script>{f'<script src="{prefix}/assets/qcm.js" defer></script>' if quiz else ''}</head><body><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><a class="brand" href="{prefix}/index.html"><span class="brand-icon" aria-hidden="true">mp.</span> Le labo Matplotlib</a><a class="back-link" href="{prefix}/index.html">← Le parcours</a></header>'''

def foot(prefix='..'):return f'<footer class="site-footer"><span>Le labo Matplotlib / NEXA</span><a href="{prefix}/index.html">Comprendre, puis pratiquer.</a></footer></body></html>'

def page(block,sections,kind='cours'):
    title=block['title'] if kind=='cours' else ('Correction collective' if kind=='correction' else 'QCM de fin de bloc')
    nav=''.join(f'<a href="#{id}"><span>{i:02}</span>{label}</a>' for i,(id,label,_) in enumerate(sections,1))
    body=''.join(f'<section class="course-section" id="{id}"><p class="eyebrow">Bloc {block["n"]:02} <span>/</span> {label}</p>{content}</section>' for id,label,content in sections)
    hero=block['hero'] if kind=='cours' else title
    return head(title,quiz=kind=='qcm')+f'<main class="course-main" id="contenu"><div class="course-intro"><p class="eyebrow">Matplotlib · Bloc {block["n"]:02}</p><h1>{hero}</h1><p>{block["intro"]}</p><div class="meta"><span>Bases déjà acquises</span><span>Exemple → exercice → correction collective</span><span>QCM avec feedback</span></div></div><div class="course-layout"><nav class="course-nav" aria-label="Étapes du bloc"><p class="eyebrow">Votre parcours</p>{nav}<a class="download-link" href="../data/sandbox-notebook.zip" download>↓ Sandbox apprenant</a><a href="../supports/{block["slug"]}.html">Le cours du bloc</a></nav><div class="course-content">{body}</div></div></main>'+foot()

GALLERY=[('01_categories','Comparer : les catégories','Barres : comparer des ventes entre catégories. Informatique est en tête.'),('01_courbe','Suivre : les ventes quotidiennes','Courbe : suivre les ventes du 1er au 30 janvier dans l’ordre des dates.'),('01_histogramme','Répartir : les montants des lignes','Histogramme : compter les lignes de vente dans six intervalles de montants.')]

def exercise(block,lesson,i):
    e=lesson['exercise']
    body=f'<article class="exercise" id="exercice-{i}"><p class="eyebrow">Petit exercice {i:02}</p><h3>{e["title"]}</h3><p><strong>Objectif :</strong> {e["objective"]} <strong>Prérequis :</strong> {e["prereq"]}</p><p>{e["prompt"]}</p>'
    if e['starter'].strip()!='# À vous de jouer.':body+=code(e['starter'])
    body+=f'<p><strong>Livrable :</strong> {e["deliverable"]} <strong>Critères de réussite :</strong> {e["success"]}</p><p class="small">Travaillez sur les données fournies, sans saisir les résultats attendus à la place du calcul.</p>'
    body+=''.join(details(f'Indice {j}',f'<p>{h}</p>') for j,h in enumerate(e['hints'],1))
    body+='</article>'
    return body

INTRO1='''<h2>Introduction</h2><h3>Objectif</h3><p>Choisir un graphique adapté, préparer ses données et produire une figure lisible et vérifiable. Vous avez déjà exécuté du Python et tracé un graphique simple ; nous réactivons les gestes utiles.</p><h3>Résumé général</h3><p>On observe un exemple, on fait une petite modification, puis on corrige ensemble. Le QCM de fin de bloc donne une explication après chaque réponse.</p><div class="journey"><span>Observer</span><span>Essayer</span><span>Corriger ensemble</span><span>Expliquer</span></div><p>Dans la sandbox, ouvrez <code>notebooks/01_comprendre_graphiques.ipynb</code> et faites une copie à votre nom. Les cellules s’exécutent avec Maj + Entrée. Les chemins <code>/workspace/data</code> et <code>/workspace/resultats</code> sont ceux de Docker.</p><div class="actions"><a class="button primary" href="../data/sandbox-notebook.zip" download>Télécharger la sandbox ↓</a><a class="button" href="../data/commandes.csv" download>CSV des commandes ↓</a></div><details><summary>Ouvrir ou mettre à jour Jupyter</summary><p>Depuis le dossier sandbox-notebook, lancez <code>docker compose up --build -d</code>, puis consultez <code>docker compose logs notebook</code> pour le jeton. Ouvrez <a href="http://localhost:8890/lab">http://localhost:8890/lab</a>. Seaborn est inclus dans les dépendances : reconstruisez l’image si vous utilisiez la première version.</p></details>'''
INTRO2='''<h2>Introduction</h2><h3>Objectif</h3><p>Calculer un indicateur, choisir sa représentation et l’interpréter avec la bonne référence. Nous réutilisons Figure, Axes, les titres et les exports du bloc 1.</p><h3>Résumé général</h3><p>La part du total a été vue au bloc 1. Nous distinguons maintenant variation mensuelle, évolution depuis janvier, somme cumulée, moyenne mobile et marge rapportée au chiffre d’affaires.</p><div class="notice"><strong>Un second scénario fictif.</strong><p>Les six mois ci-dessous ne proviennent pas du CSV de janvier : son total et sa période sont différents et il n’a pas de colonne profit. Ce petit tableau indépendant sert à vérifier les calculs à la main, dans le même projet de carnet commercial.</p></div><p>Ouvrez <code>notebooks/02_indicateurs.ipynb</code>. Une ligne représente un mois ; le calendrier est complet et toutes les ventes sont strictement positives.</p>'''

SUMMARY_ROWS=[['Janvier','10 000','—','0 %','10 000'],['Février','12 000','+20 %','+20 %','22 000'],['Mars','9 000','−25 %','−10 %','31 000'],['Avril','15 000','+66,67 %','+50 %','46 000'],['Mai','18 000','+20 %','+80 %','64 000'],['Juin','16 500','−8,33 %','+65 %','80 500']]

PROJECT='''<h2>Le carnet visuel de la boutique.</h2><p><strong>Contexte et utilisateurs :</strong> une responsable commerciale veut des graphiques pour comparer les ventes et suivre des indicateurs. Chaque figure doit répondre à une question et pouvoir être reproduite.</p><p><strong>Organisation :</strong> les données alimentent pandas ; les Series et DataFrames préparent les mesures ; Matplotlib produit les Figures ; les notebooks conservent les raisonnements ; <code>resultats</code> accueille les PNG.</p>'''+table(['Jalon','Production vérifiable','Erreur à repérer'],[['Bloc 1','Barres par région et parts du total ; unités et dénominateur explicites.','Confondre lignes et commandes ou désassocier noms et montants.'],['Bloc 2','Courbes et barres des indicateurs ; commentaire sur juin et sur le semestre.','Confondre variation, cumul et moyenne des taux.']])+'''<p><strong>Livrables :</strong> vos deux carnets complétés, les figures des exercices et vos interprétations. <strong>Validation :</strong> mêmes résultats après redémarrage du noyau, références nommées et limites reconnues.</p><p><strong>Cas d’usage professionnel :</strong> une équipe commerciale peut partager ces images dans un rapport. Le contrôle des mesures rend les comparaisons vérifiables ; la figure ne démontre pas les causes d’une hausse ou d’une baisse.</p><p><strong>Extension facultative :</strong> refaire la comparaison des catégories sur une seule région, en précisant le filtre et le nouveau total.</p>'''

BRIDGE='''<h2>Retrouver la logique dans Power BI.</h2><p>Ce repère est facultatif : aucun exercice Power BI n’est requis pour terminer les blocs Matplotlib. On transfère le raisonnement, pas une traduction automatique de chaque ligne Python.</p>'''+table(['Question / pandas','Repère Power BI'],[['Somme : sum()','SUM, avec le contexte de filtre du modèle.'],['Variation : pct_change()','Comparer la période courante à la précédente sur un calendrier défini.'],['Évolution depuis l’origine','Choisir explicitement la période de référence et diviser les valeurs.'],['Cumul : cumsum()','RUNNINGSUM pour un calcul visuel.'],['Lissage : rolling(3).mean()','MOVINGAVERAGE pour un calcul visuel ; vérifier l’ordre et les premières fenêtres.'],['Part du total','Définir le total de référence et son contexte de filtre.'],['Marge sur CA : ratio des sommes','DIVIDE entre la somme des profits et celle des ventes.']])+'''<p><code>RUNNINGSUM</code> et <code>MOVINGAVERAGE</code> sont des fonctions de calcul visuel : leur résultat dépend des lignes, de l’ordre et des réinitialisations du visuel. Ce ne sont pas des mesures interchangeables avec les colonnes pandas. Vérifiez aussi les périodes absentes et le traitement des fenêtres incomplètes.</p><p class="source">Sources Microsoft : <a href="https://learn.microsoft.com/en-us/dax/runningsum-function-dax">RUNNINGSUM</a> · <a href="https://learn.microsoft.com/en-us/dax/movingaverage-function-dax">MOVINGAVERAGE</a>.</p>'''

REVISIONS={1:[('pandas','Calculer avant de tracer.'),('Figure / Axes','Document / zone de dessin.'),('Barres','Comparer des catégories.'),('Courbe','Suivre une chronologie.'),('Histogramme','Compter dans des intervalles.'),('Part du total','Composante / total du périmètre × 100.')],2:[('Variation','Référence : ligne précédente.'),('Évolution','Référence : première période.'),('Cumul','Addition en euros.'),('Moyenne mobile','Fenêtre de lignes ordonnées.'),('Marge sur CA','Somme des profits / somme des ventes.'),('Interprétation','Nommer unité, référence et limite.')]}
QUESTIONS={1:['Quand choisir des barres plutôt qu’une courbe ?','Qui calcule les sommes avant le tracé ?','Quelle différence entre Figure et Axes ?','Pourquoi trier les noms avec les valeurs ?','Quel dénominateur utilise une part du total ?','Quel grain utilise notre histogramme ?'],2:['Pourquoi mars vaut-il −25 % et −10 % selon la référence ?','Pourquoi janvier est-il NaN pour la variation et 0 % pour l’évolution ?','Pourquoi un cumul peut-il monter pendant une baisse mensuelle ?','Que signifie rolling(3) si un mois manque ?','Pourquoi le ratio global diffère-t-il de la moyenne des taux ?','Quelles vérifications faire avant d’interpréter un graphique ?']}

def revision(block):
    n=block['n']
    text='<h2>Retenir avant le QCM.</h2><h3>Fiche de révision</h3><div class="revision-grid">'+''.join(f'<p><strong>{a}</strong><br>{b}</p>' for a,b in REVISIONS[n])+'</div><h3>Erreurs fréquentes</h3>'
    text+=('<p>Tracer les lignes brutes comme si elles étaient déjà additionnées ; trier les montants seuls ; omettre unité ou périmètre ; lire un nombre de lignes comme un nombre de commandes.</p>' if n==1 else '<p>Calculer sur des mois désordonnés ; sommer des pourcentages de variation ; remplacer les NaN par zéro ; diviser par zéro ; moyenner des taux pour obtenir le ratio global.</p><p>Dans notre tableau les dénominateurs sont positifs. Avec une référence ou un total nul, le ratio est indéfini : il faut le signaler, pas inventer 0 %. Avec des mois absents, vérifier le calendrier avant pct_change ou rolling.</p>')
    text+='<h3>Questions de révision</h3><ol>'+''.join(f'<li>{q}</li>' for q in QUESTIONS[n])+'</ol><h3>Résumé final</h3><p>'+('Préparez les valeurs avec pandas. Choisissez la représentation selon la question. Ciblez un Axes, rendez le titre et l’unité explicites, contrôlez les chiffres et exportez. Rejouez le carnet depuis un noyau neuf.' if n==1 else 'Un indicateur dépend de son dénominateur et de son périmètre. Variation, évolution et cumul répondent à des questions différentes. Le lissage décrit le passé ; le ratio de sommes mesure la marge globale sur CA. Confrontez chaque graphique aux chiffres avant de conclure.')+'</p>'
    text+=f'<div class="quiz-invitation"><div><p class="eyebrow">Fin du bloc {n:02}</p><h3>QCM avec feedback</h3><p>Choisissez une réponse, puis lisez son explication avant de poursuivre.</p></div><a class="button primary" href="../qcm/{block["slug"]}.html#quiz-panel">Faire le QCM →</a></div>'
    text+='<p class="source">Références : <a href="https://matplotlib.org/stable/users/explain/quick_start.html">Matplotlib</a> · <a href="https://seaborn.pydata.org/tutorial/introduction.html">Seaborn</a> · <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html">pct_change</a> · <a href="https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html">rolling</a>.</p>'
    return text

def quiz_sections(block):
    flash='<h2>Se rappeler avant de choisir.</h2><p>Répondez de mémoire, puis révélez l’explication.</p><p id="recall-counter" class="recall-counter" aria-live="polite" hidden></p>'+''.join(f'<article class="recall-card"><span class="mini-label">Carte {i}</span><h3>{q}</h3>'+details('Révéler la réponse',f'<p>{a}</p>')+'</article>' for i,(q,a) in enumerate(block['flash'],1))+'<div class="recall-controls" hidden><button class="button" id="recall-prev">← Précédente</button><button class="button primary" id="recall-next">Suivante →</button></div>'
    quiz='<h2>Vérifier ses choix.</h2><p>Une réponse par question. Le feedback explique la bonne réponse après chaque choix. Le score est local à cette page.</p><form id="quiz">'
    for i,(q,options,answer,exp) in enumerate(block['quiz']):
        quiz+=f'<fieldset data-answer="{answer}"><legend>{i+1}. {html.escape(q)}</legend>'+''.join(f'<label class="quiz-option"><input type="radio" name="q{i}" value="{j}"><span>{html.escape(o)}</span></label>' for j,o in enumerate(options))+f'<p class="quiz-feedback" data-explanation="{html.escape(exp,quote=True)}" aria-live="polite" hidden></p></fieldset>'
    quiz+='<div class="actions"><button class="button primary" type="submit">Vérifier</button><button class="button" type="reset">Recommencer</button></div><p id="quiz-score" role="status"></p></form><noscript><p>Activez JavaScript pour le feedback interactif, ou consultez les réponses ci-dessous.</p></noscript>'+details('Correction complète après le QCM','<ol>'+''.join(f'<li><strong>{html.escape(opts[a])}.</strong> {exp}</li>' for _,opts,a,exp in block['quiz'])+'</ol>')
    if block['n']==1:quiz+='<div class="actions"><a class="button primary" href="../supports/02_indicateurs.html">Après la correction : ouvrir le bloc 2 →</a></div>'
    return [('flashcards','Flashcards',flash),('quiz-panel','QCM de fin de bloc',quiz)]

def cell(kind,text):
    item={'cell_type':kind,'metadata':{},'source':text.splitlines(keepends=True)}
    if kind=='code':item.update(execution_count=None,outputs=[])
    return item

def notebooks(block):
    for corrected in (False,True):
        cells=[cell('markdown',f'# Bloc {block["n"]:02} — {block["title"]}\n\n'+('**Correction formateur — à consulter après chaque essai.**\n\n' if corrected else '')+'Exemple → petit exercice → correction collective. Faites une copie à votre nom et exécutez dans l’ordre. Les chemins /workspace sont ceux de la sandbox Docker. Dans un Jupyter externe, adaptez les chemins de lecture et d’export.\n\n'+block['intro'])]
        if block['n']==2:cells.extend([cell('markdown',INTRO2),cell('code',block['setup']),cell('markdown','Chaque ligne est un mois ; les dates sont triées. La variable mois contient les étiquettes du graphique. Le profit est un montant fictif fourni, pas calculé depuis le CSV de janvier.'),cell('code',MONTHLY)])
        for i,lesson in enumerate(block['lessons'],1):
            cells.append(cell('markdown',lesson['text']))
            if lesson.get('gallery'):
                cells.append(cell('markdown','\n\n'.join(f'### {title}\n![{alt}](../data/visuels/{name}.png)' for name,title,alt in GALLERY)))
            elif lesson.get('figure'):
                cells.append(cell('markdown',f'![{lesson["alt"]}](../data/visuels/{lesson["figure"]}.png)'))
            if lesson.get('before_code'):cells.extend([cell('code',lesson['before_code']),cell('markdown','### Même histogramme avec Seaborn')])
            if lesson['code']:cells.append(cell('code',lesson['code']))
            if lesson['reading']:cells.append(cell('markdown','### '+('Lecture du code et résultat' if lesson['code'] else 'Comment lire la figure')+'\n'+lesson['reading']))
            e=lesson['exercise']
            cells.append(cell('markdown',f'## Petit exercice {i} — {e["title"]}\n\n**Objectif :** {e["objective"]} **Prérequis :** {e["prereq"]}\n\n{e["prompt"]}\n\n**Livrable :** {e["deliverable"]}\n\n**Réussite :** {e["success"]}\n\nContrainte : utiliser les données fournies et les méthodes déjà présentées.\n\n'+''.join(details(f'Indice {j}',f'<p>{h}</p>') for j,h in enumerate(e['hints'],1))))
            if corrected:
                if e['solution']:cells.append(cell('code',e['solution']))
                cells.append(cell('markdown','### Correction collective\n'+e['answer']))
            else:
                cells.extend([cell('markdown','### Ma prédiction / ma démarche\nÀ compléter avant de lancer le code.'),cell('code',e['starter']),cell('markdown','### Mon résultat et la correction collective\nÀ compléter pendant notre mise en commun : résultat, explication et éventuelle correction.')])
        cells.append(cell('markdown','## Fin du bloc\n\n- Vérifier les montants, unités et références.\n- Redémarrer le noyau puis tout exécuter.\n- Revenir au support HTML pour le **QCM de fin de bloc avec feedback**.\n\n### Fiche de révision\n'+ '\n'.join(f'- **{a} :** {b}' for a,b in REVISIONS[block['n']])+'\n\n### Questions de révision\n'+ '\n'.join(f'{i}. {q}' for i,q in enumerate(QUESTIONS[block['n']],1))))
        for i,c in enumerate(cells):c['id']=f'bloc{block["n"]}-{i:03}'
        nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
        folder='corrections' if corrected else 'notebooks'
        name=block['notebook']+('_corrige' if corrected else '')+'.ipynb'
        write(f'sandbox-notebook/{folder}/{name}',json.dumps(nb,ensure_ascii=False,indent=1)+'\n')

def card(step,title,desc,url,pill):
    return f'<a class="path-card" href="{url}"><span class="card-top"><span class="step-number">{step}</span><span class="pill">{pill}</span></span><h3>{title}</h3><p>{desc}</p><span class="card-bottom">Ouvrir <span aria-hidden="true">↗</span></span></a>'

def main():
    for block in BLOCKS:
        intro=INTRO1 if block['n']==1 else INTRO2+code(block['setup'])+'<h3>Lecture du code</h3><p>DataFrame crée la petite table. date_range produit les six débuts de mois (MS). sort_values impose l’ordre chronologique ; reset_index renumérote les lignes ; strftime prépare des étiquettes mois/année. Les ventes et profits restent numériques.</p>'+code(MONTHLY)+figure('02_mensuel','Ventes mensuelles : 10 000, 12 000, 9 000, 15 000, 18 000 puis 16 500 euros.')
        sections=[('sandbox','Introduction',intro)]
        corrections=[('mode','Correction collective','<h2>Comparer après chaque essai.</h2><p>Reprenez les cellules de démonstration du bloc dans l’ordre avant les corrections. Les solutions réutilisent leurs variables. Plusieurs titres ou couleurs sont possibles ; les calculs et leurs références doivent rester justes.</p>')]
        for i,lesson in enumerate(block['lessons'],1):
            body=lesson['text']
            if lesson.get('gallery'):
                body+='<div class="gallery-grid">'+''.join(figure(name,alt,title) for name,title,alt in GALLERY)+'</div>'
            elif lesson.get('figure'):
                body+=figure(lesson['figure'],lesson['alt'])
            if lesson.get('before_code'):body+=code(lesson['before_code'])+'<h3>Exemple Seaborn</h3>'
            if lesson['code']:body+=code(lesson['code'])
            if lesson.get('comparison'):
                body+=figure('02_mensuel','Ventes mensuelles : baisse de 18 000 à 16 500 euros entre mai et juin.','Comparer avec les montants mensuels. Les deux graphiques ont leurs propres échelles : lire les axes, pas seulement la hauteur des points.')
                body+=table(['Mois','Ventes (€)','Variation mensuelle','Évolution / janvier','Cumul (€)'],SUMMARY_ROWS)
            if lesson['reading']:body+='<h3>'+('Lecture du code et résultat' if lesson['code'] else 'Comment lire la figure')+'</h3><p>'+lesson['reading']+'</p>'
            body+=exercise(block,lesson,i)
            sections.append((lesson['id'],lesson['title'],body))
            e=lesson['exercise']
            answer=f'<h2>{e["title"]}</h2><p><strong>Question :</strong> {e["prompt"]}</p>'
            if e['solution']:answer+=code(e['solution'])
            answer+=f'<h3>Résultat et explication</h3><p>{e["answer"]}</p><p><strong>À faire verbaliser :</strong> {e["success"]}</p><a class="button" href="{block["slug"]}.html#{lesson["id"]}">← Revenir à l’exemple et à l’exercice</a>'
            corrections.append((f'correction-{i}',f'Exercice {i:02}',answer))
        sections.append(('projet','Le fil rouge',PROJECT))
        if block['n']==2:sections.append(('powerbi','Passerelle facultative',BRIDGE))
        sections.append(('revision','Fin de bloc · QCM',revision(block)))
        write(f'docs/supports/{block["slug"]}.html',page(block,sections))
        write(f'docs/supports/correction_{block["n"]:02}.html',page(block,corrections,'correction'))
        write(f'docs/qcm/{block["slug"]}.html',page(block,quiz_sections(block),'qcm'))
        notebooks(block)
    home=head('Des graphiques aux indicateurs','.')+'''<main class="home" id="contenu"><section class="hero"><div><p class="eyebrow"><span class="status-dot"></span> Comprendre les données, puis les représenter</p><h1>Vos données.<br>Une figure.<br><span>Une réponse.</span></h1><p class="hero-description">Réactivez les bases de Matplotlib. Construisez des graphiques, calculez des indicateurs et expliquez vos résultats, avec de petits exercices corrigés ensemble.</p><div class="actions"><a class="button primary" href="supports/01_graphiques_fiables.html">Commencer le premier bloc →</a><a class="button" href="data/sandbox-notebook.zip" download>La sandbox ↓</a></div><p class="hero-note">Bases Python · Matplotlib et Seaborn · pandas · Notebook</p></div><div class="hero-illustration"><div class="diagram-heading"><span class="mini-label">De la question au graphique</span><span class="pill">Matplotlib</span></div><div class="flow-step"><span class="flow-index">01</span><div><small>OBSERVER</small><strong>Un exemple concret</strong></div></div><div class="flow-connector" aria-hidden="true">↓</div><div class="flow-step treatment"><span class="flow-index">02</span><div><small>ESSAYER</small><strong>Un petit exercice</strong></div></div><div class="flow-connector" aria-hidden="true">↓</div><div class="flow-step"><span class="flow-index">03</span><div><small>COMPRENDRE</small><strong>Une correction collective</strong></div></div><p class="diagram-caption">Puis un QCM avec feedback en fin de bloc.</p></div></section>'''
    for b in BLOCKS:
        home+=f'<section class="home-path-section"><div class="section-heading"><div><p class="eyebrow">Bloc {b["n"]:02}</p><h2>{b["title"]}</h2></div></div><nav class="path-grid home-grid" aria-label="Parcours bloc {b["n"]}">'+card('EXEMPLES ET EXERCICES',b['title'],'Observer, calculer, tracer et expliquer. Une correction collective après chaque essai.',f'supports/{b["slug"]}.html','Cours')+card('MISE EN COMMUN','Corriger ensemble','Retrouver le code, les résultats et les questions à discuter.',f'supports/correction_{b["n"]:02}.html','Corrections')+card('FIN DE BLOC','QCM avec feedback','Huit questions expliquées et six flashcards pour réactiver les notions.',f'qcm/{b["slug"]}.html#quiz-panel','Se vérifier')+'</nav></section>'
    home+='<aside class="home-tip"><span class="tip-mark" aria-hidden="true">i</span><p><strong>Le bon réflexe :</strong> prédire le résultat, essayer dans le notebook, puis expliquer les écarts pendant la correction.</p></aside></main>'+foot('.')
    write('docs/index.html',home)
    monthly='mois,ventes,profit\n2026-01-01,10000,2000\n2026-02-01,12000,3000\n2026-03-01,9000,1800\n2026-04-01,15000,3750\n2026-05-01,18000,4500\n2026-06-01,16500,3300\n'
    for folder in ['docs/data','sandbox-notebook/data']:write(f'{folder}/indicateurs_mensuels.csv',monthly)
    print('Deux blocs, deux QCM, corrections et carnets modèles générés ; aucune durée pédagogique.')

if __name__=='__main__':main()
