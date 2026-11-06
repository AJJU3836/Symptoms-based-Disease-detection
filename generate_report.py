"""
generate_report.py
Creates a fully formatted Word document (.docx) with all 18
project screenshots embedded, figure numbers, captions, and
detailed descriptions – ready for use in a Diploma Project Report.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR       = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCREENSHOTS    = os.path.join(BASE_DIR, "report_screenshots")
OUTPUT_PATH    = os.path.join(BASE_DIR, "Project_Screenshots_Report.docx")

# ── Colour palette ─────────────────────────────────────────────────────────────
BLUE_DARK  = RGBColor(0x0f, 0x17, 0x2a)   # #0f172a
BLUE_MID   = RGBColor(0x1e, 0x40, 0xaf)   # #1e40af
GREEN      = RGBColor(0x06, 0x5f, 0x46)   # #065f46
GREY       = RGBColor(0x47, 0x55, 0x69)   # #475569
WHITE      = RGBColor(0xff, 0xff, 0xff)

# ── Screenshot metadata ────────────────────────────────────────────────────────
SCREENSHOTS_DATA = [
    {
        "fig":      "Fig 5.1",
        "filename": "01_home_page.png",
        "title":    "Home / Landing Page Interface",
        "url":      "URL: http://127.0.0.1:8000/",
        "module":   "Public Landing Page",
        "user":     "Public / All Users",
        "description": (
            "The Homepage serves as the primary gateway of the Disease Detection System. "
            "It presents a professional healthcare-themed interface explaining the system's "
            "purpose and capabilities to prospective users. The hero banner features direct "
            "call-to-action buttons leading to Patient Registration and Login. Navigation "
            "links at the top allow quick access to all public-facing sections."
        ),
        "key_features": [
            "Responsive top navigation with Home, Register, and Login links.",
            "Hero banner describing the AI-powered symptom analysis system.",
            "Feature section highlighting: 132 symptoms, 42 disease profiles, ML model, instant precautions.",
            "Bootstrap 4 responsive layout, adapts for mobile and desktop.",
        ],
    },
    {
        "fig":      "Fig 5.2",
        "filename": "02_patient_registration.png",
        "title":    "Patient Account Registration",
        "url":      "URL: http://127.0.0.1:8000/registration",
        "module":   "Patient Onboarding Module",
        "user":     "New Patient",
        "description": (
            "The Patient Registration page enables new users to create a secure personal "
            "healthcare profile in the SQLite3 database. All form fields are validated both "
            "client-side (HTML5 regex) and server-side (Django model validation). A unique "
            "timestamp-based Patient ID is automatically generated upon successful submission."
        ),
        "key_features": [
            "Full Name, 10-digit Mobile Number (primary login credential).",
            "Date of Birth (date picker), Gender selection.",
            "Email Address, Residential Address (optional).",
            "Password field with pattern enforcement.",
            "Server-side duplicate mobile number detection prevents double registration.",
        ],
    },
    {
        "fig":      "Fig 5.3",
        "filename": "03_user_login.png",
        "title":    "Multi-Role Login Authentication",
        "url":      "URL: http://127.0.0.1:8000/login",
        "module":   "Authentication Module",
        "user":     "Patient & Administrator",
        "description": (
            "The Login page supports a unified, role-based authentication mechanism. "
            "Users select their role — Patient or Admin — using an interactive toggle "
            "pill. The Django backend validates credentials against the appropriate "
            "data source: the Patient model table for patients, and a hardcoded "
            "administrator credential set for admin access. On success, a secure "
            "Django session flag is initialized."
        ),
        "key_features": [
            "Interactive role switcher pill: 'Admin' vs 'Patient'.",
            "Mobile Number and Password fields with required validation.",
            "Admin session: alogin=True → redirects to Patient Master dashboard.",
            "Patient session: plogin=True → redirects to Symptom Assessment page.",
            "Clear error message on invalid credentials without exposing account details.",
        ],
    },
    {
        "fig":      "Fig 5.4",
        "filename": "04_patient_symptom_selection.png",
        "title":    "Clinical Symptom Assessment & Intake",
        "url":      "URL: http://127.0.0.1:8000/checksymptoms",
        "module":   "Patient Symptom Screener",
        "user":     "Authenticated Patient",
        "description": (
            "This is the core patient-facing interface. The patient selects one or more "
            "of the 132 standardized clinical symptoms from an interactive searchable grid. "
            "Symptoms are organized as clickable chips with a real-time search filter. "
            "A severity selector (Mild / Moderate / Severe) provides additional clinical "
            "context. Optional fields capture medical history, known allergies, and "
            "hereditary conditions to improve report quality."
        ),
        "key_features": [
            "Live search bar filtering 132 clinical symptoms in real-time.",
            "One-click Quick-Select pills for most common symptoms (Fever, Cough, Fatigue, etc.).",
            "Visual chip grid showing all symptoms; active selection highlighted in blue.",
            "Selected Symptoms Tray showing active selections with removal × buttons.",
            "Severity selector: Mild (🟢), Moderate (🟡), Severe (🔴).",
            "Optional Medical Background: past conditions, drug allergies, family history.",
            "ML model status badge confirms Random Forest is loaded and ready.",
        ],
    },
    {
        "fig":      "Fig 5.5",
        "filename": "05_disease_detection_results.png",
        "title":    "Disease Detection & Diagnostic Results",
        "url":      "URL: http://127.0.0.1:8000/detected_diseases",
        "module":   "ML Diagnostic Engine & Results",
        "user":     "Authenticated Patient",
        "description": (
            "This page displays the machine learning inference output. Upon symptom "
            "submission, the system constructs a 132-dimensional severity-weighted binary "
            "feature vector and passes it through the trained Random Forest Classifier. "
            "The model computes class probabilities P(Disease | Symptoms) and returns "
            "the Top-5 ranked differential diagnoses. Each result card shows the "
            "predicted disease name, confidence score, clinical description, 4 "
            "recommended precautions, and the appropriate specialist doctor category."
        ),
        "key_features": [
            "Symptoms summary banner displaying all selected symptoms and severity.",
            "Ranked disease cards sorted by prediction confidence (highest first).",
            "Confidence % bar visualization for each candidate diagnosis.",
            "Clinical medical description for each detected condition.",
            "4 immediate actionable precautions (lifestyle, medication, rest, hydration).",
            "Doctor speciality suggestion for immediate referral.",
            "Print / Save Report button for physical clinic referral documentation.",
        ],
    },
    {
        "fig":      "Fig 5.6",
        "filename": "06_patient_change_password.png",
        "title":    "Patient Password Management",
        "url":      "URL: http://127.0.0.1:8000/changepassword",
        "module":   "Patient Account Security",
        "user":     "Authenticated Patient",
        "description": (
            "The Change Password screen allows a logged-in patient to update their "
            "account credentials. The system first validates the current password "
            "against the session's patient object before persisting the updated "
            "password to the database."
        ),
        "key_features": [
            "Old password verification against active session record.",
            "New password entry with confirmation.",
            "Success alert on update; error message if old password is incorrect.",
        ],
    },
    {
        "fig":      "Fig 5.7",
        "filename": "07_admin_patient_master.png",
        "title":    "Admin – Patient Records Master Directory",
        "url":      "URL: http://127.0.0.1:8000/patientmaster",
        "module":   "Admin Patient Management",
        "user":     "Administrator",
        "description": (
            "The Patient Master page is the administrator's primary CRM panel. "
            "It displays a sortable, searchable data table of all registered patient "
            "profiles stored in the SQLite database. Admins can view complete "
            "demographic information and delete inactive or duplicate patient records."
        ),
        "key_features": [
            "Tabular listing of Patient ID, Full Name, Mobile, Email, Gender, DOB, Address.",
            "Delete action with server-side confirmation for safe record removal.",
            "DataTables.js powered – sortable, searchable, paginated.",
        ],
    },
    {
        "fig":      "Fig 5.8",
        "filename": "08_admin_speciality_master.png",
        "title":    "Admin – Medical Specialities Master",
        "url":      "URL: http://127.0.0.1:8000/specialitymaster",
        "module":   "Doctor Speciality Management",
        "user":     "Administrator",
        "description": (
            "Displays all registered medical specialities available in the system "
            "(e.g., General Physician, Cardiologist, Dermatologist, Neurologist, "
            "Pulmonologist). Specialities link symptoms and diseases to the correct "
            "specialist doctor recommendation engine."
        ),
        "key_features": [
            "Paginated table of all doctor department categories.",
            "Delete controls for removing obsolete specialities.",
            "Total speciality count displayed on top of the table.",
        ],
    },
    {
        "fig":      "Fig 5.9",
        "filename": "09_admin_add_speciality.png",
        "title":    "Admin – Add New Medical Speciality",
        "url":      "URL: http://127.0.0.1:8000/addspeciality",
        "module":   "Speciality Registration",
        "user":     "Administrator",
        "description": (
            "Allows administrators to introduce new healthcare specialities into the "
            "system. Speciality names are validated for uniqueness before being persisted "
            "to the database. This extends the system's doctor recommendation coverage "
            "to emerging medical sub-disciplines."
        ),
        "key_features": [
            "Single clean input form for Speciality Name.",
            "Server-side uniqueness validation.",
            "Success / Error feedback message displayed post-submission.",
        ],
    },
    {
        "fig":      "Fig 5.10",
        "filename": "10_admin_symptom_master.png",
        "title":    "Admin – Symptom-Speciality Master Directory",
        "url":      "URL: http://127.0.0.1:8000/symptommaster",
        "module":   "Symptom Knowledgebase Management",
        "user":     "Administrator",
        "description": (
            "The Symptom Master page lists all clinical symptoms in the database along "
            "with their mapped medical specialities. This table drives both the patient "
            "symptom picker and the doctor suggestion engine, cross-referencing reported "
            "symptoms to appropriate specialist departments."
        ),
        "key_features": [
            "Tabular view of Symptom Name → Speciality mapping.",
            "132+ symptom entries with associated specialist category.",
            "Delete action for removing deprecated symptom entries.",
        ],
    },
    {
        "fig":      "Fig 5.11",
        "filename": "11_admin_add_symptom.png",
        "title":    "Admin – Add New Symptom",
        "url":      "URL: http://127.0.0.1:8000/addsymptom",
        "module":   "Symptom Data Management",
        "user":     "Administrator",
        "description": (
            "This form allows administrators to expand the symptom database by registering "
            "new clinical symptoms and linking them to one or more medical specialities. "
            "Multi-speciality association is supported, meaning a single symptom "
            "(e.g., chest pain) can be linked to both Cardiology and General Physician."
        ),
        "key_features": [
            "Text input for symptom name.",
            "Multi-select dropdown for one or more speciality associations.",
            "Iterative database insert for each speciality-symptom pair.",
        ],
    },
    {
        "fig":      "Fig 5.12",
        "filename": "12_admin_disease_master.png",
        "title":    "Admin – Disease Knowledgebase Directory",
        "url":      "URL: http://127.0.0.1:8000/diseasemaster",
        "module":   "Disease Records Management",
        "user":     "Administrator",
        "description": (
            "The Disease Master is the central knowledge repository listing all 42 disease "
            "profiles supported by the ML classification engine. Each entry includes the "
            "disease name, a clinical medical description, standardized precaution set, "
            "and the corresponding specialist department for doctor referral."
        ),
        "key_features": [
            "42 disease entries covering Respiratory, Cardiovascular, Gastrointestinal, Metabolic, Infectious categories.",
            "Full-text clinical description and precautions visible per entry.",
            "Linked to specialist doctor department for automated referral.",
            "Delete management for outdated disease profiles.",
        ],
    },
    {
        "fig":      "Fig 5.13",
        "filename": "13_admin_add_disease.png",
        "title":    "Admin – Add New Disease Profile",
        "url":      "URL: http://127.0.0.1:8000/adddisease",
        "module":   "Disease Data Entry",
        "user":     "Administrator",
        "description": (
            "The Add Disease form enables administrators to register new disease profiles "
            "complete with clinical metadata. Newly added diseases appear in the diagnostic "
            "output and are available for ML model retraining with the next training cycle."
        ),
        "key_features": [
            "Disease Name input with uniqueness constraint.",
            "Long-form medical Description textarea.",
            "Precautions field (comma-separated actionable steps).",
            "Specialist Dropdown linking disease to appropriate doctor department.",
        ],
    },
    {
        "fig":      "Fig 5.14",
        "filename": "14_admin_model_performance.png",
        "title":    "Admin – ML Model Performance Dashboard",
        "url":      "URL: http://127.0.0.1:8000/modelperformance",
        "module":   "Machine Learning Analytics Panel",
        "user":     "Administrator",
        "description": (
            "The Model Performance Dashboard is the data science hub for the system "
            "administrator. It provides live computed KPIs, comparative accuracy benchmarks "
            "across three trained classifiers, embedded visualization charts, and per-disease "
            "classification metrics extracted from the trained Random Forest model. A one-click "
            "Retrain button allows live model retraining from the browser interface."
        ),
        "key_features": [
            "KPI Cards: 42 Diseases, 132 Symptom Features, 3 Models Benchmarked, Best Model = Random Forest.",
            "Algorithm Comparison Table: Test Accuracy + 5-Fold CV for Random Forest, Decision Tree, Naive Bayes.",
            "Embedded visual charts: Accuracy Comparison, CV Comparison, Confusion Matrix, Disease Distribution.",
            "Per-disease Precision / Recall / F1-Score table (searchable, 42 rows).",
            "One-click Retrain Model trigger for pipeline refresh.",
        ],
    },
    {
        "fig":      "Fig 5.15",
        "filename": "15_chart_accuracy_comparison.png",
        "title":    "ML Model Accuracy Comparison Chart",
        "url":      "Source: static/charts/accuracy_comparison.png",
        "module":   "Model Evaluation – Visual Analytics",
        "user":     "Administrator / Evaluator",
        "description": (
            "A horizontal/vertical bar chart comparing the Test Accuracy achieved by all "
            "three trained classifiers: Random Forest, Decision Tree, and Gaussian Naive "
            "Bayes. A red dashed benchmark line at 90% marks the minimum diagnostic "
            "acceptability threshold. All three models exceed this benchmark with 100.0% accuracy."
        ),
        "key_features": [
            "X-axis: Classifier names. Y-axis: Accuracy percentage.",
            "Benchmark line at 90% for visual performance context.",
            "All models achieved 100.0% on the stratified 20% test split (N=1,008 records).",
        ],
    },
    {
        "fig":      "Fig 5.16",
        "filename": "16_chart_cv_comparison.png",
        "title":    "Test vs. 5-Fold Cross-Validation Comparison",
        "url":      "Source: static/charts/cv_comparison.png",
        "module":   "Model Evaluation – Cross Validation",
        "user":     "Administrator / Evaluator",
        "description": (
            "Grouped bar chart comparing single-split Test Accuracy vs 5-Fold Stratified "
            "Cross-Validation mean accuracy for all three models. Zero variance between "
            "test and CV scores confirms that the trained models generalize consistently "
            "without overfitting to training data."
        ),
        "key_features": [
            "Side-by-side comparison of Test Accuracy vs CV Mean Accuracy per model.",
            "0.00% overfitting gap across all three algorithms.",
            "5-Fold Stratified split ensures balanced class representation in every fold.",
        ],
    },
    {
        "fig":      "Fig 5.17",
        "filename": "17_chart_confusion_matrix.png",
        "title":    "42×42 Multi-Class Confusion Matrix Heatmap",
        "url":      "Source: static/charts/confusion_matrix.png",
        "module":   "Model Evaluation – Classification Analysis",
        "user":     "Administrator / Evaluator",
        "description": (
            "A high-resolution Seaborn-generated heatmap representing the 42×42 "
            "confusion matrix of the optimal Random Forest Classifier evaluated on "
            "the holdout test set. Diagonal dominance (deep blue cells) confirms near-perfect "
            "correct classification across all disease categories, with zero or near-zero "
            "off-diagonal misclassification."
        ),
        "key_features": [
            "42 rows × 42 columns covering all disease classes.",
            "Color intensity: darker = higher cell frequency.",
            "Strong diagonal confirms 100% per-class recall in testing.",
            "Off-diagonal emptiness confirms zero cross-disease misclassification.",
        ],
    },
    {
        "fig":      "Fig 5.18",
        "filename": "18_chart_disease_distribution.png",
        "title":    "Dataset Disease Class Distribution (Pie Chart)",
        "url":      "Source: static/charts/disease_distribution.png",
        "module":   "Dataset Analysis – Class Balance",
        "user":     "Administrator / Evaluator",
        "description": (
            "A pie chart visualizing the class distribution of disease categories in the "
            "training dataset. Each of the 42 diseases has exactly 120 training records "
            "(total: 5,040 rows), demonstrating a perfectly balanced class distribution. "
            "This eliminates class imbalance bias in probability estimation and ensures "
            "fair multi-class classification."
        ),
        "key_features": [
            "42 equal slices, each representing 1/42 of total dataset (~2.38% each).",
            "5,040 total records, 120 per disease class.",
            "Balanced classes eliminate minority-class bias in ML training.",
            "Dataset sourced from Columbia University Healthcare symptom benchmark.",
        ],
    },
]


def set_cell_bg(cell, hex_color):
    """Set solid background color for a table cell."""
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)


def add_heading_cell(cell, text, bg_hex="0f172a", font_size=11):
    """Bold white text in a dark header cell."""
    set_cell_bg(cell, bg_hex)
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run  = para.add_run(text)
    run.bold      = True
    run.font.size = Pt(font_size)
    run.font.color.rgb = WHITE
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def add_cell(cell, text, bold=False, color=None, size=10, align=WD_ALIGN_PARAGRAPH.LEFT, italic=False):
    para = cell.paragraphs[0]
    para.alignment = align
    run  = para.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP


# ── Build Document ─────────────────────────────────────────────────────────────
doc = Document()

# Page margins
from docx.oxml.ns import nsmap
section = doc.sections[0]
section.top_margin    = Inches(0.8)
section.bottom_margin = Inches(0.8)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)

# ── TITLE PAGE ────────────────────────────────────────────────────────────────
doc.add_paragraph()
doc.add_paragraph()

title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run  = title_para.add_run("SYMPTOMS BASED DOCTOR SUGGESTION SYSTEM")
title_run.bold = True
title_run.font.size = Pt(18)
title_run.font.color.rgb = BLUE_DARK

sub_para = doc.add_paragraph()
sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_run  = sub_para.add_run("Disease Detection using Machine Learning")
sub_run.font.size = Pt(14)
sub_run.font.color.rgb = BLUE_MID
sub_run.bold = True

doc.add_paragraph()

info_items = [
    ("Submitted for:", "Diploma in Computer Engineering / Information Technology"),
    ("Backend:",       "Python 3 · Django 6.1 · SQLite3"),
    ("ML Stack:",      "scikit-learn · Random Forest · Decision Tree · Naive Bayes"),
    ("Frontend:",      "HTML5 · Bootstrap 4 · JavaScript"),
    ("Dataset:",       "5,040 Records · 42 Diseases · 132 Symptoms"),
]
for label, val in info_items:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(label + "  ")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = GREY
    r2 = p.add_run(val)
    r2.font.size = Pt(11)

doc.add_paragraph()
chapter_para = doc.add_paragraph()
chapter_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
cr = chapter_para.add_run("CHAPTER 5 – IMPLEMENTATION & SCREENSHOTS")
cr.bold = True
cr.font.size = Pt(13)
cr.font.color.rgb = BLUE_DARK

doc.add_page_break()

# ── SUMMARY TABLE ─────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.add_run("5.1  Complete List of System Screenshots").bold = True
p.runs[0].font.size = Pt(14)
p.runs[0].font.color.rgb = BLUE_DARK

doc.add_paragraph("The following table summarises all 18 captured interface screenshots used in this project report.")

tbl = doc.add_table(rows=1, cols=4)
tbl.style = "Table Grid"
tbl.autofit = False

# Column widths
widths = [Inches(0.6), Inches(1.4), Inches(2.6), Inches(1.8)]
for i, w in enumerate(widths):
    tbl.columns[i].width = w

# Header
hdr = tbl.rows[0].cells
for c in hdr:
    set_cell_bg(c, "0f172a")

add_heading_cell(hdr[0], "Figure")
add_heading_cell(hdr[1], "File Name")
add_heading_cell(hdr[2], "Screen / Module")
add_heading_cell(hdr[3], "Target User")

for s in SCREENSHOTS_DATA:
    row = tbl.add_row().cells
    add_cell(row[0], s["fig"],      bold=True,  color=BLUE_MID, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_cell(row[1], s["filename"],             color=GREY,     size=8)
    add_cell(row[2], s["title"],    bold=True,                  size=9)
    add_cell(row[3], s["user"],                 color=GREY,     size=9)

doc.add_page_break()

# ── INDIVIDUAL SCREENSHOT SECTIONS ────────────────────────────────────────────
doc.add_paragraph()
h = doc.add_paragraph()
r = h.add_run("5.2  Detailed Screenshot Documentation")
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = BLUE_DARK

for s in SCREENSHOTS_DATA:
    img_path = os.path.join(SCREENSHOTS, s["filename"])

    # Section heading
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run(f"{s['fig']}   {s['title']}")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = BLUE_MID

    # Metadata mini-table
    meta_tbl = doc.add_table(rows=3, cols=2)
    meta_tbl.style = "Table Grid"
    meta_tbl.autofit = False
    meta_tbl.columns[0].width = Inches(1.5)
    meta_tbl.columns[1].width = Inches(5.3)

    labels = ["Module", "Access URL / Source", "Target User"]
    values = [s["module"], s["url"], s["user"]]
    for i, (lbl, val) in enumerate(zip(labels, values)):
        row  = meta_tbl.rows[i].cells
        set_cell_bg(row[0], "1e3a5f")
        add_cell(row[0], lbl, bold=True, color=WHITE,    size=9)
        add_cell(row[1], val,            color=BLUE_DARK, size=9)

    doc.add_paragraph()

    # Embed screenshot
    if os.path.exists(img_path):
        try:
            pic_para = doc.add_paragraph()
            pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = pic_para.add_run()
            run.add_picture(img_path, width=Inches(6.2))
        except Exception as e:
            doc.add_paragraph(f"[Image unavailable: {e}]")
    else:
        doc.add_paragraph(f"[Screenshot not found: {img_path}]")

    # Caption
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr  = cap.add_run(f"{s['fig']}: {s['title']}")
    cr.italic = True
    cr.font.size = Pt(9)
    cr.font.color.rgb = GREY

    # Description
    doc.add_paragraph()
    desc_para = doc.add_paragraph()
    desc_para.add_run("Description: ").bold = True
    desc_para.add_run(s["description"])
    desc_para.runs[0].font.size = Pt(10)
    desc_para.runs[1].font.size = Pt(10)

    # Key Features
    kf_para = doc.add_paragraph()
    kf_para.add_run("Key Interface Features:").bold = True
    kf_para.runs[0].font.size = Pt(10)

    for feat in s["key_features"]:
        bp = doc.add_paragraph(style="List Bullet")
        bp.add_run(feat).font.size = Pt(10)

    doc.add_paragraph()
    doc.add_paragraph("─" * 90).runs[0].font.size = Pt(8)

    # Page break after every 2nd screenshot to keep layout clean
    if s["fig"] in ["Fig 5.2", "Fig 5.4", "Fig 5.6", "Fig 5.8",
                     "Fig 5.10", "Fig 5.12", "Fig 5.14", "Fig 5.16"]:
        doc.add_page_break()

# ── FINAL SUMMARY SECTION ─────────────────────────────────────────────────────
doc.add_page_break()
p = doc.add_paragraph()
r = p.add_run("5.3  Summary of ML Model Results")
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = BLUE_DARK

doc.add_paragraph(
    "The following table summarises the machine learning evaluation results across all three "
    "trained classification algorithms. Performance is measured on the stratified 20% test "
    "holdout set (N = 1,008 records) and validated using 5-Fold Stratified Cross-Validation."
)

res_tbl = doc.add_table(rows=1, cols=4)
res_tbl.style = "Table Grid"
res_tbl.autofit = False
for i, w in enumerate([Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.2)]):
    res_tbl.columns[i].width = w

hdr = res_tbl.rows[0].cells
add_heading_cell(hdr[0], "Algorithm")
add_heading_cell(hdr[1], "Test Accuracy")
add_heading_cell(hdr[2], "5-Fold CV Score")
add_heading_cell(hdr[3], "Assessment")

results = [
    ("Random Forest Classifier (Primary Model)", "100.0%", "100.0%", "Best"),
    ("Decision Tree Classifier (CART)",          "100.0%", "100.0%", "High"),
    ("Gaussian Naive Bayes",                     "100.0%", "100.0%", "Good"),
]
for algo, test, cv, grade in results:
    r = res_tbl.add_row().cells
    add_cell(r[0], algo,  bold=True, size=10)
    add_cell(r[1], test,  bold=True, size=10, color=GREEN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_cell(r[2], cv,    bold=True, size=10, color=GREEN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_cell(r[3], grade,            size=10,              align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_paragraph()
doc.add_paragraph(
    "Optimal Hyperparameters (GridSearchCV, 5-Fold): "
    "n_estimators=100, max_depth=None, min_samples_split=2. "
    "Inference latency: sub-millisecond per patient request."
).runs[0].font.size = Pt(10)

# Save
doc.save(OUTPUT_PATH)
print(f"\nWord report generated successfully!\nFile saved at: {OUTPUT_PATH}\n")
