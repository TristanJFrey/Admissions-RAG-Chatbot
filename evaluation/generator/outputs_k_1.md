## Q: 1 - 6

# Results

Q7: Vague reply to general vague question; uses correct chunk
Q8: FAISS Precise reply; uses correct chunk / Hybrid fails?
Q9: Precise reply; uses correct chunk / FAISS quotes the wrong chunk however so the generator likely hallucinated its citation but still had the correct information
Q10: Precise reply; uses correct chunk

=== Answer-Level Evaluation ===
Questions : 6
Hybrid BERTScore : mean F1 0.8829
FAISS BERTScore : mean F1 0.8789
Hybrid hallucinations (citation missing/out-of-pool): 1/6
FAISS hallucinations (citation missing/out-of-pool): 3/6

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
1 | 0.8816 | 0.8428 | N | Y
2 | 0.8633 | 0.8262 | N | Y
3 | 0.9029 | 0.9001 | N | N
4 | 0.9138 | 0.9149 | N | N
5 | 0.8790 | 0.8772 | N | Y
6 | 0.8569 | 0.9124 | Y | N

=== Generated Answers ===

Q1: When is the deadline for first years applicants at Miami University?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For first-year applicants, Miami University uses several deadlines depending on the application type. Early Decision and Early Action I have a November 1 deadline, Early Action II is due December 1, and Regular Decision applications are due February 1. Spring admission also has a December 1 deadline.
FAISS ans : The undergraduate application deadline at Miami University is December 1st [admissions.md-4-chunk-00004].
Hybrid ans : For first-year applicants at Miami University, the deadline for Early Action II and for spring admission is December 1st. [admissions.md-5-chunk-00005]

Q2: What are the requirements to apply for graduate admission?
Gold chunk : admissions.md-9-chunk-00009
Gold answer: Graduate applicants must hold a bachelor’s degree from an accredited institution and apply through the Graduate School. Programs may require additional materials such as GRE/GMAT scores, recommendations, portfolios, a CV, or supplemental documents. English-proficiency is required for international applicants.
FAISS ans : I do not have information about the requirements for graduate admission. [admissions.md-2-chunk-00002]
Hybrid ans : To apply for graduate admission, you'll need a bachelor's degree from an accredited institution and admission to the Graduate School, though specific programs might have additional requirements [admissions.md-9-chunk-00009].

Q3: What are the requirements to apply for transfer undergraduate admission?
Gold chunk : admissions.md-6-chunk-00006
Gold answer: Transfer applicants should be in good academic standing, have a high school diploma, and typically a college GPA of 2.0 or higher, though some programs may set higher standards. They may apply through the Common App (Transfer) or Miami’s own transfer application.
FAISS ans : To apply for transfer undergraduate admission, you generally need to be in good academic standing with a high school diploma and a college GPA of at least 2.0, though specific programs might have different expectations [admissions.md-6-chunk-00006].
Hybrid ans : To apply for transfer undergraduate admission, you'll need to have good academic standing, a high school diploma, and generally a college GPA of 2.0 or higher, though specific programs might have different expectations [admissions.md-6-chunk-00006].

Q4: Do first-year applicants need recommendation letters?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes, first-year applicants must submit at least one recommendation from a counselor or an academic teacher.
FAISS ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher. [admissions.md-3-chunk-00003]
Hybrid ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher [admissions.md-3-chunk-00003].

Q5: What is the spring semester application deadline for undergraduates?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For undergraduate spring admission, Miami University sets a December 1 application deadline, and decisions are released on a rolling basis.
FAISS ans : The spring semester application deadline for undergraduates is December 1st [admissions.md-4-chunk-00004].
Hybrid ans : The application deadline for the spring semester for undergraduates is December 1st [admissions.md-5-chunk-00005].

Q6: Is there a separate application for international undergraduate students?
Gold chunk : admissions.md-8-chunk-00008
Gold answer: Yes. International undergraduate applicants can apply through the Common Application or through the Miami International Application, which does not require an essay.
FAISS ans : International undergraduate students can use either the Common Application or the Miami International Application, which doesn't require an essay [admissions.md-8-chunk-00008].
Hybrid ans : There is no mention of a separate application for international undergraduate students in the provided context. [admissions.md-12-chunk-00012]

## Q: 7 - 10

# Results

Q7: Vague reply to general vague question; uses correct chunk
Q8: FAISS Precise reply; uses correct chunk / Hybrid fails?
Q9: Precise reply; uses correct chunk / FAISS quotes the wrong chunk however so the generator likely hallucinated its citation but still had the correct information
Q10: Precise reply; uses correct chunk

=== Answer-Level Evaluation ===
Questions : 4
Hybrid BERTScore : mean F1 0.9054
FAISS BERTScore : mean F1 0.9092
Hybrid hallucinations (citation missing/out-of-pool): 1/4
FAISS hallucinations (citation missing/out-of-pool): 2/4

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
7 | 0.9112 | 0.9102 | N | N
8 | 0.8820 | 0.9199 | Y | Y
9 | 0.8937 | 0.8743 | N | Y
10 | 0.9347 | 0.9324 | N | N

=== Generated Answers ===

Q7: What are the Early Decision and Early Action deadlines?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: Early Decision and Early Action I both have a November 1 application deadline. Early Action II has a December 1 deadline.
FAISS ans : The deadline to apply for Early Decision is November 1, and the deadline to apply for Early Action I is also November 1, while Early Action II has a deadline of December 1 [admissions.md-5-chunk-00005].
Hybrid ans : The Early Decision application deadline is November 1, and the Early Action I deadline is also November 1, while Early Action II has a deadline of December 1 [admissions.md-5-chunk-00005].

Q8: What application platforms can first-year students use?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year students may apply through the Common Application or the Coalition Application, depending on availability.
FAISS ans : First-year students can apply through the Common Application or the Coalition Application [admissions.md-2-chunk-00002].
Hybrid ans : I do not have information on the application platforms first-year students can use.

Q9: Is Miami University test-optional for first-year applicants?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes. Miami University is ACT/SAT test-optional for first-year applicants applying to the Oxford campus through Spring 2026.
FAISS ans : Miami University is test-optional for first-year applicants [admissions.md-0-chunk-00000].
Hybrid ans : Miami University is test-optional for first-year applicants through Spring 2026 [admissions.md-3-chunk-00003].

Q10: What materials do first-year applicants need to submit?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year applicants must submit a high school transcript (unofficial accepted initially), at least one counselor or teacher recommendation, and proof of English proficiency if they are not native English speakers.
FAISS ans : First-year applicants need to submit their high school transcript, at least one recommendation from a counselor or academic teacher, and proof of English proficiency if they are not native English speakers [admissions.md-3-chunk-00003].
Hybrid ans : First-year applicants need to submit a high school transcript, at least one recommendation from a counselor or academic teacher, and proof of English proficiency if they are not native English speakers [admissions.md-3-chunk-00003].
