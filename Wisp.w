(func add a b (+ a b))
(func f n (if (eq n 0) 1 (* n (f (- n 1))) ))


;Comment
(f 170)
;Comment
