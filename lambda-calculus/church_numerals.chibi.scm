(import (scheme base)
        (scheme write))

(define zero (lambda (f) (lambda (x) x)))

(define one  (lambda (f) (lambda (x) (f x))))
(define two  (lambda (f) (lambda (x) (f (f x)))))
(define three (lambda (f) (lambda (x) (f (f (f x))))))

(define (church->int n)
  ((n (lambda (i) (+ i 1))) 0))

(define (int->church n)
  (if (zero? n)
    zero
    (lambda (f)
      (lambda (x)
        (f (((int->church (- n 1)) f) x))))))


;; SUCC = λn.λf.λx. f (n f x)
(define succ
  (lambda (n)
    (lambda (f)
      (lambda (x) 
        (f ((n f) x))))))

;; PLUS = λm.λn.λf.λx. m f (n f x)
(define plus
  (lambda (m)
    (lambda (n)
      (lambda (f) 
        (lambda (x) 
          ((m f) ((n f) x)))))))

;; MULT = λm.λn.λf. m (n f)
(define mult
  (lambda (m)
    (lambda (n)
      (lambda (f) (m (n f))))))

;; POW = λm.λn. n m
(define pow
  (lambda (m)
    (lambda (n) (n m))))

;; ========== 辅助函数：前驱与判零（可选，用于阶乘）==========
;; ISZERO = λn. n (λx. false) true
(define (is-zero? n)
  ((n (lambda (_) #f)) #t))

;;  PRED（使用 pair 编码，标准算法）
(define pred
  (lambda (n)
    (let ((shift (lambda (p)
                   (cons (cdr p) (succ (cdr p))))))
      (car ((n shift) (cons zero zero))))))

;; 为方便使用，将上述 lambda 风格转为 Scheme 函数（语法糖）
(define (add m n) ((plus m) n))
(define (mul m n) ((mult m) n))
(define (expt m n) ((pow m) n))

;; define Y-combinator
(define Y
  (lambda (f)
    ((lambda (g) (g g))
     (lambda (h)
       (f (lambda (x) ((h h) x)))))))

;; 
(define fact-church
  (Y (lambda (f)
       (lambda (n)
         (if (is-zero? n)
           one
           (mul n (f (pred n))))))))

;; ==========  Test and Println ==========
(display "=== Church Numerals Demo ===\n")

(display "Church 3  = ") (display (church->int three)) (newline)  ; => 3

(define church-2 (int->church 2))
(define church-3 (int->church 3))
(display "Church 2 succ = ") (display (church->int (succ two))) (newline)  ; => 3
(display "Church 3 succ = ") (display (church->int church-3)) (newline)  ; => 3
(display "Church 2 succ = ") (display (church->int (succ (int->church 2)))) (newline)  ; => 3

(display "2 + 3 = ") (display (church->int (add church-2 church-3))) (newline)  ; => 5
(display "2 + 3 = ") (display (church->int ((plus church-2) church-3))) (newline)  ; => 5

(display "2 * 3 = ") (display (church->int (mul church-2 church-3))) (newline)  ; => 6
(display "2 ^ 3 = ") (display (church->int (expt church-2 church-3))) (newline) ; => 8

;; 3. Test pow（使用 Church 数字）
(define church-5 (int->church 5))
(define church-fact5 (fact-church church-5))
(display "5! = ") (display (church->int church-fact5)) (newline)  ; => 120

;; 4. Test  pred and is-zero?
(display "Pred(1) = ") (display (church->int (pred one))) (newline)    ; => 0
(display "Is zero? (zero) = ") (display (is-zero? zero)) (newline)     ; => #t
(display "Is zero? (two)  = ") (display (is-zero? two)) (newline)      ; => #f
