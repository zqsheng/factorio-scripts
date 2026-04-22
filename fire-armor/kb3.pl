% Knowledge Base 3

happy(vincent).
listens2Music(butch).

playsAirGuitar(vincent):-
	listens2Music(vincent), % `and` or `logical conjunction`
	happy(vincent).

playsAirGuitar(butch):-
	happy(butch).

%playsAirGuitar(butch):-
%	happy(butch);
%	listens2Music(butch).
	

% Queries
% playsAirGuitar(vincent). false

