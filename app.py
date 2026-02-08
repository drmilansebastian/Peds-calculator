import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Peds Dosing", page_icon="💊")

# --- DATA & LOGIC ---
# Define the drugs and their reference points (Weight in kg: Dose in ml)
drug_db = {
    "Syrup Atarax (Hydroxyzine)": {
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q8H",
        "note": "For 30kg: 3/4 of T. Atarax 25mg"
    },
    "Syrup Salasma Plus": {
        "points": {10: 2.5, 15: 3.5, 20: 4.5, 30: 7, 40: 10},
        "freq": "Q12H",
        "note": "Contains Ambroxol + Levosalbutamol + Guaifenesin"
    },
    "Syrup MegaCV (457/5)": {
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup MegaCV (228/5)": {
        "points": {5: 2.5, 10: 4.5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Cefixime (100/5)": {
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Cefixime (50/5)": {
        "points": {5: 2.0, 7: 2.5},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Montek LC": {
        "points": {10: 2.5, 15: 3.5, 20: 5},
        "freq": "HS (Bedtime)",
        "note": ""
    },
    "Syrup Paracetamol (250/5)": {
        "points": {10: 3.0, 15: 5.0},
        "freq": "Q8H / SOS",
        "note": ""
    },
    "Kufril LS Drops": {
        "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0},
        "freq": "Q8H",
        "note": ""
    },
    "Nozolev Drops": {
        "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Ambrodil S": {
        "points": {5: 2.5, 7: 3.5, 10: 5.0},
        "freq": "Q12H",
        "note": ""
    },
    "Syrup Emecet (1/5)": {
        "points": {5: 1.5, 7: 2.0, 10: 2.5, 20: 5.0},
        "freq": "As Directed",
        "note": "For 20kg+, consider 2mg Tablet"
    }
}

def calculate_dose(weight, points):
    # Sort weights to ensure correct interpolation
    sorted_weights = sorted(points.keys())
    
    # Handle weight below lowest data point (Extrapolation or fixed min)
    if weight <= sorted_weights[0]:
        return points[sorted_weights[0]] * (weight / sorted_weights[0]) # Linear down to 0
    
    # Handle weight above highest data point
    if weight >= sorted_weights[-1]:
        return points[sorted_weights[-1]] # Cap at max defined dose logic (or extend)
        
    # Linear Interpolation
    for i in range(len(sorted_weights) - 1):
        w1 = sorted_weights[i]
        w2 = sorted_weights[i+1]
        if w1 <= weight <= w2:
            d1 = points[w1]
            d2 = points[w2]
            return d1 + (weight - w1) * (d2 - d1) / (w2 - w1)
    return 0

# --- APP INTERFACE ---
st.title("Pediatric Dosing Calculator")
st.write("Select a drug and enter weight to get the dose.")

selected_drug = st.selectbox("Select Drug", list(drug_db.keys()))
weight = st.number_input("Child's Weight (kg)", min_value=1.0, max_value=60.0, value=10.0, step=0.5)

if st.button("Calculate Dose"):
    drug_info = drug_db[selected_drug]
    points = drug_info["points"]
    freq = drug_info["freq"]
    
    dose_ml = calculate_dose(weight, points)
    
    st.success(f"**Dose:** {dose_ml:.1f} ml")
    st.write(f"**Frequency:** {freq}")
    
    if drug_info["note"]:
        st.info(f"**Note:** {drug_info['note']}")

    st.caption("Dr.milan sebastian")
          
