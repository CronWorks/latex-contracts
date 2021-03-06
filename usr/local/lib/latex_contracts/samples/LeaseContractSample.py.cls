
            \NeedsTeXFormat{LaTeX2e}[1999/09/01]
            \ProvidesClass{/home/luke/Reference/Code/Source/latex-contracts/usr/local/lib/latex_contracts/samples/LeaseContractSample.py}[2014/ 5/10 J Luke Scott, Copyright (C) 2014]
        %% Copyright (C) 2011-2013 J Luke Scott
%% This material is subject to the LaTeX Project Public License. See
%% http://www.ctan.org/tex-archive/help/Catalogue/licenses.lppl.html for the details of that
%% license.

%% NOTE: This file contains Jinja directives. You must process it using Jinja.
%% NOTE: do not use \NeedsTeXFormat or \ProvidesClass. This will be set automatically.

\usepackage{fontspec} % allows the sans font
\setsansfont[Scale=MatchLowercase,Mapping=tex-text]{Open Sans}
\renewcommand{\familydefault}{\sfdefault} % sans font


\LoadClass[10pt,letterpaper]{article}

% why does hyperref cause the bad pagination/margin screwups?
%\usepackage[hidelinks]{hyperref}% form fields, hyperlinks for \ref{}

\usepackage[hang,flushmargin]{footmisc} % Align the footnote number better
\usepackage[letterpaper]{geometry}
\geometry{
    verbose,
    tmargin=2.5cm,
    bmargin=2.5cm,
    lmargin=3cm,
    rmargin=3cm
}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}% also determines form spacing
\setlength{\footskip}{90pt}

\usepackage{etoolbox}% provides \csdef, \csuse, \providebool, \booltrue, \boolfalse, \ifbool
\usepackage{wasysym}% provides \Square (i.e. checkbox)

\usepackage{datetime}% \formatdate command
\mmddyyyydate % must be AFTER \usepackage{datetime}
\usepackage{microtype}


% widow/orphan control
\widowpenalty=300
\clubpenalty=300

% the structure of the contract itself - sections & clauses
\renewcommand \thesection{\Roman{section}.}
\renewcommand \thesubsection{\arabic{section}.\arabic{subsection}}
\renewcommand{\section}{%
    \@startsection{section}{1}{0pt}{15pt}{5pt}{\centering\large\bfseries}
}
\renewcommand{\subsection}{%
    \@startsection{subsection}{2}{0pt}{10pt}{1pt}{\bfseries}
}

