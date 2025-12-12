## Q: 1 - 3

# Results

Q1: Vague reply to general vague question; uses correct chunk
Q2: Precise reply; uses correct chunk
Q3: Precise reply; uses correct chunk

=== Answer-Level Evaluation ===
Questions : 3
Hybrid BERTScore : mean F1 0.8805
FAISS BERTScore : mean F1 0.8830
Hybrid hallucinations (citation missing/out-of-pool): 0/3
FAISS hallucinations (citation missing/out-of-pool): 0/3

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
1 | 0.8742 | 0.8808 | N | N
2 | 0.8626 | 0.8633 | N | N
3 | 0.9047 | 0.9048 | N | N

=== Generated Answers ===

Q1: When is the deadline for first years applicants at Miami University?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For first-year applicants, Miami University uses several deadlines depending on the application type. Early Decision and Early Action I have a November 1 deadline, Early Action II is due December 1, and Regular Decision applications are due February 1. Spring admission also has a December 1 deadline.
FAISS ans : The application deadline for first-year applicants for Early Action II is December 1st, and for Regular Decision, it's February 1st [admissions.md-5-chunk-00005].  
Hybrid ans : For first-year applicants at Miami University, the Early Action II deadline is December 1st [admissions.md-5-chunk-00005].

Q2: What are the requirements to apply for graduate admission?
Gold chunk : admissions.md-9-chunk-00009
Gold answer: Graduate applicants must hold a bachelor’s degree from an accredited institution and apply through the Graduate School. Programs may require additional materials such as GRE/GMAT scores, recommendations, portfolios, a CV, or supplemental documents. English-proficiency is required for international applicants.
FAISS ans : To apply for graduate admission, you'll need a bachelor's degree from an accredited institution and admission to the Graduate School, though specific programs might have additional requirements [admissions.md-9-chunk-00009].
Hybrid ans : To apply for graduate admission, you'll need a bachelor's degree from an accredited institution and to be admitted by the Graduate School, though specific programs might have additional requirements [admissions.md-9-chunk-00009].

Q3: What are the requirements to apply for transfer undergraduate admission?
Gold chunk : admissions.md-6-chunk-00006
Gold answer: Transfer applicants should be in good academic standing, have a high school diploma, and typically a college GPA of 2.0 or higher, though some programs may set higher standards. They may apply through the Common App (Transfer) or Miami’s own transfer application.
FAISS ans : To apply for transfer undergraduate admission, you generally need to be in good academic standing with a high school diploma and a college GPA of 2.0 or higher, though specific programs might have different expectations [admissions.md-6-chunk-00006].
Hybrid ans : To apply for transfer undergraduate admission, you need to be in good academic standing, have a high school diploma, and generally maintain a college GPA of 2.0 or higher, although specific programs might have different expectations [admissions.md-6-chunk-00006].

## Q: 4 - 6

# Results

Q4: Precise reply; uses correct chunk
Q5: Precise reply; uses correct chunk
Q6: Precise reply; uses correct chunk

=== Answer-Level Evaluation ===
Questions : 3
Hybrid BERTScore : mean F1 0.8955
FAISS BERTScore : mean F1 0.8933
Hybrid hallucinations (citation missing/out-of-pool): 0/3
FAISS hallucinations (citation missing/out-of-pool): 0/3

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
4 | 0.9138 | 0.9138 | N | N
5 | 0.8815 | 0.8741 | N | N
6 | 0.8911 | 0.8920 | N | N

=== Generated Answers ===

Q4: Do first-year applicants need recommendation letters?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes, first-year applicants must submit at least one recommendation from a counselor or an academic teacher.
FAISS ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher [admissions.md-3-chunk-00003].
Hybrid ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher [admissions.md-3-chunk-00003].

Q5: What is the spring semester application deadline for undergraduates?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For undergraduate spring admission, Miami University sets a December 1 application deadline, and decisions are released on a rolling basis.
FAISS ans : The application deadline for the spring semester is December 1st [admissions.md-5-chunk-00005].
Hybrid ans : The application deadline for the spring semester for undergraduates is December 1. [admissions.md-5-chunk-00005]

Q6: Is there a separate application for international undergraduate students?
Gold chunk : admissions.md-8-chunk-00008
Gold answer: Yes. International undergraduate applicants can apply through the Common Application or through the Miami International Application, which does not require an essay.  
FAISS ans : International undergraduate students can apply through either the Common Application or the Miami International Application [admissions.md-8-chunk-00008].
Hybrid ans : International undergraduate students can apply using either the Common Application or the Miami International Application [admissions.md-8-chunk-00008].

## Q: 7 - 10

# Results

Q7: ?
Q8: Precise reply; uses correct chunk
Q9: Precise reply; uses correct chunk
Q10: Precise reply; uses correct chunk

=== Answer-Level Evaluation ===
Questions : 4
Hybrid BERTScore : mean F1 0.9153
FAISS BERTScore : mean F1 0.9059
Hybrid hallucinations (citation missing/out-of-pool): 0/4
FAISS hallucinations (citation missing/out-of-pool): 0/4

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
7 | 0.9129 | 0.8693 | N | N
8 | 0.9228 | 0.9228 | N | N
9 | 0.8937 | 0.8990 | N | N
10 | 0.9316 | 0.9325 | N | N

=== Generated Answers ===

Q7: What are the Early Decision and Early Action deadlines?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: Early Decision and Early Action I both have a November 1 application deadline. Early Action II has a December 1 deadline.
FAISS ans : The Early Decision application deadline is November 1, with decisions expected by December 1 [admissions.md-5-chunk-00005].
Hybrid ans : The application deadline for Early Decision is November 1, and for Early Action I it is also November 1, with Early Action II having a deadline of December 1. [admissions.md-5-chunk-00005]

Q8: What application platforms can first-year students use?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year students may apply through the Common Application or the Coalition Application, depending on availability.
FAISS ans : First-year students can apply using either the Common Application or the Coalition Application. [admissions.md-3-chunk-00003]
Hybrid ans : First-year students can apply using either the Common Application or the Coalition Application. [admissions.md-3-chunk-00003]

Q9: Is Miami University test-optional for first-year applicants?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes. Miami University is ACT/SAT test-optional for first-year applicants applying to the Oxford campus through Spring 2026.
FAISS ans : Miami University is test-optional for first-year applicants through the Spring 2026 term for their Oxford campus [admissions.md-3-chunk-00003].
Hybrid ans : Miami University is test-optional for first-year applicants through Spring 2026 [admissions.md-3-chunk-00003].

Q10: What materials do first-year applicants need to submit?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year applicants must submit a high school transcript (unofficial accepted initially), at least one counselor or teacher recommendation, and proof of English proficiency if they are not native English speakers.
FAISS ans : First-year applicants are required to submit their high school transcript, at least one recommendation from a counselor or academic teacher, and proof of English proficiency if they are not native English speakers [admissions.md-3-chunk-00003].
Hybrid ans : First-year applicants need to submit their high school transcript, at least one recommendation from a counselor or academic teacher, and proof of English proficiency if
they are non-native English speakers [admissions.md-3-chunk-00003].
