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
    
(declare-fun u_j () U)
(declare-fun k_select (U U U) U)
(declare-fun u_heap () U)
(declare-fun u_A () U)
(declare-fun arr (U) U)
(declare-fun fieldIdentifier (U) Int)
(declare-fun u_i () U)
(declare-fun cast (U T) U)
(declare-const sort_Heap T)
(declare-const |sort_int[]| T)
(declare-const sort_Field T)
(assert (distinct sort_Heap |sort_int[]| sort_boolean sort_Field sort_int))

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
    
(assert (instanceof u_j sort_int))
(assert (instanceof u_heap sort_Heap))
(assert (instanceof u_A |sort_int[]|))

        (assert (forall ((u U)) (!
            (=> (>= (u2i u) 0) (= (fieldIdentifier (arr u)) (u2i u)))
            :pattern ((arr u)))))
        (assert (forall ((u U)) (! (exactinstanceof (arr u) sort_Field) :pattern ((arr u)))) )
    
(assert (instanceof u_i sort_int))

(assert (forall ((x U) (t T)) (! (subtype (typeof (cast x t)) t) :pattern ((cast x t)))))
(assert (forall ((x U) (t T)) (! (=> (subtype (typeof x) t) (= (cast x t) x)) :pattern ((cast x t)))))
    

; --- Sequent
(assert (not (forall ((var_q Int)) (or (not (and (>= var_q 0) (< var_q (+ (u2i u_j) 1)))) (>= (u2i (cast (k_select u_heap u_A (arr u_i)) sort_int)) (u2i (cast (k_select u_heap u_A (arr (i2u var_q))) sort_int)))))))

(check-sat)