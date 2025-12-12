## Q: 1-15

# Results

Q1: F correct content but wrong chunk/cite; H /
Q2: F wrong chunk and says can’t answer; H /
Q3: F /; H /
Q4: F /; H /
Q5: F correct content but wrong chunk/cite; H /
Q6: F /; H /
Q7: F /; H /
Q8: F correct content but wrong chunk/cite; H /
Q9: F correct content but wrong chunk/cite; H /
Q10: F /; H /
Q11: F wrong chunk and off-target (transfer table); H wrong chunk and off-target
Q12: F correct date but wrong chunk/cite; H correct date but wrong chunk/cite
Q13: F /; H /
Q14: F /; H /
Q15: F wrong chunk and says can’t answer; H /

=== Answer-Level Evaluation ===
Questions : 5
Hybrid BERTScore : mean F1 0.89898
FAISS BERTScore : mean F1 0.89561
Hybrid hallucinations (citation missing/out-of-pool): 2/15
FAISS hallucinations (citation missing/out-of-pool): 8/15

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
1 | 0.8825 | 0.8353 | N | Y
2 | 0.8623 | 0.8247 | N | Y
3 | 0.9029 | 0.8969 | N | N
4 | 0.9138 | 0.9149 | N | N
5 | 0.8756 | 0.8879 | N | Y
6 | 0.9124 | 0.9277 | N | N
7 | 0.8989 | 0.9015 | N | N
8 | 0.9237 | 0.9128 | N | Y
9 | 0.8952 | 0.8906 | N | Y
10 | 0.9292 | 0.9325 | N | N
11 | 0.8835 | 0.8908 | Y | Y
12 | 0.9222 | 0.9221 | Y | Y
13 | 0.8963 | 0.9005 | N | N
14 | 0.9136 | 0.9425 | N | N
15 | 0.8726 | 0.8535 | N | Y

=== Generated Answers ===

Q1: When is the deadline for first years applicants at Miami University?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For first-year applicants, Miami University uses several deadlines depending on the application type. Early Decision and Early Action I have a November 1 deadline, Early Action II is due December 1, and Regular Decision applications are due February 1. Spring admission also has a December 1 deadline.
FAISS ans : The undergraduate application deadline is December 1st [admissions.md-4-chunk-00004].
Hybrid ans : For first-year applicants at Miami University, the deadline for Early Action II and for Spring Admission is December 1st. [admissions.md-5-chunk-00005]

Q2: What are the requirements to apply for graduate admission?
Gold chunk : admissions.md-9-chunk-00009
Gold answer: Graduate applicants must hold a bachelor’s degree from an accredited institution and apply through the Graduate School. Programs may require additional materials such as GRE/GMAT scores, recommendations, portfolios, a CV, or supplemental documents. English-proficiency is required for international applicants.
FAISS ans : I cannot provide information about graduate admission requirements, as the context only details undergraduate admission. [admissions.md-2-chunk-00002]
Hybrid ans : To apply for graduate admission, you need a bachelor's degree from an accredited institution and admission to the Graduate School, though individual programs might have extra requirements [admissions.md-9-chunk-00009].

Q3: What are the requirements to apply for transfer undergraduate admission?
Gold chunk : admissions.md-6-chunk-00006
Gold answer: Transfer applicants should be in good academic standing, have a high school diploma, and typically a college GPA of 2.0 or higher, though some programs may set higher standards. They may apply through the Common App (Transfer) or Miami’s own transfer application.
FAISS ans : To apply for transfer undergraduate admission, you generally need to be in good academic standing with a high school diploma and a college GPA of at least 2.0, though specific program requirements may differ [admissions.md-6-chunk-00006].
Hybrid ans : To apply for transfer undergraduate admission, you generally need to be in good academic standing, have a high school diploma, and have a college GPA of at least 2.0, though specific programs might have different expectations [admissions.md-6-chunk-00006].

Q4: Do first-year applicants need recommendation letters?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes, first-year applicants must submit at least one recommendation from a counselor or an academic teacher.
FAISS ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher. [admissions.md-3-chunk-00003]
Hybrid ans : First-year applicants are required to submit at least one recommendation letter from a counselor or academic teacher [admissions.md-3-chunk-00003].

Q5: What is the spring semester application deadline for undergraduates?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For undergraduate spring admission, Miami University sets a December 1 application deadline, and decisions are released on a rolling basis.
FAISS ans : The undergraduate application deadline for the spring semester is December 1. [admissions.md-4-chunk-00004]
Hybrid ans : The application deadline for the spring semester is December 1st. [admissions.md-5-chunk-00005]

Q6: Is there a separate application for international undergraduate students?
Gold chunk : admissions.md-8-chunk-00008
Gold answer: Yes. International undergraduate applicants can apply through the Common Application or through the Miami International Application, which does not require an essay.
FAISS ans : Yes, international undergraduate students can apply through either the Common Application or the Miami International Application, which doesn't require an essay [admissions.md-8-chunk-00008].
Hybrid ans : International undergraduate students can use either the Common Application or the Miami International Application, which doesn't require an essay [admissions.md-8-chunk-00008].

