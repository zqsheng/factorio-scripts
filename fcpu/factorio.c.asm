;; Automatic recipe switcher

;; 64 general purpose registers (1-64)
;; 4 memory channels for vector processing(1-4)


;; red   wire: logistic network stroage 
;; green wire: recipe
;; output    : quality

;; 


;;

 
mov r10 1[virtual-signal=signal-red,quality=normal]
mov r11 1[virtual-signal=signal-red,quality=uncommon]
mov r12 1[virtual-signal=signal-red,quality=rare]
mov r13 1[virtual-signal=signal-red,quality=epic]
mov r14 1[virtual-signal=signal-red,quality=legendary]


;; loop0 init
mov r1 14
:loop0


;;  loop1 init
clr m1
mov r2 1
mov r5 99
:loop1

mov r3 green@2
mov r4 r@1
ssq r3 r4
emit m1 r3


;; loop1 for
inc r2
tle r2 cng
jmp :loop1

xdiv m1 red m1

;; set output
xmin r5 m1

tlt r5 5
jmp :nextq

teq cnm1 cng
mov out1 r4

tgt r5 5
teq cnm1 cng
jmp :done

:nextq

;; loop0 for
dec r1
tgt r1 9
jmp :loop0

:done

