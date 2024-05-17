; --- Preamble
; BEGIN preamble from preamble.smt2

(set-option :print-success true)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(set-logic ALL)

(declare-sort T 0)
(declare-sort U 0)

(declare-fun instanceof (U T) Bool)
(declare-fun exactinstanceof (U T) Bool)
(declare-fun subtype (T T) Bool)
(declare-fun typeof (U) T)

(assert (forall ((t1 T)) (subtype t1 t1)))
(assert (forall ((t1 T) (t2 T)) (! (=> (and (subtype t1 t2) (subtype t2 t1)) (= t1 t2)) :pattern ((subtype t1 t2) (subtype t2 t1)))))
(assert (forall ((t1 T) (t2 T) (t3 T)) (! (=> (and (subtype t1 t2) (subtype t2 t3)) (subtype t1 t3)) :pattern ((subtype t1 t2) (subtype t2 t3)))))
(assert (forall ((u U) (t T)) (! (= (instanceof u t) (subtype (typeof u) t)) :pattern ((instanceof u t)))))
(assert (forall ((u U) (t T)) (! (= (exactinstanceof u t) (= (typeof u) t)) :pattern ((exactinstanceof u t)))))

; END preamble from preamble.smt2


; --- Declarations

(declare-fun u2b (U) Bool)
(declare-fun b2u (Bool) U)
(declare-const sort_boolean T)
    

(declare-fun u2i (U) Int)
(declare-fun i2u (Int) U)
(declare-const sort_int T)
    
(declare-fun u_x () U)
(declare-fun u_a () U)
(declare-fun u_b () U)
(declare-fun u_y () U)
(declare-fun u_c () U)
(declare-fun u_z () U)
(assert (distinct sort_boolean sort_int))

; --- Axioms

(assert (instanceof (b2u true) sort_boolean))
(assert (instanceof (b2u false) sort_boolean))
(assert (forall ((b Bool)) (= (u2b (b2u b)) b)))
; This seems to improve Z3 performance: Needs investigation (probably triggers above)
(assert (not (u2b (b2u false))))
(assert (forall ((u U)) (! (=> (= (typeof u) sort_boolean) (or (= u (b2u true)) (= u (b2u false)))) :pattern ((typeof u)))))
(assert (forall ((x U)) (! (=> (instanceof x sort_boolean)  (= (typeof x ) sort_boolean)) :pattern ((instanceof x sort_boolean)))))
    

(assert (forall ((i Int)) (= (u2i (i2u i)) i)))
(assert (forall ((x U)) (! (=> (= (typeof x) sort_int)  (= (i2u (u2i x)) x)) :pattern ((typeof x)))))
(assert (forall ((t T)) (! (=> (subtype t sort_int) (= t sort_int)) :pattern ((subtype t sort_int)))))
; (assert (forall ((x U)) (! (=> (instanceof x sort_int)  (= (typeof x ) sort_int)) :pattern ((instanceof x sort_int)))))
(assert (forall ((i Int)) (! (= (typeof (i2u i)) sort_int) :pattern ((i2u i)))))
    
(assert (instanceof u_x sort_int))
(assert (instanceof u_a sort_int))
(assert (instanceof u_b sort_int))
(assert (instanceof u_y sort_int))
(assert (instanceof u_c sort_int))
(assert (instanceof u_z sort_int))

; --- Sequent
(assert (not (and (and (= u_x (i2u (+ (u2i u_a) (u2i u_b)))) (= u_y (i2u (* 2 (u2i u_c))))) (= u_z (i2u (* 2 (u2i u_a)))))))

(check-sat)