Why?
====

Some CLI *utility* apps I want to make have complex logic. After failing
two or three times, I realized that to implement such things, imperative
code may not be the best thing.

After reading The Elm Architecture (and because I can not learn Elixir or
Clojure at the moment) I decided to try to implement the philosophy of Elm
and Redux in a Python framework. Python because it

-  interacts with system much better than JS
-  is cross-platform enough, without being Java which ICNLATM
-  comes installed on most systems I'd work on

Take a look at the ``examples/``

You may need to:

``export PYTHONPATH=$PWD:$PYTHONPATH``

Progress so far
---------------

I am focusing on CLI only. So you *have* to press <Enter> key often.

I am really inspired by the questions posed by Evan in the blockquotes
of lessons given at guide.elm-lang.org, as such I have tried to address
them all done all three examples

-  all signal/msg are derived from a hidden ``Msg`` class
-  a custom switch case construct is provided, it alerts you when a case
   is missing, when a case is repeated, or a case is not of ``Msg`` type
-  whole app's state is in a single immutable dictionary
-  (pseudo-)pattern matching


