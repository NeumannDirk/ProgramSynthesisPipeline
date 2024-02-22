# The last part of the example requires a QF_LIA solver to be installed.
#
#
# This example shows how to interact with files in the SMT-LIB
# format. In particular:
#
# 1. How to read a file in SMT-LIB format
# 2. How to write a file in SMT-LIB format
# 3. Formulas and SMT-LIB script
# 4. How to access annotations from SMT-LIB files
# 5. How to extend the parser with custom commands
#
from io import StringIO

from pysmt.smtlib.parser import SmtLibParser


# To make the example self contained, we store the example SMT-LIB
# script in a string.
DEMO_SMTLIB=\
"""
(set-logic QF_LIA)
(declare-fun p () Int)
(declare-fun q () Int)
(declare-fun x () Bool)
(declare-fun y () Bool)
(define-fun .def_1 () Bool (! (and x y) :cost 1))
(assert (=> x (> p q)))
(check-sat)
(push)
(assert (=> y (> q p)))
(check-sat)
(assert .def_1)
(check-sat)
(pop)
(check-sat)
"""

DEMO_SMTLIB=\
"""
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
(assert
  (forall
    ((t1 T) (t2 T))
    (!
      (=> (and (subtype t1 t2) (subtype t2 t1)) (= t1 t2))
      :pattern
      ((subtype t1 t2) (subtype t2 t1)))))
(assert
  (forall
    ((t1 T) (t2 T) (t3 T))
    (!
      (=> (and (subtype t1 t2) (subtype t2 t3)) (subtype t1 t3))
      :pattern
      ((subtype t1 t2) (subtype t2 t3)))))
(assert
  (forall
    ((u U) (t T))
    (!
      (= (instanceof u t) (subtype (typeof u) t))
      :pattern
      ((instanceof u t)))))
(assert
  (forall
    ((u U) (t T))
    (!
      (= (exactinstanceof u t) (= (typeof u) t))
      :pattern
      ((exactinstanceof u t)))))
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
(declare-fun k_null () U)
(declare-fun k_length (U) U)
(declare-const |field_java.lang.Object::<created>| U)
(declare-fun u_A_old () U)
(declare-fun k_wellFormed (U) Bool)
(declare-const sort_any T)
(declare-const sort_java.lang.Object T)
(declare-const |sort_int[]| T)
(declare-const sort_Null T)
(declare-const sort_Field T)
(declare-const sort_Heap T)
(assert
  (distinct
    sort_any
    sort_java.lang.Object
    sort_boolean
    |sort_int[]|
    sort_Null
    sort_Field
    sort_int
    sort_Heap))
; --- Axioms
(assert (instanceof (b2u true) sort_boolean))
(assert (instanceof (b2u false) sort_boolean))
(assert (forall ((b Bool)) (= (u2b (b2u b)) b)))
; This seems to improve Z3 performance: Needs investigation (probably triggers above)
(assert (not (u2b (b2u false))))
(assert
  (forall
    ((u U))
    (!
      (=>
        (= (typeof u) sort_boolean)
        (or (= u (b2u true)) (= u (b2u false))))
      :pattern
      ((typeof u)))))
(assert
  (forall
    ((x U))
    (!
      (=> (instanceof x sort_boolean) (= (typeof x) sort_boolean))
      :pattern
      ((instanceof x sort_boolean)))))
(assert (forall ((i Int)) (= (u2i (i2u i)) i)))
(assert
  (forall
    ((x U))
    (!
      (=> (= (typeof x) sort_int) (= (i2u (u2i x)) x))
      :pattern
      ((typeof x)))))
(assert
  (forall
    ((t T))
    (!
      (=> (subtype t sort_int) (= t sort_int))
      :pattern
      ((subtype t sort_int)))))
; (assert (forall ((x U)) (! (=> (instanceof x sort_int)  (= (typeof x ) sort_int)) :pattern ((instanceof x sort_int)))))
(assert
  (forall
    ((i Int))
    (! (= (typeof (i2u i)) sort_int) :pattern ((i2u i)))))
(assert (instanceof u_j sort_int))
(assert (instanceof u_heap sort_Heap))
(assert (instanceof u_A |sort_int[]|))
(assert
  (forall
    ((u U))
    (!
      (=> (>= (u2i u) 0) (= (fieldIdentifier (arr u)) (u2i u)))
      :pattern
      ((arr u)))))
(assert
  (forall
    ((u U))
    (! (exactinstanceof (arr u) sort_Field) :pattern ((arr u)))))
(assert (instanceof u_i sort_int))
(assert
  (forall
    ((x U) (t T))
    (! (subtype (typeof (cast x t)) t) :pattern ((cast x t)))))
(assert
  (forall
    ((x U) (t T))
    (! (=> (subtype (typeof x) t) (= (cast x t) x)) :pattern ((cast x t)))))
(assert (instanceof k_null sort_Null))
(assert
  (forall
    ((var_x U))
    (!
      (=>
        (instanceof var_x sort_any)
        (=> (= (b2u (instanceof var_x sort_Null)) (b2u true)) (= var_x k_null)))
      :pattern
      ((instanceof var_x sort_Null)))))
(assert
  (forall
    ((var_0 U))
    (! (instanceof (k_length var_0) sort_int) :pattern ((k_length var_0)))))
(assert
  (forall
    ((var_o U))
    (=>
      (instanceof var_o sort_java.lang.Object)
      (>= (u2i (k_length var_o)) 0))))
(assert (instanceof |field_java.lang.Object::<created>| sort_Field))
(assert (= (fieldIdentifier |field_java.lang.Object::<created>|) (- 2)))
(assert (instanceof u_A_old |sort_int[]|))
(assert
  (forall
    ((var_h U) (var_o U) (var_f U))
    (!
      (=>
        (and
          (instanceof var_h sort_Heap)
          (instanceof var_o sort_java.lang.Object)
          (instanceof var_f sort_Field))
        (=>
          (k_wellFormed var_h)
          (or
            (=
              (cast
                (k_select
                  var_h
                  (cast (k_select var_h var_o var_f) sort_java.lang.Object)
                  |field_java.lang.Object::<created>|)
                sort_boolean)
              (b2u true))
            (= (cast (k_select var_h var_o var_f) sort_java.lang.Object) k_null))))
      :pattern
      ((cast (k_select var_h var_o var_f) sort_java.lang.Object)))))
(assert (subtype sort_java.lang.Object sort_any))
(assert (not (subtype sort_java.lang.Object sort_boolean)))
(assert (not (subtype sort_java.lang.Object sort_Field)))
(assert (not (subtype sort_java.lang.Object sort_int)))
(assert (not (subtype sort_java.lang.Object sort_Heap)))
(assert (subtype sort_boolean sort_any))
(assert (not (subtype sort_boolean sort_java.lang.Object)))
(assert (not (subtype sort_boolean sort_Field)))
(assert (not (subtype sort_boolean sort_int)))
(assert (not (subtype sort_boolean sort_Heap)))
(assert (subtype sort_Field sort_any))
(assert (not (subtype sort_Field sort_java.lang.Object)))
(assert (not (subtype sort_Field sort_boolean)))
(assert (not (subtype sort_Field sort_int)))
(assert (not (subtype sort_Field sort_Heap)))
(assert (subtype sort_int sort_any))
(assert (not (subtype sort_int sort_java.lang.Object)))
(assert (not (subtype sort_int sort_boolean)))
(assert (not (subtype sort_int sort_Field)))
(assert (not (subtype sort_int sort_Heap)))
(assert (subtype sort_Heap sort_any))
(assert (not (subtype sort_Heap sort_java.lang.Object)))
(assert (not (subtype sort_Heap sort_boolean)))
(assert (not (subtype sort_Heap sort_Field)))
(assert (not (subtype sort_Heap sort_int)))
(assert (subtype |sort_int[]| sort_java.lang.Object))
(assert (subtype sort_Null sort_java.lang.Object))
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

(exit)
"""



