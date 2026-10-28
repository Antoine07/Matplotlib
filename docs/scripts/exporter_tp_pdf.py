"""Exporter uniquement le sujet du TP, sans les corrections, en PDF A4."""
from pathlib import Path
import shutil
import subprocess
import tempfile

from tp_content import TP


ROOT = Path(__file__).resolve().parents[1]


def tex(text):
    escapes = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
               '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(escapes.get(character, character) for character in text)


def main():
    engine = shutil.which('xelatex')
    if engine is None:
        raise SystemExit('XeLaTeX est nécessaire pour produire ce PDF.')
    fields = '\n'.join(r'\texttt{' + tex(name) + '} & ' + tex(description) + r' \\'
                       for name, description in TP['fields'])
    visuals = '\n'.join(r'\item \textbf{' + tex(title) + '}\n\n' + tex(task)
                        for title, task in TP['visuals'])
    count_word = {2: 'deux', 4: 'quatre'}.get(len(TP['visuals']), str(len(TP['visuals'])))
    optional = TP.get('optional_question')
    optional_text = ''
    if optional:
        optional_text = r'\sectiontitle{Question facultative · ' + tex(optional['title']) + '}\n' + tex(optional['prompt'])
    # Sélectionner explicitement le sujet : ne pas importer SOLUTION ou INSIGHTS.
    source = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=19mm,headheight=14pt,footskip=12mm]{geometry}
\usepackage{fontspec}
\setmainfont{texgyreheros}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
\setmonofont{lmmono10-regular.otf}
\usepackage[table]{xcolor}
\definecolor{coursegreen}{HTML}{275C47}
\definecolor{courselime}{HTML}{B5CF66}
\definecolor{coursesoft}{HTML}{EEF3E7}
\definecolor{courseink}{HTML}{203B36}
\definecolor{coursemuted}{HTML}{63716A}
\usepackage{tabularx,enumitem,fancyhdr}
\usepackage[unicode,hidelinks]{hyperref}
\hypersetup{pdftitle={TP en binômes — Préparer un tableau de bord Power BI},pdfauthor={Le labo Matplotlib / NEXA}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{coursegreen}\textbf{Le labo Matplotlib}}
\fancyhead[R]{\small\color{coursemuted}NEXA · Sujet du TP}
\fancyfoot[L]{\footnotesize\color{coursemuted}Pandas · Matplotlib · Power BI}
\fancyfoot[R]{\footnotesize\color{coursemuted}\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\setlist[enumerate]{leftmargin=6mm,itemsep=12pt,topsep=5pt}
\setlist[itemize]{leftmargin=5mm,itemsep=5pt,topsep=4pt}
\newcommand{\sectiontitle}[1]{\par\vspace{8pt}{\large\bfseries\color{coursegreen}#1}\par\vspace{2pt}}
\color{courseink}
\begin{document}
{\small\bfseries\color{coursegreen}TP EN BINÔMES}\par
{\fontsize{25}{29}\selectfont\bfseries\color{coursegreen}Préparer un tableau\par de bord Power BI}\par
\vspace{3pt}
\textcolor{courselime}{\rule{\linewidth}{3pt}}

__INTRO__

\sectiontitle{Votre mission}
\textbf{__QUESTION__}

Votre notebook constitue une maquette analytique pour un futur tableau de bord Power BI destiné à la responsable commerciale.

\sectiontitle{Les données : réseau Nova}
Utilisez le fichier \texttt{/workspace/data/__FILENAME__}.

Ces données pédagogiques sont fictives et couvrent l’année 2025. Une ligne correspond à une ligne de commande ; une commande peut contenir plusieurs produits. Les montants sont exprimés en euros hors taxes.

\begingroup
\fontsize{9.5}{12}\selectfont
\renewcommand{\arraystretch}{1.22}
\rowcolors{2}{coursesoft}{white}
\begin{tabularx}{\linewidth}{@{}p{35mm}X@{}}
\rowcolor{coursegreen}\color{white}\textbf{Colonne} & \color{white}\textbf{Signification} \\
__FIELDS__
\end{tabularx}
\endgroup

{\small La marge commerciale est la différence entre le chiffre d’affaires et le coût d’achat. Le pourcentage demandé rapporte cette marge au chiffre d’affaires. Les autres charges de l’entreprise ne sont pas décrites.}

\newpage
{\small\bfseries\color{coursegreen}TRAVAIL DEMANDÉ}\par
{\fontsize{25}{29}\selectfont\bfseries\color{coursegreen}__GRAPH_TITLE__ graphiques,\par deux insights}\par
\vspace{3pt}
\textcolor{courselime}{\rule{\linewidth}{3pt}}

\sectiontitle{Les __GRAPH_COUNT__ graphiques}
\begin{enumerate}
__VISUALS__
\end{enumerate}

Chaque graphique doit comporter un titre, des axes lisibles et les unités appropriées.

\sectiontitle{Les deux insights}
Rédigez exactement deux insights portant sur des constats différents et appuyés sur les graphiques. Chaque insight présente un constat métier précis, les chiffres qui le justifient et une implication ou une piste d’action.

\sectiontitle{À rendre}
\begin{itemize}
\item Un notebook créé par votre binôme, contenant les calculs, les __GRAPH_COUNT__ graphiques et les deux insights.
\item Les __GRAPH_COUNT__ figures exportées en PNG dans \texttt{/workspace/resultats}.
\end{itemize}

Le notebook doit pouvoir s’exécuter de haut en bas après redémarrage du noyau.
__OPTIONAL__
\end{document}
'''
    for marker, value in {'INTRO': tex(TP['intro']), 'QUESTION': tex(TP['question']),
                          'FILENAME': tex(TP['data_file']), 'FIELDS': fields,
                          'VISUALS': visuals, 'GRAPH_COUNT': count_word,
                          'GRAPH_TITLE': count_word.capitalize(),
                          'OPTIONAL': optional_text}.items():
        source = source.replace(f'__{marker}__', value)
    target = ROOT / 'tp_binomes.pdf'
    with tempfile.TemporaryDirectory(prefix='matplotlib-tp-pdf-') as directory:
        work = Path(directory)
        (work / 'sujet.tex').write_text(source, encoding='utf8')
        for _ in range(2):
            result = subprocess.run([engine, '-no-shell-escape', '-interaction=nonstopmode',
                                     '-halt-on-error', 'sujet.tex'], cwd=work,
                                    capture_output=True, text=True)
            if result.returncode:
                raise SystemExit(result.stdout[-5000:])
        log = (work / 'sujet.log').read_text()
        if 'Overfull \\hbox' in log or 'Overfull \\vbox' in log:
            raise SystemExit('Le PDF comporte un débordement : vérifier la mise en page.')
        shutil.copyfile(work / 'sujet.pdf', target)
    print(target)


if __name__ == '__main__':
    main()
