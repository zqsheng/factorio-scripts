;; Y-combinator
;; interpreter: chibi-scheme/RS87
;; 
(import (scheme base)
        (scheme write))
(display "Y-combinator")
(newline)

;; Traditional Y combinator(applicative-order, strict)
;; Y = λf.(λx.f (x x))(λx. f (x x))

(define Y
  (lambda (f)
    ((lambda (g) (g g))
     (lambda (h)
       (f (lambda (x) ((h h) x)))))))

;; Example: factorial using Y
(define fact
  (Y (lambda (f)
       (lambda (n)
         (if (zero? n)
           1
           (* n (f (- n 1))))))))

(display (fact 5))  ; => 120
(newline)

;; Another example: Fibonacci
(define fib
  (Y (lambda (f)
       (lambda (n)
         (if (< n 2)
           n
           (+ (f (- n 1)) (f (- n 2))))))))

(display (fib 10))  ; => 55
(newline)




(display "hello, world")
(newline)
