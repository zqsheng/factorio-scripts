/cc 
local signals = {}
Append(signals, {item = 'iron', count = 10})


local a = ConstantCombinator(true, signals)
local b = DeciderCombinator(true)
Wire(a, OutRed, b, InRed)


