"""
Script to create the symptom-disease dataset.
This generates a comprehensive dataset with 42 diseases and 132 symptoms.
Run once: python app/ml/create_dataset.py
"""
import pandas as pd
import os

BASE = os.path.dirname(__file__)

# ── 1. DISEASE -> SYMPTOMS MAPPING ──────────────────────────────────────────
disease_symptom_map = {
    "Fungal infection":       ["itching","skin_rash","nodal_skin_eruptions","dischromic_patches"],
    "Allergy":                ["continuous_sneezing","shivering","chills","watering_from_eyes"],
    "GERD":                   ["stomach_pain","acidity","ulcers_on_tongue","vomiting","cough","chest_pain"],
    "Chronic cholestasis":    ["itching","vomiting","yellowish_skin","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes"],
    "Drug Reaction":          ["itching","skin_rash","stomach_pain","burning_micturition","spotting_urination"],
    "Peptic ulcer disease":   ["vomiting","indigestion","loss_of_appetite","abdominal_pain","passage_of_gases","internal_itching"],
    "AIDS":                   ["muscle_wasting","patches_in_throat","high_fever","extra_marital_contacts"],
    "Diabetes":               ["fatigue","weight_loss","restlessness","lethargy","irregular_sugar_level","blurred_and_distorted_vision","obesity","excessive_hunger","increased_appetite","polyuria"],
    "Gastroenteritis":        ["vomiting","sunken_eyes","dehydration","diarrhoea"],
    "Bronchial Asthma":       ["fatigue","cough","high_fever","breathlessness","family_history","mucoid_sputum"],
    "Hypertension":           ["headache","chest_pain","dizziness","loss_of_balance","lack_of_concentration"],
    "Migraine":               ["acidity","indigestion","headache","blurred_and_distorted_vision","excessive_hunger","stiff_neck","depression","irritability","visual_disturbances"],
    "Cervical spondylosis":   ["back_pain","weakness_in_limbs","neck_pain","dizziness","loss_of_balance"],
    "Paralysis (brain hemorrhage)": ["vomiting","headache","weakness_of_one_body_side","altered_sensorium"],
    "Jaundice":               ["itching","vomiting","fatigue","weight_loss","high_fever","yellowish_skin","dark_urine","abdominal_pain"],
    "Malaria":                ["chills","vomiting","high_fever","sweating","headache","nausea","diarrhoea","muscle_pain"],
    "Chicken pox":            ["itching","skin_rash","fatigue","lethargy","high_fever","headache","loss_of_appetite","mild_fever","swelled_lymph_nodes","malaise","red_spots_over_body"],
    "Dengue":                 ["skin_rash","chills","joint_pain","vomiting","fatigue","high_fever","headache","nausea","loss_of_appetite","pain_behind_the_eyes","back_pain","malaise","muscle_pain","red_spots_over_body"],
    "Typhoid":                ["chills","vomiting","fatigue","high_fever","headache","nausea","constipation","abdominal_pain","diarrhoea","toxic_look_(typhos)","belly_pain"],
    "Hepatitis A":            ["joint_pain","vomiting","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","diarrhoea","mild_fever","yellowing_of_eyes","muscle_pain"],
    "Hepatitis B":            ["itching","fatigue","lethargy","yellowish_skin","dark_urine","loss_of_appetite","abdominal_pain","yellow_urine","yellowing_of_eyes","malaise","receiving_blood_transfusion","receiving_unsterile_injections"],
    "Hepatitis C":            ["fatigue","yellowish_skin","nausea","loss_of_appetite","family_history"],
    "Hepatitis D":            ["joint_pain","vomiting","fatigue","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes"],
    "Hepatitis E":            ["joint_pain","vomiting","fatigue","high_fever","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes","acute_liver_failure","coma","stomach_bleeding"],
    "Alcoholic hepatitis":    ["vomiting","yellowish_skin","abdominal_pain","swelling_of_stomach","history_of_alcohol_consumption","fluid_overload","ascites"],
    "Tuberculosis":           ["chills","vomiting","fatigue","weight_loss","cough","high_fever","breathlessness","sweating","loss_of_appetite","mild_fever","swelled_lymph_nodes","malaise","phlegm","chest_pain","blood_in_sputum"],
    "Common Cold":            ["continuous_sneezing","chills","fatigue","cough","high_fever","headache","swelled_lymph_nodes","malaise","phlegm","throat_irritation","redness_of_eyes","sinus_pressure","runny_nose","congestion","chest_pain","loss_of_smell","muscle_pain"],
    "Pneumonia":              ["chills","fatigue","cough","high_fever","breathlessness","sweating","malaise","phlegm","chest_pain","fast_heart_rate","rusty_sputum"],
    "Dimorphic hemmorhoids(piles)": ["constipation","pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus"],
    "Heart attack":           ["vomiting","breathlessness","sweating","chest_pain"],
    "Varicose veins":         ["fatigue","cramps","bruising","obesity","swollen_legs","swollen_blood_vessels","prominent_veins_on_calf"],
    "Hypothyroidism":         ["fatigue","weight_gain","cold_hands_and_feets","mood_swings","lethargy","dizziness","puffy_face_and_eyes","enlarged_thyroid","brittle_nails","swollen_extremeties","depression","irritability","abnormal_menstruation"],
    "Hyperthyroidism":        ["fatigue","mood_swings","weight_loss","restlessness","sweating","diarrhoea","fast_heart_rate","excessive_hunger","muscle_weakness","irritability","abnormal_menstruation"],
    "Hypoglycemia":           ["vomiting","fatigue","sweating","anxiety","cold_hands_and_feets","mood_swings","headache","nausea","blurred_and_distorted_vision","excessive_hunger","drying_and_tingling_lips","slurred_speech","irritability","palpitations","muscle_weakness"],
    "Osteoarthritis":         ["joint_pain","neck_pain","knee_pain","hip_joint_pain","swelling_joints","painful_walking"],
    "Arthritis":              ["muscle_weakness","stiff_neck","swelling_joints","movement_stiffness","painful_walking"],
    "Vertigo":                ["vomiting","headache","nausea","spinning_movements","loss_of_balance","unsteadiness"],
    "Acne":                   ["skin_rash","pus_filled_pimples","blackheads","scurring"],
    "Urinary tract infection":["burning_micturition","bladder_discomfort","foul_smell_of_urine","continuous_feel_of_urine"],
    "Psoriasis":              ["skin_rash","joint_pain","skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails"],
    "Impetigo":               ["skin_rash","high_fever","blister","red_sore_around_nose","yellow_crust_ooze"],
    "COVID-19":               ["continuous_sneezing","fatigue","cough","high_fever","headache","breathlessness","loss_of_smell","muscle_pain","sore_throat"],
}

