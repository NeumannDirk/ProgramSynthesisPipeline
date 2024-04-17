(set-logic SLIA)

(declare-datatype Tuple ((mkTuple (getField0 (Seq Int)))))

(declare-const i_preCon Int)
(declare-const A_preCon Int)
(declare-const i_postCon Int)
(declare-const A_postCon Int)

(define-fun preCondition ((i_preCon Int) (A_preCon (Seq Int))) Bool 
(and
	(not (= A_preCon (as seq.empty (Seq Int))))
	(> i_preCon 0)
	(< i_preCon (str.len A_preCon))
	(= 5 (seq.nth A_preCon i_preCon))
))

(define-fun postCondition ((i_postCon Int) (A_postCon (Seq Int))) Bool 
(and
	(not (= A_postCon (as seq.empty (Seq Int))))
	(< i_postCon (str.len A_postCon))
	(= 6 (seq.nth A_postCon i_postCon))
))

(define-fun targetFunction ((i Int) (A (Seq Int))) Tuple
	(mkTuple (seq.update A i (seq.unit 6)))
)

(declare-const i_in Int)
(declare-const A_in (Seq Int))
(declare-const A_out (Seq Int))

(assert (not (forall ((i_in Int) (A_in (Seq Int)) (A_out (Seq Int))) (=>
	(and
		(preCondition i_in A_in)
		(= A_out (getField0 (targetFunction i_in A_in)))
	)
	(and
		(postCondition i_in A_out)
	)
))))
(check-sat)
(get-model)