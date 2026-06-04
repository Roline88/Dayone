App name: DayOne D1 



Goal:

Design a tablet app for community health workers supporting pregnant women using an at-home maternal health kit. The health worker may have limited medical training, so the app must be extremely simple, visual, guided, and easy to use. The app helps the worker manage patient records, guide each test, save results, and understand when monitoring or referral is needed.



Visual style:

Use soft, reassuring colors: warm beige or off-white background, pastel blue and green accents, coral/orange for warnings, and red only for urgent alerts. Use large buttons, simple icons, clear spacing, and minimal text. The design should feel friendly, safe, and professional, not too clinical.



Main navigation:

Bottom navigation bar with 4 tabs:

Home

Patients

Tests

Alerts



Page 1: Landing page / Patient dashboard



The first screen shows a list of pregnant patients followed by the health worker.



Top section:

Welcome message: “Good morning”

Search bar: “Search patient”

Large button: “+ Add new patient”



Patient cards:

Each patient appears as a simple card with:

Patient name

Age

Gestational week

Village/address

Health status color:

Green = stable

Orange = needs monitoring

Red = needs intervention

Next test needed

Last visit date



Example card:

Amina Diallo

24 years old · 22 weeks pregnant

Status: Orange — Monitor closely

Next test: Blood pressure today

Last visit: 2 days ago



Add patient button:

When clicked, opens a simple form:

Full name

Age

Phone number

Address/location

Emergency contact

Estimated start of pregnancy

Estimated due date

Previous pregnancy complications

Known conditions

Assigned health worker

Notes



Page 2: Patient profile page



When the health worker clicks on a patient, the patient profile opens.



Top patient info section:

Name

Age

Address

Phone number

Emergency contact

Gestational age

Estimated due date

Start of pregnancy

Risk level

Last visit

Notes



Below that, show a “Today’s action” card:

Example:

“Blood pressure and urine protein should be checked today.”



Health status summary:

Use four large test cards:



1. Blood pressure

   Device: Cradle BP monitor

   Purpose: Hypertension / preeclampsia risk

   Show:

   Latest result

   Mini graph of recent results

   Comparison graph with safe, warning, and danger zones

   Status color

   Button: “Open BP test”



2. Iron / anemia

   Test: Iron or hemoglobin test

   Purpose: Anemia screening

   Show:

   Latest result

   Mini trend graph

   Comparison with normal vs low range

   Status color

   Button: “Open anemia test”



3. Glucose

   Test: Blood glucose test

   Purpose: Gestational diabetes screening

   Show:

   Latest result

   Mini trend graph

   Comparison with normal vs high range

   Status color

   Button: “Open glucose test”



4. Urine protein

   Test: Urine dipstick / protein test

   Purpose: Preeclampsia and kidney warning signs

   Show:

   Latest result

   Mini trend graph

   Comparison with negative, trace, +, ++, +++

   Status color

   Button: “Open urine test”



Recommendation section:

Show a clear recommendation card:

Green: “All good — continue routine monitoring.”

Orange: “Needs monitoring — repeat test and follow up.”

Red: “Needs intervention — refer to clinic or supervisor.”



Also include:

“Call supervisor” button

“Create referral note” button

“Add visit notes” button



Page 3: Individual test page



Each test has its own page with the same simple structure.



Example: Blood Pressure Test Page



Top:

Patient name

Test name: Blood Pressure

Last result

Current status



Schedule section:

Show when this test should be done:

Last completed: May 12

Next due: Today

Frequency: Every visit / as recommended



Step-by-step checklist:

Use large checkboxes:

Wash hands

Explain the test to the patient

Ask the patient to sit and rest

Place the device correctly

Start the test

Take a photo of the result or connect device

Confirm the result

Save result



Result input:

Photo recognition button:

“Take photo of result”

Manual backup entry:

Systolic BP

Diastolic BP

Heart rate

Symptoms:

Headache

Swelling

Dizziness

Blurred vision

Other notes



Interpretation section:

The app shows a simple message:

Green: “Result looks normal.”

Orange: “Repeat or monitor closely.”

Red: “Possible risk — contact supervisor or refer.”



Recommendation:

The app should clearly explain the next action:

“Continue routine follow-up”

“Repeat test in 30 minutes”

“Schedule another visit”

“Refer patient to clinic”

“Call emergency contact/supervisor”



History section:

A table or timeline showing:

Date

Result

Status

Action taken

Notes

Photo attached



The same structure should be repeated for:

Iron/anemia test

Glucose test

Urine protein test



Page 4: Alerts page



This page shows only patients who need attention.



Alert cards:

Patient name

Alert type

Test result

Risk color

Recommended action

Button: “Open patient”



Examples:

Red alert:

“High blood pressure + urine protein detected. Refer to clinic.”



Orange alert:

“Low iron detected. Monitor and follow up.”



Page 5: Records page



This page keeps a complete history of all visits and tests.



Filters:

Patient

Date

Test type

Status



Each record includes:

Patient name

Test performed

Result

Photo

Recommendation

Health worker name

Date and time

Notes



Important UX details:

Use simple language, not medical jargon.

Use icons for each test.

Use color-coded results.

Use large buttons for tablet use.

Always show the next step clearly.

Never show too much information at once.

Include confirmation messages like “Result saved successfully.”

Include offline mode indicator in case the health worker has poor internet.

Include a sync button: “Sync records when connected.”



Overall prototype flow:

Landing page → Select patient → Patient profile → Select test → Guided checklist → Add/photo result → Automatic interpretation → Save record → Recommendation/referral if needed.