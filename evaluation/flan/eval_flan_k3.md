## Q: 1-15

# Results

Q1: F correct but no citation; H correct but no citation.
Q2: F correct but no citation; H correct but no citation.
Q3: F correct; H correct but extra/off-topic text.
Q4: F correct; H wrong (hallucinates international GPA note).
Q5: F correct; H correct.
Q6: F correct but long; H wrong/URL, no citation.
Q7: F partial (EA I only); H partial (EA I only).
Q8: F correct content; H correct content.
Q9: F off-topic/adds fee waiver; H off-topic/adds fee waiver.
Q10: F wrong chunk/content; H wrong chunk/content.
Q11: F wrong amount; H wrong topic/chunk.
Q12: F correct; H correct.
Q13: F wrong topic (STEM programs); H wrong topic (STEM programs).
Q14: F wrong (transfer note); H wrong (transfer note).
Q15: F wrong (YouAreWelcomeHere); H wrong chunk/topic.

=== Answer-Level Evaluation ===
Questions : 15
Hybrid BERTScore : mean F1 0.8811
FAISS BERTScore : mean F1 0.8856
Hybrid hallucinations (citation missing/out-of-pool): 14/15
FAISS hallucinations (citation missing/out-of-pool): 13/15

ID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?
1 | 0.8449 | 0.8449 | Y | Y
2 | 0.8902 | 0.8902 | Y | Y
3 | 0.9247 | 0.9155 | Y | Y
4 | 0.8530 | 0.9402 | Y | Y
5 | 0.8783 | 0.8783 | Y | Y
6 | 0.8624 | 0.8617 | Y | N
7 | 0.8744 | 0.8744 | Y | Y
8 | 0.9543 | 0.9543 | Y | Y
9 | 0.8913 | 0.8913 | Y | Y
10 | 0.8907 | 0.8700 | Y | N
11 | 0.8478 | 0.9050 | Y | Y
12 | 0.9549 | 0.9549 | Y | Y
13 | 0.8348 | 0.8348 | Y | Y
14 | 0.8531 | 0.8531 | Y | Y
15 | 0.8612 | 0.8156 | N | Y

=== Generated Answers ===

Q1: When is the deadline for first years applicants at Miami University?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For first-year applicants, Miami University uses several deadlines depending on the application type. Early Decision and Early Action I have a November 1 deadline, Early Action II is due December 1, and Regular Decision applications are due February 1. Spring admission also has a December 1 deadline.
FAISS ans : Dec. 1
Hybrid ans : Dec. 1

Q2: What are the requirements to apply for graduate admission?
Gold chunk : admissions.md-9-chunk-00009
Gold answer: Graduate applicants must hold a bachelor’s degree from an accredited institution and apply through the Graduate School. Programs may require additional materials such as GRE/GMAT scores, recommendations, portfolios, a CV, or supplemental documents. English-proficiency is required for international applicants.
FAISS ans : Bachelor’s degree from an accredited institution; Graduate School admission required; programs may add requirements
Hybrid ans : Bachelor’s degree from an accredited institution; Graduate School admission required; programs may add requirements

Q3: What are the requirements to apply for transfer undergraduate admission?
Gold chunk : admissions.md-6-chunk-00006
Gold answer: Transfer applicants should be in good academic standing, have a high school diploma, and typically a college GPA of 2.0 or higher, though some programs may set higher standards. They may apply through the Common App (Transfer) or Miami’s own transfer application.
FAISS ans : Good academic standing; HS diploma required; 2.0+ college GPA generally expected (programs may vary)
Hybrid ans : Good academic standing; HS diploma required; 2.0+ college GPA generally expected (programs may vary) Application Platforms: Common App (Transfer); Miami Transfer Application (no essay)

Q4: Do first-year applicants need recommendation letters?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes, first-year applicants must submit at least one recommendation from a counselor or an academic teacher.
FAISS ans : At least one counselor or academic teacher recommendation
Hybrid ans : First-year international students with a U.S. equivalent GPA of 3.5+ who meet admission requirements are automatically considered.

Q5: What is the spring semester application deadline for undergraduates?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: For undergraduate spring admission, Miami University sets a December 1 application deadline, and decisions are released on a rolling basis.
FAISS ans : Dec. 1
Hybrid ans : Dec. 1

