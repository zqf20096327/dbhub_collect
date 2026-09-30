# Assignments from the course DM840.

These projects have not been cleaned or corrected. please see at own risk.

## Assignment 1
Solves games and some chemical reactions via graph grammar.

## Assignment 2
Solves Atom to atom mapping, this, is poorly made, let's not talk more about it than that, should probably be redone with actual code, but at a later time. when i need to rewise the topic.

TLDL: It's a mess.


Running things at the IMADA computer room can be done via 

nohup sh solvecatalanonimada.sh&> file7.out&


 && ./test $@ && mod_post
mv summary/summary.pdf summary/Atom-Atom-Mapping.pdf
scp summary/Atom-Atom-Mapping.pdf alzira:WWWpublic/dm840/
rm summary/Atom-Atom-Mapping.pdf



To copy the reporst to the web server run
scp logon.sdu.dk:courses/DM840/formose/summary/summary.pdf /var/www/doommius.com/html/dm840/formose/
scp logon.sdu.dk:courses/DM840/catalan/summary/summary.pdf /var/www/doommius.com/html/dm840/catalan/