Q7: What are the Early Decision and Early Action deadlines?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: Early Decision and Early Action I both have a November 1 application deadline. Early Action II has a December 1 deadline.
FAISS ans : The application deadline for Early Decision is November 1, for Early Action I it's also November 1, and for Early Action II it's December 1 [admissions.md-5-chunk-00005].
Hybrid ans : The Early Decision application deadline is November 1, Early Action I is November 1, and Early Action II is December 1. [admissions.md-5-chunk-00005]

Q8: What application platforms can first-year students use?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year students may apply through the Common Application or the Coalition Application, depending on availability.
FAISS ans : First-year students can use the Common Application or the Coalition Application for admission [admissions.md-2-chunk-00002].
Hybrid ans : First-year students can apply using either the Common Application or, if available, the Coalition Application. [admissions.md-3-chunk-00003]

Q9: Is Miami University test-optional for first-year applicants?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes. Miami University is ACT/SAT test-optional for first-year applicants applying to the Oxford campus through Spring 2026.
FAISS ans : Yes, Miami University is test-optional for first-year applicants [admissions.md-0-chunk-00000].
Hybrid ans : Miami University is test-optional for first-year applicants through the Spring 2026 term [admissions.md-3-chunk-00003].

Q10: What materials do first-year applicants need to submit?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year applicants must submit a high school transcript (unofficial accepted initially), at least one counselor or teacher recommendation, and proof of English proficiency if they are not native English speakers.
FAISS ans : First-year applicants are required to submit their high school transcript, at least one recommendation from a counselor or academic teacher, and proof of English proficiency if they are not native English speakers [admissions.md-3-chunk-00003].
Hybrid ans : First-year applicants are required to submit a high school transcript, at least one recommendation from a counselor or academic teacher, and English proficiency documentation if they are not native English speakers [admissions.md-3-chunk-00003].

Q11: What is the merit scholarship amount for a high school student with a 3.82 GPA and is an Ohio resident?
Gold chunk : admissions.md-15-chunk-00015
Gold answer: A high school student with a weighted GPA of 3.82 who is an Ohio resident falls within the 3.75–3.94 GPA range and is eligible for a merit scholarship starting at $4,000 per year.
FAISS ans : For a first-semester college student who is an Ohio resident with a 3.82 high school GPA, the merit scholarship amount is $4,000 annually [admissions.md-20-chunk-00020].
Hybrid ans : For a first-semester college student who is an Ohio resident and has a high school GPA of 3.5 or higher, the annual merit scholarship value is $4,000. [admissions.md-20-chunk-00020]

Q12: When is the priority application deadline for Miami's merit scholarships?
Gold chunk : admissions.md-14-chunk-00014
Gold answer: The priority application deadline for most of Miami University’s merit scholarships is December 1.
FAISS ans : The priority application deadline for most of Miami's merit scholarships is December 1st. [admissions.md-5-chunk-00005]
Hybrid ans : The priority application deadline for most of Miami's merit scholarships is December 1. [admissions.md-5-chunk-00005]

Q13: Who is eligible for the Partner Community College Scholarship?
Gold chunk : admissions.md-24-chunk-00024
Gold answer: Eligible students must be incoming transfer students who attended a Miami University partner community college full-time immediately before enrolling at Miami and who transfer directly from that institution.
FAISS ans : To be eligible for the Partner Community College Scholarship, you must be an incoming transfer student who has attended a partner community college full-time just before enrolling at Miami. [admissions.md-24-chunk-00024]
Hybrid ans : To be eligible for the Partner Community College Scholarship, you need to be an incoming transfer student who has attended a partner community college full-time right before starting at Miami [admissions.md-24-chunk-00024].

Q14: How is the Phi Theta Kappa Scholarship renewed?
Gold chunk : admissions.md-23-chunk-00023
Gold answer: The Phi Theta Kappa Scholarship is renewed by maintaining full-time enrollment on the Oxford campus and a minimum cumulative GPA of 3.0.
FAISS ans : The Phi Theta Kappa Scholarship is renewed by maintaining full-time enrollment at the Oxford campus and a 3.0 cumulative GPA. [admissions.md-23-chunk-00023]
Hybrid ans : To renew the Phi Theta Kappa Scholarship, you need to stay enrolled full-time at the Oxford campus and keep your cumulative GPA at 3.0 or higher [admissions.md-23-chunk-00023].

Q15: How do I apply for the International Education Scholarship?
Gold chunk : admissions.md-27-chunk-00027
Gold answer: There is no separate application for the International Education Scholarship. All new first-year international undergraduate students who submit a complete admission application and meet requirements are automatically considered, with priority given to those who apply by December 1.
FAISS ans : I don't have information on how to apply for the International Education Scholarship. [admissions.md-26-chunk-00026]
Hybrid ans : To apply for the International Education Scholarship, you simply need to submit your completed undergraduate application with all the necessary admission materials [admissions.md-27-chunk-00027].