\newcommand{\sectionintro}[1]{
    \begin{center}
        \parbox[t]{0.7\textwidth}{\centering\textit{#1}}
    \end{center}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%          Clauses          %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% \textwidth = \clauseNumberWidth + \clauseWidth
% \clauseNumberWidth = {right-aligned number} + \clauseNumberPadding
% For definition lines: \clauseWidth = \definitionWidth + {remainder = def. text}
% For form lines: \clauseWidth = \formLabelWidth + {remainder = underline}
\newcommand{\clauseNumberWidth}{18pt}
\newcommand{\clauseNumberPadding}{5pt}
\newcommand{\formLineVerticalPadding}{10pt}% mostly for multi-line formlines

\newlength{\clauseWidth}
\setlength{\clauseWidth}{\textwidth}
\addtolength{\clauseWidth}{-\clauseNumberWidth}

\newcounter{Clause}
\newenvironment{clauseLine}{%
    \refstepcounter{Clause}%
    \begin{minipage}[t][][t]{\clauseNumberWidth}%
        \raggedleft \arabic{Clause}\hspace*{\clauseNumberPadding}%
    \end{minipage}%
    \begin{minipage}[t][][t]{\clauseWidth}%
}
{\end{minipage}\par}

\addtolength{\clauseWidth}{-13pt}% accounts for the \minipage slop when referring to this length

% A definition goes at the start of the document to identify lessor, tenant, dates, property
% address, etc
\newlength{\definitionLabelWidth}
\setlength{\definitionLabelWidth}{\clauseWidth}
\addtolength{\definitionLabelWidth}{-0.6\clauseWidth}% i.e. 0.4 * clauseWidth

\newlength{\definitionWidth}
\setlength{\definitionWidth}{\clauseWidth}
\addtolength{\definitionWidth}{-\definitionLabelWidth}

% format: \definition[abbreviatedTerm]{full text term}{description}
% NOTE: a label is created for the abbreviatedTerm, or the full text term if no abbreviatedTerm is given.
\newcommand{\definition}[3][]{% 
    \begin{clauseLine}%
        \parbox[t]{\definitionLabelWidth}{%
            {#2}%
            {\ifstrempty{#1}%
                {}%
                { (``{#1}'')}%
            }%
        :}%
        \parbox[t]{\definitionWidth}{\raggedleft{#3}}%
        {\ifstrempty{#1}%
            {\label{#2}}%
            {\label{#1}}%
        }%
    \end{clauseLine}%
}

% Create a clause. A clause is the most common paragraph-style element, identifying each of the main
% terms of the agreement. 
% TODO not written yet: Overridden clauses are accommodated by generating if/then blocks for each
% overridden clause label; if a clause is requested which matches a custom clause, then
% it is replaced by the custom content.
\newcommand{\clause}[2][]{%
    \par
    \begin{clauseLine}%
        \parbox[t]{\clauseWidth}{%
            {\ifstrempty{#1}{}{\bfseries{#1:~}}}%
            {#2}%
        }%
        {\ifstrempty{#1}{}{\label{#1}}}%
    \end{clauseLine}
    \par
}


% functions to standardize formatting in the clause text
\newcommand{\highlight}[1]{\textbf{{#1}}}

\newlength{\formLabelWidth}% width of the label of the form line
\setlength{\formLabelWidth}{0.3\clauseWidth}

\newlength{\formLabelSpacing}% width between label and _______
\setlength{\formLabelSpacing}{0.05\clauseWidth}

\newlength{\formUnderlineWidth}% width of the _______
\setlength{\formUnderlineWidth}{\clauseWidth}
\addtolength{\formUnderlineWidth}{-\formLabelWidth}
\addtolength{\formUnderlineWidth}{-\formLabelSpacing}

\newcommand{\formLine}[2][]{% format: \formLine[pre-filled content]{title shown on form}
    \formLineWithContent{\hrulefill}{#1}{#2}%
}
\newcommand{\formLineWithContent}[3]{% format: \formLineWithContent{parboxContent}{pre-filled content}{title shown on form}
    \vspace{\formLineVerticalPadding}%
    \begin{clauseLine}%
        \parbox[t]{\formLabelWidth}{{#3}:}%
        \hspace{\formLabelSpacing}%
        \rlap{\smash{\raisebox{3pt}{#2}}}% pre-filled content to put on the line
        \parbox[t]{\formUnderlineWidth}{%
            {#1}%
        }%
    \end{clauseLine}%
}

\newlength{\formCheckboxLabelWidth}
\setlength{\formCheckboxLabelWidth}{0.9\clauseWidth}

\newlength{\formCheckboxWidth}
\setlength{\formCheckboxWidth}{\clauseWidth}
\addtolength{\formCheckboxWidth}{-\formCheckboxLabelWidth}

\newcommand{\formLineCheckbox}[1]{%
    \par\vspace{\formLineVerticalPadding}
    \begin{clauseLine}%
        \parbox[t]{\formCheckboxLabelWidth}{{#1}:}%
        \parbox[t]{\formCheckboxWidth}{\raggedleft{\Large\Square}}%
    \end{clauseLine}%
}


%%%%%%%%%%%%%%%%%%%%%%%
%% Footer (initials) %%
%%%%%%%%%%%%%%%%%%%%%%%

% sign sections via contract object settings. This just sets TeX booleans which are used later.
\providebool{signSection1}\booltrue{signSection1}%
\providebool{signSection2}\booltrue{signSection2}%
\providebool{signSection3}\booltrue{signSection3}%
\providebool{signSection4}\booltrue{signSection4}%

% initials forms in the footer of each page
\newcommand{\initialsSpaceWidth}{1.9cm}
\newcommand{\getInitialsBox}{%
    \begin{tabular}{r r}%
        \getInitialsBoxLeft%
    \end{tabular}%
    \begin{tabular}{r r}%
        \getInitialsBoxRight%
    \end{tabular}%
}
\newcommand{\getInitialsBoxLeft}{}% renew in sub-formats
\newcommand{\getInitialsBoxRight}{}% renew in sub-formats


%%%%%%%%%%%%%%%%%%%%%%%%%
%% the actual document %%
%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{lastpage}% \pageref{LastPage} command
\AtBeginDocument{
    \ifthenelse{\pageref{LastPage}>1}{
        % multiple pages - show initials boxes and "page x of y"
        
            \newgeometry{
                bmargin=5cm
            }
        

        \renewcommand{\@oddfoot}{
            \parbox[b]{\textwidth}{
                \centering %
                %
                Initials:\\
                    \vspace{7pt}
                    \getInitialsBox% this will have to be created in the calling document/class
                
                
                \thepage\ of \pageref{LastPage}
            } 
        }
    }{ % only 1 page - don't show the initials or page number
        \let\@oddfoot\@empty
    }

    \begin{center}
        {\Large \textbf{Contract Agreement}} \\[0.5\baselineskip]
        \textbf{This document is a Contractual Agreement (``Agreement'') between the parties listed.}%
    \end{center}
    \rule{\linewidth}{0.3mm}
}
