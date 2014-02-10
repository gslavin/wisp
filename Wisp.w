(func add a b (+ a b))
(add (add 1 3) 2)

(func f n (if (eq n 0) 1 (* n (f (- n 1))) ))
(f 170)