;;; factorio fCPU script ;;;

; calculate fib(n)
; f(0) = 0
; f(1) = 1
; clr 


mov reg8 10 ; fib(reg8)
mov reg1 0
mov reg2 1
mov reg7 0

teq reg8 0
jmp :done

:loop
    add reg3 reg1 reg2
    mov reg1 reg2
    mov reg2 reg3
    inc reg7 
    tlt reg7 reg8
    jmp :loop

:done
mov out1 reg1
nop

