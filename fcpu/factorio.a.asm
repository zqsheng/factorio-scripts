; factroi fCPU script

; qulity set = normal, uncommon, rare, epic, legendary
; entity set = stone, holmium-ore

; recipe(holmium result = 1xstone + 2xholumium)

clr
;;;;;;;;;;; - start

clr m1
emit m1 1[item=holmium-ore,quality=legendary]
xflt m3 red m1
xmin r1 m3

clr m1
emit m1 1[item=stone,quality=legendary]
xflt m3 red m1
xmin r2 m3

mul r2 2

tlt r1 r2
mov r3 r1

tlt r2 r1 
mov r3 r2


mov r4 1[virtual-signal=signal-red,quality=legendary
swpv r3 r4
tgt r4 100
jmp :done

;;;;;;;;;;;; - end
;;;;;;;;;;; - start

clr m1
emit m1 1[item=holmium-ore,quality=epic]
xflt m3 red m1
xmin r1 m3

clr m1
emit m1 1[item=stone,quality=epic]
xflt m3 red m1
xmin r2 m3

mul r2 2

tlt r1 r2
mov r3 r1

tlt r2 r1 
mov r3 r2


mov r4 1[virtual-signal=signal-red,quality=epic]
swpv r3 r4
tgt r4 100
jmp :done

;;;;;;;;;;;; - end
;;;;;;;;;;; - start

clr m1
emit m1 1[item=holmium-ore,quality=rare]
xflt m3 red m1
xmin r1 m3

clr m1
emit m1 1[item=stone,quality=rare]
xflt m3 red m1
xmin r2 m3

mul r2 2

tlt r1 r2
mov r3 r1

tlt r2 r1 
mov r3 r2


mov r4 1[virtual-signal=signal-red,quality=rare]
swpv r3 r4
tgt r4 100
jmp :done

;;;;;;;;;;;; - end
;;;;;;;;;;; - start

clr m1
emit m1 1[item=holmium-ore,quality=uncommon]
xflt m3 red m1
xmin r1 m3

clr m1
emit m1 1[item=stone,quality=uncommon]
xflt m3 red m1
xmin r2 m3

mul r2 2

tlt r1 r2
mov r3 r1

tlt r2 r1 
mov r3 r2


mov r4 1[virtual-signal=signal-red,quality=uncommon]
swpv r3 r4
tgt r4 100
jmp :done

;;;;;;;;;;;; - end

;;;;;;;;;;; - start

clr m1
emit m1 1[item=holmium-ore,quality=normal]
xflt m3 red m1
xmin r1 m3

clr m1
emit m1 1[item=stone,quality=normal]
xflt m3 red m1
xmin r2 m3

mul r2 2

tlt r1 r2
mov r3 r1

tlt r2 r1 
mov r3 r2


mov r4 1[virtual-signal=signal-red,quality=normal]
swpv r3 r4
tgt r4 100
jmp :done

;;;;;;;;;;;; - end




:done

clr m1
emit m1 r4
xmov output m1