# All unique symptoms
all_symptoms = sorted(set(s for syms in disease_symptom_map.values() for s in syms))

# ── 2. BUILD dataset.csv ────────────────────────────────────────────────────
rows = []
for disease, syms in disease_symptom_map.items():
    # Generate 120 rows per disease (some with slight variation)
    for i in range(120):
        row = {"Disease": disease}
        for sym in all_symptoms:
            row[sym] = 1 if sym in syms else 0
        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(os.path.join(BASE, "data", "dataset.csv"), index=False)
print(f"dataset.csv -> {len(df)} rows x {len(df.columns)} cols")

# ── 3. BUILD symptom_severity.csv ───────────────────────────────────────────
severity_data = {
    "Symptom": all_symptoms,
    "weight":  [5]*len(all_symptoms)   # default weight 5; override key ones below
}
sev_df = pd.DataFrame(severity_data)
high_sev = ["high_fever","chest_pain","breathlessness","coma","stomach_bleeding",
            "blood_in_sputum","altered_sensorium","weakness_of_one_body_side",
            "acute_liver_failure","fast_heart_rate"]
sev_df.loc[sev_df["Symptom"].isin(high_sev), "weight"] = 7
low_sev = ["itching","skin_rash","continuous_sneezing","runny_nose","congestion",
           "blackheads","scurring","silver_like_dusting"]
