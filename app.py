import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Peds Dosing", page_icon="💊")

# --- DATA ---
drug_db = {
    # --- WEIGHT BASED DRUGS ---
    "Syrup Atarax": {
        "type": "weight",
        "comp": "Hydroxyzine (10mg/5ml)",
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q8H",
        "note": "For 30kg: 3/4 of T. Atarax 25mg"
    },
    "Syrup Salasma Plus": {
        "type": "weight",
        "comp": "Ambroxol + Levosalbutamol + Guaifenesin",
        "points": {10: 2.5, 15: 3.5, 20: 4.5, 30: 7, 40: 10},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup MegaCV (457/5)": {
        "type": "weight",
        "comp": "Amoxicillin + Clavulanic Acid (457mg/5ml)",
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup MegaCV (228/5)": {
        "type": "weight",
        "comp": "Amoxicillin + Clavulanic Acid (228mg/5ml)",
        "points": {5: 2.5, 10: 4.5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Cefixime (100/5)": {
        "type": "weight",
        "comp": "Cefixime (100mg/5ml)",
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Cefixime (50/5)": {
        "type": "weight",
        "comp": "Cefixime (50mg/5ml)",
        "points": {5: 2.0, 7: 2.5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Montek LC": {
        "type": "weight",
        "comp": "Montelukast + Levocetirizine",
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "HS (Bedtime)",
        "note": ""
    },
    "Syrup Paracetamol (250/5)": {
        "type": "weight",
        "comp": "Paracetamol (250mg/5ml)",
        "points": {10: 3.0, 15: 5.0},
        "freq": "Q8H / SOS",
        "note": ""
    },
    "Kufril LS Drops": {
        "type": "weight",
        "comp": "Ambroxol + Levosalbutamol + Guaifenesin",
        "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0},
        "freq": "Q8H",
        "note": ""
    },
    "Nozolev Drops": {
        "type": "weight",
        "comp": "Phenylephrine + Chlorpheniramine",
        "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Ambrodil S": {
        "type": "weight",
        "comp": "Ambroxol + Salbutamol",
        "points": {5: 2.5, 7: 3.5, 10: 5.0},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Emecet (1/5)": {
        "type": "weight",
        "comp": "Ondansetron (2mg/5ml)",
        "points": {5: 1.5, 7: 2.0, 10: 2.5, 20: 5.0},
        "freq": "As Directed",
        "note": "For 20kg+, consider 2mg Tablet"
    },
    "Syrup Cetrizine (5/5)": {
        "type": "weight",
        "comp": "Cetirizine (5mg/5ml)",
        "points": {5: 1.5, 7: 2.0, 10: 2.5},
        "freq": "HS (Bedtime)",
        "note": ""
    },
    "Syrup Cyclopam (10/5)": {
        "type": "weight",
        "comp": "Dicyclomine (10mg) + Simethicone (40mg)",
        "points": {4: 2.0, 8: 4.0, 10: 5.0},
        "freq": "Q8H",
        "note": ""
    },
    "Syrup Albendazole (400/10)": {
        "type": "age",
        "comp": "Albendazole (400mg/10ml)",
        "note": "Age < 2yrs: 5ml. Age > 2yrs: 10ml."
    },
    "Syrup Zinc (20/5)": {
        "type": "age",
        "comp": "Zinc Acetate/Gluconate (20mg/5ml)",
        "note": "2-6 months: 2.5ml OD. >6 months: 2.5ml Q12H."
    }
}

# --- FUNCTIONS ---
def calculate_weight_dose(weight, points):
    sorted_weights = sorted(points.keys())
    if weight <= sorted_weights[0]:
        return points[sorted_weights[0]] * (weight / sorted_weights[0])
    if weight >= sorted_weights[-1]:
        return points[sorted_weights[-1]]
    for i in range(len(sorted_weights) - 1):
        w1 = sorted_weights[i]
        w2 = sorted_weights[i+1]
        if w1 <= weight <= w2:
            d1 = points[w1]
            d2 = points[w2]
            return d1 + (weight - w1) * (d2 - d1) / (w2 - w1)
    return 0

def calculate_age_dose(drug_name, age_months):
    if "Albendazole" in drug_name:
        if age_months < 24: # Less than 2 years
            return "5 ml", "HS (Once in 2 weeks for 4 weeks)"
        else: # Greater than 2 years
            return "10 ml", "HS (Once in 2 weeks for 4 weeks)"
    if "Zinc" in drug_name:
        if 2 <= age_months <= 6:
            return "2.5 ml", "OD (Once Daily)"
        elif age_months > 6:
            return "2.5 ml", "Q12H (Twice Daily)"
        else:
            return "0 ml", "Consult Pediatrician (Age < 2 months)"
    return "0 ml", ""

# --- APP INTERFACE ---
st.title("Pediatric Dosing Calculator")
st.write("Select one or more drugs, enter details, and get the list.")

# Multiselect for Drugs
selected_drugs = st.multiselect("Select Drugs", list(drug_db.keys()))

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=60.0, value=10.0, step=0.5)
with col2:
    age_months = st.number_input("Age (in months)", min_value=0, max_value=200, value=12, step=1)

if st.button("Calculate All"):
    if not selected_drugs:
        st.warning("Please select at least one drug.")
    else:
        st.markdown("### 📋 Prescription List")
        for drug_name in selected_drugs:
            drug_info = drug_db[drug_name]
            comp = drug_info["comp"]
            note = drug_info.get("note", "")
            
            # Logic Switch based on Drug Type
            if drug_info.get("type") == "weight":
                dose_val = calculate_weight_dose(weight, drug_info["points"])
                dose_str = f"{dose_val:.1f} ml"
                freq = drug_info["freq"]
            elif drug_info.get("type") == "age":
                dose_str, freq = calculate_age_dose(drug_name, age_months)
            
            # Display Card for each drug
            with st.expander(f"**{drug_name}** - {dose_str}", expanded=True):
                st.write(f"**Dose:** {dose_str} | **Freq:** {freq}")
                st.caption(f"Composition: {comp}")
                if note:
                    st.info(f"Note: {note}")

    st.caption("Dr.milan sebastian")
    