Q6: Is there a separate application for international undergraduate students?
Gold chunk : admissions.md-8-chunk-00008
Gold answer: Yes. International undergraduate applicants can apply through the Common Application or through the Miami International Application, which does not require an essay.
FAISS ans : [admissions.md-8-chunk-00008] ## 2.3 International Undergraduate Admission Application Platforms: Common Application; Miami International Application (no essay) Application Fee: $70 (may be waived via “Miami Fee Waiver” if selected by Dec
Hybrid ans : International Apply: https://miamioh.edu/admission-aid/apply/international-students/index.html

Q7: What are the Early Decision and Early Action deadlines?
Gold chunk : admissions.md-5-chunk-00005
Gold answer: Early Decision and Early Action I both have a November 1 application deadline. Early Action II has a December 1 deadline.
FAISS ans : Early Action I: Apply by Nov 1 Decision by Dec 15
Hybrid ans : Early Action I: Apply by Nov 1 Decision by Dec 15

Q8: What application platforms can first-year students use?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year students may apply through the Common Application or the Coalition Application, depending on availability.
FAISS ans : Common Application; Coalition Application (where available)
Hybrid ans : Common Application; Coalition Application (where available)

Q9: Is Miami University test-optional for first-year applicants?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: Yes. Miami University is ACT/SAT test-optional for first-year applicants applying to the Oxford campus through Spring 2026.
FAISS ans : ACT/SAT optional for Oxford through Spring 2026; superscoring considered if multiple test dates submitted Application Fee: $50 (fee waiver available if selecting “Miami Fee Waiver” by Dec 1)
Hybrid ans : ACT/SAT optional for Oxford through Spring 2026; superscoring considered if multiple test dates submitted Application Fee: $50 (fee waiver available if selecting “Miami Fee Waiver” by Dec 1)

Q10: What materials do first-year applicants need to submit?
Gold chunk : admissions.md-3-chunk-00003
Gold answer: First-year applicants must submit a high school transcript (unofficial accepted initially), at least one counselor or teacher recommendation, and proof of English proficiency if they are not native English speakers.
FAISS ans : [admissions.md-3-chunk-00003] ## 2.1 First-Year (Freshman) Admission Application Platforms: Common Application; Coalition Application (where available) Test Policy: ACT/SAT optional for Oxford through Spring 2026; superscoring considered
Hybrid ans : High school transcript (unofficial accepted at time of application) - At least one counselor or academic teacher recommendation - English proficiency for non-native English speakers (international applicants) --- [admissions.md-28-chunk-00028]

Q11: What is the merit scholarship amount for a high school student with a 3.82 GPA and is an Ohio resident?
Gold chunk : admissions.md-15-chunk-00015
Gold answer: A high school student with a weighted GPA of 3.82 who is an Ohio resident falls within the 3.75–3.94 GPA range and is eligible for a merit scholarship starting at $4,000 per year.
FAISS ans : $8,000
Hybrid ans : 9.2 University Merit Scholarship - Eligibility - Merit scholarships are available to qualified high school students enrolling full-time on the Oxford campus.

Q12: When is the priority application deadline for Miami's merit scholarships?
Gold chunk : admissions.md-14-chunk-00014
Gold answer: The priority application deadline for most of Miami University’s merit scholarships is December 1.
FAISS ans : Dec. 1
Hybrid ans : Dec. 1

Q13: Who is eligible for the Partner Community College Scholarship?
Gold chunk : admissions.md-24-chunk-00024
Gold answer: Eligible students must be incoming transfer students who attended a Miami University partner community college full-time immediately before enrolling at Miami and who transfer directly from that institution.
FAISS ans : students pursuing STEM degrees, engineering, data and science fields, and health sciences.
Hybrid ans : students pursuing STEM degrees, engineering, data and science fields, and health sciences.

Q14: How is the Phi Theta Kappa Scholarship renewed?
Gold chunk : admissions.md-23-chunk-00023
Gold answer: The Phi Theta Kappa Scholarship is renewed by maintaining full-time enrollment on the Oxford campus and a minimum cumulative GPA of 3.0.
FAISS ans : if the student is admitted as a transfer
Hybrid ans : if the student is admitted as a transfer

Q15: How do I apply for the International Education Scholarship?
Gold chunk : admissions.md-27-chunk-00027
Gold answer: There is no separate application for the International Education Scholarship. All new first-year international undergraduate students who submit a complete admission application and meet requirements are automatically considered, with priority given to those who apply by December 1.
FAISS ans : YouAreWelcomeHere application
Hybrid ans : [admissions.md-27-chunk-00027] ## 9.1 International Education Scholarship - Eligibility - Scholarships are based on academic records and other information provided at the time of application.
