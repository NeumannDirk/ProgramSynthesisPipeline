from FormulaTree import *
from smtTreeParser import *
from generateSygusProblem import generate_sygus_problem

INPUT = """
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
      (k_wellFormed u_heap))
"""

INPUT2 = """
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
            (<= (u2i u_j) (u2i (k_length u_A))))"""


INPUT3 = """
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
                        (and
                          (and
                            (and
                              (and
                                (and
                                  (forall
                                    ((var_q Int))
                                    (=>
                                      (and (>= var_q 0) (< var_q 0))
                                      (= (cast (k_select u_heap u_A (arr (i2u var_q))) sort_int) (i2u 0))))
                                  (forall
                                    ((var_q Int))
                                    (=>
                                      (and (>= var_q 0) (< var_q 0))
                                      (= (cast (k_select u_heap u_A (arr (i2u var_q))) sort_int) (i2u 1)))))
                                (forall
                                  ((var_q Int))
                                  (=>
                                    (and (>= var_q (u2i (k_length u_A))) (< var_q (u2i (k_length u_A))))
                                    (= (cast (k_select u_heap u_A (arr (i2u var_q))) sort_int) (i2u 2)))))
                              (<= 0 0))
                            (<= 0 (u2i (k_length u_A))))
                          (<= (u2i (k_length u_A)) (u2i (k_length u_A))))
                        (not (= u_A k_null)))
                      (> (u2i (k_length u_A)) 0))
                    (<= 0 (u2i u_wb)))
                  (<= (u2i u_wb) (u2i u_wt)))
                (<= (u2i u_wt) (u2i u_bb)))
              (<= (u2i u_bb) (u2i (k_length u_A))))
            (forall
              ((var_i Int))
              (=>
                (and (>= var_i 0) (< var_i (u2i (k_length u_A))))
                (or
                  (or
                    (= (cast (k_select u_heap u_A (arr (i2u var_i))) sort_int) (i2u 0))
                    (= (cast (k_select u_heap u_A (arr (i2u var_i))) sort_int) (i2u 1)))
                  (= (cast (k_select u_heap u_A (arr (i2u var_i))) sort_int) (i2u 2))))))
          (=
            (cast (k_select u_heap u_A |field_java.lang.Object::<created>|) sort_boolean)
            (b2u true)))
        (=
          (cast
            (k_select u_heap u_A_old |field_java.lang.Object::<created>|)
            sort_boolean)
          (b2u true)))
      (k_wellFormed u_heap))"""


if __name__ == "__main__":
    # print("Hallo")
    tree = parse_smt_to_tree(INPUT3)
    # print(tree.toString())
    cleaned_tree = cleanup_tree_from_smt(tree)
    back_to_smt = print_tree_to_sygus(cleaned_tree).replace("u_", "")

    print("\nsmt condition:\n", back_to_smt)

    variables = [("j", True, "int"), ("i", True, "int"), ("A", False, "int[]")]
    parsed_pre_cond = [back_to_smt]
    parsed_post_cond = [back_to_smt]
    sygus_problem = generate_sygus_problem(variables, parsed_pre_cond, parsed_post_cond)

    sygus_file = "sygus_gen.sy"
    with open("D:\\" + sygus_file, "w") as output_file:
        output_file.write(sygus_problem)

    print("\nsygus problem:\n", sygus_problem)

    # "k_null" should be translated


# (and (and (and (and (and (and (and (and (and (and (forall ( (var_q Int)) (=> (and (>= var_q 0)
# (< var_q (+ u_j 1))) (>= (k_select u_heap u_A (arr u_i)) (k_select u_heap u_A (arr var_q))))) (not (= u_A k_null))) (> (seq.len u_A)
# 0)) (< (seq.len u_A) 10)) (>= u_i 0)) (< u_i (seq.len u_A))) (>= u_j 0)) (<= u_j (seq.len u_A))))))