sev_df.loc[sev_df["Symptom"].isin(low_sev), "weight"] = 2
sev_df.to_csv(os.path.join(BASE, "data", "symptom_severity.csv"), index=False)
print(f"symptom_severity.csv -> {len(sev_df)} symptoms")

# ── 4. BUILD symptom_description.csv ────────────────────────────────────────
desc = {
    "Disease": list(disease_symptom_map.keys()),
    "Description": [
        "A fungal infection affecting the skin causing itching and rashes.",
        "An immune response to a foreign substance causing sneezing and watery eyes.",
        "Gastroesophageal reflux disease causing acid to flow back into the esophagus.",
        "A liver disease causing bile to build up in the liver.",
        "An adverse reaction of the body to a medication.",
        "Sores developing on the lining of the stomach or small intestine.",
        "Acquired Immunodeficiency Syndrome caused by the HIV virus.",
        "A chronic condition that affects how the body processes blood sugar.",
        "Inflammation of the stomach and intestines caused by infection.",
        "A condition in which airways narrow and swell causing difficulty breathing.",
        "A long-term condition where blood pressure in arteries is persistently elevated.",
        "A recurrent headache disorder manifesting with moderate to severe headaches.",
        "Age-related wear and tear affecting the spinal discs in the neck.",
        "Brain damage due to rupture or blockage of blood vessels in the brain.",
        "Yellowing of skin and eyes caused by high bilirubin levels.",
        "A mosquito-borne infectious disease caused by Plasmodium parasites.",
        "A highly contagious viral disease causing an itchy blister-like rash.",
        "A mosquito-borne viral infection causing severe flu-like symptoms.",
        "A bacterial infection caused by Salmonella typhi affecting the digestive tract.",
        "A liver infection caused by the Hepatitis A virus spread via contaminated food.",
        "A viral infection attacking the liver caused by Hepatitis B virus.",
        "A liver infection caused by Hepatitis C virus spread through blood contact.",
        "A viral co-infection occurring only with Hepatitis B infection.",
        "A liver infection caused by Hepatitis E virus through contaminated water.",
        "Liver inflammation caused by excessive alcohol consumption.",
        "A bacterial infection caused by Mycobacterium tuberculosis affecting the lungs.",
        "A common viral infection affecting nose and throat.",
        "Infection of lungs causing alveoli to fill with fluid.",
        "Swollen veins in the lowest part of the rectum and anus.",
        "A myocardial infarction caused by blocked blood flow to the heart.",
        "Enlarged veins usually occurring in legs and feet.",
        "An underactive thyroid gland that does not produce enough thyroid hormone.",
        "An overactive thyroid that produces too much thyroxine.",
        "Low blood sugar (glucose) levels in the body.",
        "Breakdown of joint cartilage and underlying bone.",
        "Inflammation of one or more joints causing pain and stiffness.",
        "A condition causing dizziness and loss of balance.",
        "A skin condition causing spots and pimples especially on the face.",
        "A bacterial infection of the urinary tract.",
        "A skin disease that speeds up the life cycle of skin cells.",
        "A highly contagious skin infection caused by bacteria.",
        "A respiratory illness caused by the SARS-CoV-2 virus.",
    ]
}
desc_df = pd.DataFrame(desc)
desc_df.to_csv(os.path.join(BASE, "data", "symptom_description.csv"), index=False)
print(f"symptom_description.csv -> {len(desc_df)} diseases")

