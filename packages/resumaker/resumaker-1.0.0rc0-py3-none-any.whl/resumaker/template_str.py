template = {
    "license": r"""
% Medium Length Professional CV
% LaTeX Template
% Version 3.0 (December 17, 2022)
%
% This template originates from:
% https://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@latextemplates.com)
%
% Original author:
% Trey Hunner (http://www.treyhunner.com/)
%
% License:
% CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
% FILE HAS BEEN MODIFIED
""",
    "setup": r"""
\documentclass[
	%a4paper, % Uncomment for A4 paper size (default is US letter)
	11pt, % Default font size, can use 10pt, 11pt or 12pt
]{resume} % Use the resume class

\usepackage{ebgaramond} % Use the EB Garamond font
\usepackage{hyperref}
\hypersetup
{
    colorlinks=true,
    urlcolor=blue
}

\input{glyphtounicode}
\pdfgentounicode=1
""",
    "main": r"""
\begin{document}
$CONTENT
\end{document}
""",
    "contact": r"""
\name{$name}
\address{$location}
\address{\raisebox{-2px}{\includegraphics[width=10px]{icons/phone.png}}  $phone \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/mail.png}} $email  \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/linkedin.png}} \href{https://www.linkedin.com/in/$linkedin/}{linkedin.com/in/$linkedin} \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/github.png}} \href{https://github.com/$github}{github.com/$github}}
""",
    "education": {
        "complete": r"""
    \begin{rSection}{Education}
        $all_education
    \end{rSection}""",
        "single": r"""

        \textbf{$degree} \hfill \textit{$duration} \\ 
        $institution_name, $institution_location \\
        $all_achievements
        """,
        "achievement": r"$single_achievement \\",
    },
    "links": {
        "complete": r"""
\begin{rSection}{Links}
	\begin{tabular}{@{} >{\bfseries}l @{\hspace{6ex}} l @{}}
        $all_links
	\end{tabular}
\end{rSection}""",
        "single": r"$link_title & \href{$link_url}{$link_url_text} \\",
    },
    "summary": r"""
\begin{rSection}{$title}
    $text
\end{rSection}
""",
    "skills": {
        "complete": r"""
            \begin{rSection}{Skills}
                \begin{tabular}{@{} >{\bfseries}l @{\hspace{6ex}} l @{}}
                    $all_skills
                \end{tabular}
            \end{rSection}
    """,
        "single": r"$skill_topic & $skills_list \\",
    },
    "work_experience": {
        "complete": r"""
                \begin{rSection}{Work Experience}
                \def \\ {\addressSep\ } 
                $all_work_experiences
            \end{rSection}
    """,
        "single": r"""
            \begin{rSubsection}{$company_name, $company_location \\ $position \\ $duration}{}{}{}
                    $all_contributions
	        \end{rSubsection}
        """,
        "single-contribution": r"\item $contribution",
    },
    "projects": {
        "complete": r"""
                \begin{rSection}{Projects}
                $all_projects
            \end{rSection}
    """,
        "single": r"""
            \begin{rSubsection}{$project_name}{$technologies}{}{}
                    $all_details
	        \end{rSubsection}
        """,
        "single-detail": r"\item $detail",
    },
}
