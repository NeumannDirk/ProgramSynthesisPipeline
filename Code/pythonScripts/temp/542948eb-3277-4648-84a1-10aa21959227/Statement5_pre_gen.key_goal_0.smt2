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
    
(declare-fun u_maxi (U U U U) Bool)
(declare-fun u_A () U)
(declare-fun u_j () U)
(declare-fun u_i () U)
(declare-fun k_null () U)
(declare-fun k_length (U) U)
(declare-fun k_select (U U U) U)
(declare-fun u_heap () U)
(declare-fun fieldIdentifier (U) Int)
(declare-const |field_java.lang.Object::<created>| U)
(declare-fun cast (U T) U)
(declare-fun u_A_old () U)
(declare-fun k_wellFormed (U) Bool)
(declare-const sort_Null T)
(declare-const sort_any T)
(declare-const sort_Field T)
(declare-const sort_java.lang.Object T)
(declare-const sort_Heap T)
(declare-const |sort_int[]| T)
(assert (distinct sort_Null sort_any sort_Field sort_int sort_boolean sort_java.lang.Object sort_Heap |sort_int[]|))

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
    
(assert (instanceof u_A |sort_int[]|))
(assert (instanceof u_j sort_int))
(assert (instanceof u_i sort_int))
(assert (instanceof k_null sort_Null))
(assert (forall ((var_x U)) (! (=> (instanceof var_x sort_any) (=> (= (b2u (instanceof var_x sort_Null)) (b2u true)) (= var_x k_null))) :pattern ((instanceof var_x sort_Null)))))
(assert (forall ((var_0 U)) (! (instanceof (k_length var_0) sort_int) :pattern ((k_length var_0)))))
(assert (forall ((var_o U)) (=> (instanceof var_o sort_java.lang.Object) (>= (u2i (k_length var_o)) 0))))
(assert (instanceof u_heap sort_Heap))
(assert (instanceof |field_java.lang.Object::<created>| sort_Field))
(assert (= (fieldIdentifier |field_java.lang.Object::<created>|) (- 2)))

(assert (forall ((x U) (t T)) (! (subtype (typeof (cast x t)) t) :pattern ((cast x t)))))
(assert (forall ((x U) (t T)) (! (=> (subtype (typeof x) t) (= (cast x t) x)) :pattern ((cast x t)))))
    
(assert (instanceof u_A_old |sort_int[]|))
(assert (forall ((var_h U) (var_o U) (var_f U)) (! (=> (and (instanceof var_h sort_Heap) (instanceof var_o sort_java.lang.Object) (instanceof var_f sort_Field)) (=> (k_wellFormed var_h) (or (= (cast (k_select var_h (cast (k_select var_h var_o var_f) sort_java.lang.Object) |field_java.lang.Object::<created>|) sort_boolean) (b2u true)) (= (cast (k_select var_h var_o var_f) sort_java.lang.Object) k_null)))) :pattern ((cast (k_select var_h var_o var_f) sort_java.lang.Object)))))
(assert (subtype sort_Field sort_any))
(assert (not (subtype sort_Field sort_int)))
(assert (not (subtype sort_Field sort_boolean)))
(assert (not (subtype sort_Field sort_java.lang.Object)))
(assert (not (subtype sort_Field sort_Heap)))
(assert (subtype sort_int sort_any))
(assert (not (subtype sort_int sort_Field)))
(assert (not (subtype sort_int sort_boolean)))
(assert (not (subtype sort_int sort_java.lang.Object)))
(assert (not (subtype sort_int sort_Heap)))
(assert (subtype sort_boolean sort_any))
(assert (not (subtype sort_boolean sort_Field)))
(assert (not (subtype sort_boolean sort_int)))
(assert (not (subtype sort_boolean sort_java.lang.Object)))
(assert (not (subtype sort_boolean sort_Heap)))
(assert (subtype sort_java.lang.Object sort_any))
(assert (not (subtype sort_java.lang.Object sort_Field)))
(assert (not (subtype sort_java.lang.Object sort_int)))
(assert (not (subtype sort_java.lang.Object sort_boolean)))
(assert (not (subtype sort_java.lang.Object sort_Heap)))
(assert (subtype sort_Heap sort_any))
(assert (not (subtype sort_Heap sort_Field)))
(assert (not (subtype sort_Heap sort_int)))
(assert (not (subtype sort_Heap sort_boolean)))
(assert (not (subtype sort_Heap sort_java.lang.Object)))
(assert (subtype sort_Null sort_java.lang.Object))
(assert (subtype |sort_int[]| sort_java.lang.Object))
(assert (subtype sort_Null |sort_int[]|))

; --- Sequent
(assert
  (not
    (and
      (and
        (and
          (and
            (and
              (and
                (and
                  (and
                    (and
                      (and
                        (forall
                          ((var_q Int))
                          (=>
                            (and (>= var_q 0) (< var_q (+ (u2i u_j) 1)))
                            (>=
                              (u2i (cast (k_select u_heap u_A (arr u_i)) sort_int))
                              (u2i (cast (k_select u_heap u_A (arr (i2u var_q))) sort_int)))))
                        (not (= u_A k_null)))
                      (> (u2i (k_length u_A)) 0))
                    (< (u2i (k_length u_A)) 10))
                  (>= (u2i u_i) 0))
                (< (u2i u_i) (u2i (k_length u_A))))
              (>= (u2i u_j) 0))
            (<= (u2i u_j) (u2i (k_length u_A))))
          (=
            (cast (k_select u_heap u_A |field_java.lang.Object::<created>|) sort_boolean)
            (b2u true)))
        (=
          (cast
            (k_select u_heap u_A_old |field_java.lang.Object::<created>|)
            sort_boolean)
          (b2u true)))
      (k_wellFormed u_heap))))

(check-sat)