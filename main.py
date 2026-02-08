import flet as ft

def main(page: ft.Page):
    page.title = "Peds Dosing"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.padding = 20

    # --- DATA ---
    drug_db = {
        "Syrup Atarax": {"type": "weight", "comp": "Hydroxyzine (10mg/5ml)", "points": {10: 2.5, 15: 3.5, 20: 5}, "freq": "Q8H", "note": "For 30kg: 3/4 of T. Atarax 25mg"},
        "Syrup Salasma Plus": {"type": "weight", "comp": "Ambroxol + Levosalbutamol + Guaifenesin", "points": {10: 2.5, 15: 3.5, 20: 4.5, 30: 7, 40: 10}, "freq": "Q12H", "note": ""},
        "Syrup MegaCV (457/5)": {"type": "weight", "comp": "Amox + Clav (457mg/5ml)", "points": {10: 2.5, 15: 3.5, 20: 5}, "freq": "Q12H", "note": ""},
        "Syrup MegaCV (228/5)": {"type": "weight", "comp": "Amox + Clav (228mg/5ml)", "points": {5: 2.5, 10: 4.5}, "freq": "Q12H", "note": ""},
        "Syrup Cefixime (100/5)": {"type": "weight", "comp": "Cefixime (100mg/5ml)", "points": {10: 2.5, 15: 3.5, 20: 5}, "freq": "Q12H", "note": ""},
        "Syrup Cefixime (50/5)": {"type": "weight", "comp": "Cefixime (50mg/5ml)", "points": {5: 2.0, 7: 2.5}, "freq": "Q12H", "note": ""},
        "Syrup Montek LC": {"type": "weight", "comp": "Montelukast + Levocetirizine", "points": {10: 2.5, 15: 3.5, 20: 5}, "freq": "HS", "note": ""},
        "Syrup Paracetamol": {"type": "weight", "comp": "Paracetamol (250mg/5ml)", "points": {10: 3.0, 15: 5.0}, "freq": "Q8H / SOS", "note": ""},
        "Kufril LS Drops": {"type": "weight", "comp": "Ambroxol + Levo + Guai", "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0}, "freq": "Q8H", "note": ""},
        "Nozolev Drops": {"type": "weight", "comp": "Phenylephrine + CPM", "points": {5: 0.5, 7: 0.7, 8: 0.8, 10: 1.0}, "freq": "Q12H", "note": ""},
        "Syrup Ambrodil S": {"type": "weight", "comp": "Ambroxol + Salbutamol", "points": {5: 2.5, 7: 3.5, 10: 5.0}, "freq": "Q12H", "note": ""},
        "Syrup Emecet (1/5)": {"type": "weight", "comp": "Ondansetron (2mg/5ml)", "points": {5: 1.5, 7: 2.0, 10: 2.5, 20: 5.0}, "freq": "As Directed", "note": "For 20kg+, consider 2mg Tablet"},
        "Syrup Cetrizine": {"type": "weight", "comp": "Cetirizine (5mg/5ml)", "points": {5: 1.5, 7: 2.0, 10: 2.5}, "freq": "HS", "note": ""},
        "Syrup Cyclopam": {"type": "weight", "comp": "Dicyclomine + Simethicone", "points": {4: 2.0, 8: 4.0, 10: 5.0}, "freq": "Q8H", "note": ""},
        "Syrup Albendazole": {"type": "age", "comp": "Albendazole (400mg/10ml)", "note": "<2yrs: 5ml. >2yrs: 10ml."},
        "Syrup Zinc": {"type": "age", "comp": "Zinc (20mg/5ml)", "note": "2-6m: 2.5ml OD. >6m: 2.5ml BD."}
    }

    # --- UI COMPONENTS ---
    weight_input = ft.TextField(label="Weight (kg)", value="10", keyboard_type="number", expand=True)
    age_input = ft.TextField(label="Age (months)", value="12", keyboard_type="number", expand=True)
    results_view = ft.Column()
    drug_list_view = ft.Column(scroll="auto", height=400)

    # Populate Drug List
    checkboxes = []
    for d in drug_db:
        cb = ft.Checkbox(label=d, value=False)
        checkboxes.append(cb)
        drug_list_view.controls.append(cb)

    # --- LOGIC ---
    def show_error(message):
        page.snack_bar = ft.SnackBar(ft.Text(message, color="white"), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    def select_all(e):
        # Toggle based on the first box
        new_val = not checkboxes[0].value
        for cb in checkboxes:
            cb.value = new_val
        page.update()

    def calculate_dose(e):
        results_view.controls.clear()
        
        # 1. Validate Inputs (Crash Prevention)
        try:
            if not weight_input.value: raise ValueError
            w = float(weight_input.value)
            
            if not age_input.value: raise ValueError
            am = int(age_input.value)
        except ValueError:
            show_error("Please enter a valid Weight and Age!")
            return

        # 2. Find Selected Drugs
        selected_drugs = [cb.label for cb in checkboxes if cb.value == True]
        
        if not selected_drugs:
            show_error("Please select at least one drug (check the box)!")
            return

        # 3. Calculate
        for drug_name in selected_drugs:
            info = drug_db[drug_name]
            dose_str = "0 ml"
            freq = ""
            
            if info.get("type") == "weight":
                points = info["points"]
                sorted_w = sorted(points.keys())
                if w <= sorted_w[0]: d = points[sorted_w[0]] * (w / sorted_w[0])
                elif w >= sorted_w[-1]: d = points[sorted_w[-1]]
                else:
                    for i in range(len(sorted_w)-1):
                        if sorted_w[i] <= w <= sorted_w[i+1]:
                            w1, w2 = sorted_w[i], sorted_w[i+1]
                            d = points[w1] + (w - w1) * (points[w2] - points[w1]) / (w2 - w1)
                            break
                dose_str = f"{d:.1f} ml"
                freq = info["freq"]
            
            elif info.get("type") == "age":
                if "Albendazole" in drug_name:
                    dose_str = "5 ml" if am < 24 else "10 ml"
                    freq = "Stat/HS"
                elif "Zinc" in drug_name:
                    if 2 <= am <= 6: dose_str, freq = "2.5 ml", "OD"
                    elif am > 6: dose_str, freq = "2.5 ml", "BD"
                    else: dose_str, freq = "Consult", ""

            # Create Card
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.MEDICATION, color="blue"),
                            title=ft.Text(f"{drug_name}", weight="bold"),
                            subtitle=ft.Text(f"Dose: {dose_str}  |  {freq}", size=16, color="black", weight="bold"),
                        ),
                        ft.Container(
                            content=ft.Text(f"Comp: {info['comp']}", size=12, color="grey"),
                            padding=ft.padding.only(left=16, bottom=5)
                        ),
                        ft.Container(
                            content=ft.Text(f"Note: {info.get('note','')}", size=12, italic=True, color="red"),
                            padding=ft.padding.only(left=16, bottom=10)
                        ) if info.get("note") else ft.Container()
                    ]),
                    padding=5
                )
            )
            results_view.controls.append(card)
        
        page.update()

    # --- LAYOUT ---
    page.add(
        ft.Text("Peds Calculator", size=24, weight="bold", color="blue"),
        ft.Row([weight_input, age_input]),
        ft.ElevatedButton("Select All / Deselect All", on_click=select_all),
        ft.Text("Select Drugs:", weight="bold"),
        ft.Container(drug_list_view, border=ft.border.all(1, "grey"), border_radius=10, padding=10),
        ft.ElevatedButton("Calculate Dose", on_click=calculate_dose, width=400, height=50, bgcolor="blue", color="white"),
        ft.Divider(),
        results_view,
    )

ft.app(target=main)
    
