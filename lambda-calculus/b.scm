; #!/usr/local/bin/mit-scheme
; in inter
;; cf "b"
;; mit-scheme < b.scm

; IO
(display "hello, world!")
(newline)

; functor
(define (plus4 x) (+ x 4))
(plus4 3)

; lambda
(define add (lambda (x y) (+ x y)))
(add 3 8)

((lambda (x y) (+ x y)) 2 9)

;; functor: map

(define x (map (lambda (x) (* x x)) '(1 2 3 4)))
(display x)