# ── 5. BUILD symptom_precaution.csv ─────────────────────────────────────────
prec = {
    "Disease": list(disease_symptom_map.keys()),
    "Precaution_1": ["bath twice","avoid_allergens","avoid fatty spicy food","cold baths","stop taking drug","avoid fatty spicy food","use_condom","reduce_sugar","stop_eating_outside","switch_to_walking","meditation","meditation","use_heating_pad","consult_doctor","cold_baths","avoid_oily_food","use_neem_in_bathing","drink_papaya_leaf_juice","eat_high_calorie_vegitables","drink_plenty_of_water","take_rest","consult_doctor","consult_doctor","consult_doctor","stop_alcohol_consumption","take_vaccine","drink_vitamin_c_rich_drinks","consult_doctor","avoid_fatty_spicy_food","call_ambulance","lie_down_flat","take_iodine_containing_food","eat_healthy","drink_more_water","avoid_fatty_spicy_food","massage","sleep_more","use_aha_products","increase_fluid_intake","wash_hands_with_warm_water","soak_affected_area_in_warm_water","use_mask"],
    "Precaution_2": ["use detol or neem in bathing","consult_doctor","avoid lying down after eating","exercise","consult_doctor","eat_slowly","avoid blood contact","exercise","consult_doctor","avoid_dust","consult_doctor","reduce_stress","exercise","take_aspirin","dont_cover_with_a_blanket","keep_mosquito_away","add_neem_to_bathing_water","papaya_leaf_juice","avoid_oily_food","avoid_fatty_spicy_food","avoid_fatty_spicy_food","eat_healthy","avoid_fatty_spicy_food","avoid_fatty_spicy_food","avoid_alcohol","take_vaccine","take_rest","consult_doctor","sitz_bath","rush_to_hospital","wear_compression_stockings","consult_doctor","eat_healthy","avoid_alcohol","eat_right","exercise","take_ginkgo_biloba","apply_calaamine","drink_plenty_of_water","stop_self_medication","bath_twice","wash_hands"],
    "Precaution_3": ["keep_nails_short","avoid_dust","maintain_weight","consult_doctor","follow_up","have_small_meals","avoid_open_cuts","consult_doctor","stop_eating_outside","reduce_stress","get_proper_sleep","get_proper_sleep","consult_specialist","take_prescribed_medicine","take_fruits","keep_full_sleeves","stop_bleeding","keep_eyes_clean","high_fiber_diet","eat_high_calorie_vegitables","take_rest","exercise","exercise","consult_doctor","eat_fruits","consult_doctor","gargle","exercise","consume_witch_hazel","consult_doctor","elevate_legs","eat_food_rich_in_fibres","take_antithyroid_medicines","avoid_stress","have_balanced_diet","do_yoga","lie_down","avoid_oily_food","avoid_spicy_food","exercise","consult_doctor","exercise"],
    "Precaution_4": ["use_clean_cloths","use_humidifier","avoid_alcohol","proper_medication","consult_doctor","avoid_spicy_food","be_safe","consult_doctor","eat_home_cooked_food","get_vaccinated","reduce_stress","try_nose_block_breathing","use_cervical_pillow","take_prescribed_medicine","avoid_sugary_food","drink_herbal_tea","use_calamine_lotion","keep_hydrated","avoid_fast_food","get_vaccination","eat_food_in_small_proportions","avoid_alcohol","consult_doctor","consult_doctor","consult_doctor","stop_smoking","steam","take_oximeter_readings","avoid_sitting_long","consult_specialist","avoid_prolonged_standing","follow_up","take_antithyroid_medicines","relax","avoid_steroids","consult_specialist","seek_medical_help","use_clean_face_wash","follow_up","take_tablet_ketoconazole","consult_doctor","isolate"],
}
prec_df = pd.DataFrame(prec)
prec_df.to_csv(os.path.join(BASE, "data", "symptom_precaution.csv"), index=False)
print(f"symptom_precaution.csv -> {len(prec_df)} diseases")

print("\n[SUCCESS] All dataset files created successfully!")