# We read the SMT-LIB Script by creating a Parser.
# From here we can get the SMT-LIB script.
parser = SmtLibParser()

# The method SmtLibParser.get_script takes a buffer in input. We use
# StringIO to simulate an open file.
# See SmtLibParser.get_script_fname() if to pass the path of a file.
script = parser.get_script(StringIO(DEMO_SMTLIB))

# The SmtLibScript provides an iterable representation of the commands
# that are present in the SMT-LIB file.
#
# Printing a summary of the issued commands
#for cmd in script:
#    print(cmd.name)
#print("*"*50)

# SmtLibScript provides some utilities to perform common operations: e.g,
#
# - Checking if a command is present
#assert script.contains_command("check-sat")
# - Counting the occurrences of a command
#assert script.count_command_occurrences("assert") == 3
# - Obtain all commands of a particular type
decls = script.filter_by_command_name("assert")
for d in decls:
    print(d)
print("*"*50)

# Most SMT-LIB scripts define a single SAT call. In these cases, the
# result can be obtained by conjoining multiple assertions.  The
# method to do that is SmtLibScript.get_strict_formula() that, raises
# an exception if there are push/pop calls.  To obtain the formula at
# the end of the execution of the Script (accounting for push/pop) we
# use get_last_formula
#
f = script.get_last_formula()
print("f",f)

# Finally, we serialize the script back into SMT-Lib format.  This can
# be dumped into a file (see SmtLibScript.to_file).  The flag daggify,
# specifies whether the printing is done as a DAG or as a tree.

buf_out = StringIO()
script.serialize(buf_out, daggify=True)
print(buf_out.getvalue())

print("*"*50)
# Expressions can be annotated in order to provide additional
# information. The semantic of annotations is solver/problem
# dependent. For example, VMT uses annotations to identify two
# expressions as 1) the Transition Relation and 2) Initial Condition
#
# Here we pretend that we make up a ficticious Weighted SMT format
# and label .def1 with cost 1
#
# The class pysmt.smtlib.annotations.Annotations deals with the
# handling of annotations.
#
ann = script.annotations
print(ann.all_annotated_formulae("cost"))

print("*"*50)

# Annotations are part of the SMT-LIB standard, and are the
# recommended way to perform inter-operable operations. However, in
# many cases, we are interested in prototyping some algorithm/idea and
# need to write the input files by hand. In those cases, using an
# extended version of SMT-LIB usually provides a more readable input.
# We provide now an example on how to define a symbolic transition
# system as an extension of SMT-LIB.
# (A more complete version of this example can be found in :
#    pysmt.tests.smtlib.test_parser_extensibility.py)
#
EXT_SMTLIB="""\
(declare-fun A () Bool)
(declare-fun B () Bool)
(init (and A B))
(trans (=> A (next A)))
(exit)
"""