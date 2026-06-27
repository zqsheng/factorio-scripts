% yolanda, mia

happy(yolanda).
listens2Music(mia).

listens2Music(yolanda):-happy(yolanda). % `if happy -> listens2Music` or `is implied by`
playsAirGuitar(mia):-listens2Music(mia).
playsAirGuitar(yolanda):-listens2Music(yolanda). % 

% Queries
% PlaysAirGuitar(mia). true
% PlaysAirGuitar(yolanda). true
