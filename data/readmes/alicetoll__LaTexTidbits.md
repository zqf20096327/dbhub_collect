# LaTexTidbits

LaTeX for loops
  - forloop.tex
    - loops over printing patterns
    - no R integration
  - forloopKnitr.rnw and forloopKnitr_child.rnw
    - uses Knitr for R integration
    - uses two files
    - parent file contains loop
    - child file contains what is done in the loop
    - output is saved to a variable that is then printed using \Sexpr{}

Print multiple Beamer slides on one page
  - Toll_Presentation.tex is original presentation
  - Handout.tex takes Toll_Presentation.tex as input and makes new pdf with 6 slides per page
