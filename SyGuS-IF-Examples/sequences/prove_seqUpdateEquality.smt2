(set-logic SLIA)

(define-fun seqUpdate ((s (Seq Int)) (i Int) (val Int)) (Seq Int)
    (seq.++ (seq.extract s 0 i) (seq.unit val) (seq.extract s (+ i 1) (- (seq.len s) i 1)))
)

;(declare-const index Int)
;(declare-const value Int)
;(declare-const arr (Seq Int))
;(assert (forall ((index Int) (value Int) (arr (Seq Int))) 
;(=
;(seqUpdate arr index value)
;(seq.++ (seq.extract arr 0 index) (seq.unit value) (seq.extract arr (+ index 1) (- (seq.len arr) index 1)))
;)))

(declare-const alter_at Int)
(declare-const set_value Int)
(declare-const arr_in (Seq Int))
(assert (not (= arr_in (as seq.empty (Seq Int)))))
(assert (not (forall ((alter_at Int) (check_at Int) (set_value Int) (arr_in (Seq Int)))
	
	(= 
		(seq.update arr_in alter_at (seq.unit set_value))
		(seqUpdate arr_in alter_at set_value)
	)
	
)))
(check-sat)
(get-model)