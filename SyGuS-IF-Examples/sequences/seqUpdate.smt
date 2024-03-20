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
(declare-const check_at Int)
(declare-const set_value Int)
(declare-const arr_in (Seq Int))
(declare-const arr_out (Seq Int))
(assert (forall ((alter_at Int) (check_at Int) (set_value Int) (arr_in (Seq Int)) (arr_out (Seq Int))) 
(=>
	(and
		;not empty sequence
		(not (= arr_in (as seq.empty (Seq Int))))
		(> (seq.len arr_in) 0)
		;valid indeces		
		(<= 0 alter_at)
		(< alter_at (seq.len arr_in))
		(<= 0 check_at)		
		(< check_at (seq.len arr_in))
		;define output
		(= arr_out (seqUpdate arr_in alter_at set_value))
	)
	(and
		(= (seq.len arr_in) (seq.len arr_out))
		(=> 
			(= check_at alter_at) 
			(= set_value (seq.nth arr_out check_at))
		)
		(=> 
			(not (= check_at alter_at)) 
			(= (seq.nth arr_in check_at) (seq.nth arr_out check_at))
		)
	)
)))
(check-sat)
(get-model)