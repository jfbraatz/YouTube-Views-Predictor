(TeX-add-style-hook
 "proposal"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "12pt")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "fullpage"
    "enumitem"
    "amsmath"
    "amsthm"
    "amsfonts"
    "amssymb"
    "graphicx"
    "float"
    "listings")
   (TeX-add-symbols
    '("abs" 1)
    "RR"
    "ZZ")
   (LaTeX-add-bibitems
    "Cd94")
   (LaTeX-add-amsthm-newtheorems
    "thm"
    "cor"
    "lem"
    "prop"
    "defn"
    "rem"))
 :latex)

