% Recursive 

is_digesting(X, Y) :- just_ate(X, Y).
is_digesting(X, Y) :- 
	just_ate(X,Z), 
	is_digesting(Z, Y).

just_ate(mosquito, blood(john)).
just_ate(frog, mosquito).
just_ate(stork, frog).


%

descend(X, Y) :- child(X, Y). 
descend(X, Y) :- child(X, Z),
		descend(Z, Y).


%
numernal(0).
numernal(succ(X)) :- numernal(X).

