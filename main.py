import flet as ft

# =============================================================================
# 1. DONNÉES MÉDICALES (SFAR 2024)
# =============================================================================

RFE_GENERALES = {
    "R1.1 - Délai d'administration": {
        "titre": "R1.1 - Quand administrer l'antibioprophylaxie ?",
        "reco": "Il est recommandé d'administrer l'antibioprophylaxie par céphalosporine (ou ses alternatives en cas d'allergie, hors vancomycine) au plus tôt 60 minutes avant et au plus tard avant l'incision chirurgicale.",
        "grade": "GRADE 1 (Accord FORT)"
    },
    "R1.2 - Délai Vancomycine": {
        "titre": "R1.2 - Cas particulier de la Vancomycine",
        "reco": "Débuter l'administration intraveineuse sur 60 minutes chez le patient non obèse au plus tôt 60 minutes avant, et au plus tard 30 minutes avant l'incision.",
        "grade": "Avis d'experts (Accord FORT)"
    },
    "R1.3 - Réinjection peropératoire": {
        "titre": "R1.3 - Réinjection",
        "reco": "Réinjecter (demi-dose) toutes les 2 demi-vies : 2h (Cefoxitine, Amox-Clav), 4h (Cefazoline, Clindamycine).",
        "grade": "GRADE 1 & 2"
    },
    "R1.4 - Durée": {
        "titre": "R1.4 - Durée post-opératoire",
        "reco": "Il n'est pas recommandé de prolonger l'antibioprophylaxie au-delà de la fin de la chirurgie (sauf exceptions).",
        "grade": "GRADE 1"
    }
}

SFAR_DATA = {
    "Neurochirurgie": {
        "Chirurgie Cranienne": {
            "Craniotomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 2", "allergie": "Clindamycine 900mg IVL"},
            "Biopsie cérébrale": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Rachis": {
            "Chirurgie instrumentée": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 2", "allergie": "Clindamycine 900mg IVL"},
            "Chirurgie sans matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Sauf risque brèche"}
        }
    },
    "ORL": {
        "Chirurgie rhino-sinusienne": {
            "Sinusite / Polypose": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Rhinoplastie avec greffe": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 2", "allergie": "Clindamycine 900mg IVL"}
        },
        "Amygdalectomie": {
            "Amygdalectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"}
        }
    },
    "Stomatologie": {
        "Dents": {
            "Dents incluses": {"molecule": "Amoxicilline", "dose": "2g IVL", "reinjection": "1g / 2h", "grade": "GRADE 1", "allergie": "Clindamycine 600mg PO / 900mg IV"},
            "Dents sur arcade": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"}
        }
    },
    "Ophtalmologie": {
        "Cataracte": {
            "Cataracte": {"molecule": "Céfuroxime (Intra-camérulaire)", "dose": "1mg / 0.1mL", "reinjection": "Unique", "grade": "GRADE 1", "allergie": "Moxifloxacine"}
        }
    },
    "Thoracique": {
        "Poumon": {
            "Lobectomie / Pneumonectomie": {"molecule": "Céfazoline (ou Amox-Clav si BPCO)", "dose": "2g", "reinjection": "Cefaz 4h / Amox 2h", "grade": "GRADE 1", "allergie": "Clindamycine + Gentamicine"}
        },
        "Médiastin": {
            "Médiastinoscopie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "Cardiovasculaire": {
        "Cœur": {
            "Valvulaire / Pontage": {"molecule": "Céfazoline", "dose": "2g IVL (+1g CEC)", "reinjection": "1g / 4h", "grade": "GRADE 1", "allergie": "Vanco ou Teicoplanine"},
            "Pacemaker": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 1", "allergie": "Vanco ou Teicoplanine"}
        },
        "Vaisseaux": {
            "Aorte / Carotide (matériel)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 1", "allergie": "Vanco ou Teicoplanine"},
            "Varices (sans Scarpa)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "Orthopédie": {
        "Prothèses": {
            "Hanche / Genou": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "Avis d'experts", "allergie": "Clindamycine (Vanco si épaule)"}
        },
        "Trauma": {
            "Fracture fermée": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "Avis d'experts", "allergie": "Clindamycine"},
            "Fracture ouverte": {"molecule": "Amox-Clav", "dose": "2g IVL", "reinjection": "1g / 2h", "grade": "GRADE 1", "allergie": "Clinda + Genta"}
        },
        "Arthroscopie": {
            "Sans matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "Digestif": {
        "Bariatrique": {
            "Sleeve / Bypass": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g / 2h", "grade": "Avis d'experts", "allergie": "Genta + Métronidazole"},
            "Anneau": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "Avis d'experts", "allergie": "Vanco ou Teico"}
        },
        "Colorectal": {
            "Colectomie": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g / 2h", "grade": "GRADE 1", "allergie": "Genta + Métronidazole"},
            "Appendicectomie": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g / 2h", "grade": "Avis d'experts", "allergie": "Genta + Métronidazole"}
        },
        "Hépato-Biliaire": {
            "Cholécystectomie simple": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"}
        }
    },
    "Urologie": {
        "Prostate": {
            "RTUP / Laser": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 1", "allergie": "Gentamicine"},
            "Biopsies": {"molecule": "Fosfomycine", "dose": "3g PO", "reinjection": "Unique", "grade": "GRADE 1", "allergie": "Ciprofloxacine"}
        },
        "Rein": {
            "Urétéroscopie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 1", "allergie": "Gentamicine"}
        }
    },
    "Gynécologie": {
        "Utérus": {
            "Hystérectomie": {"molecule": "Céfoxitine (ou Cefaz si subtotale)", "dose": "2g IVL", "reinjection": "2h ou 4h", "grade": "Avis d'experts", "allergie": "Clinda + Genta"}
        },
        "Obstétrique": {
            "Césarienne": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g / 4h", "grade": "GRADE 2", "allergie": "Clindamycine"},
            "IVG aspiration": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"}
        }
    }
}

# =============================================================================
# 2. APPLICATION FLET
# =============================================================================

def main(page: ft.Page):
    page.title = "Antibio SFAR 2024"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0  # Pour que l'AppBar touche les bords
    page.scroll = "adaptive"

    # --- FONCTIONS DE NAVIGATION ---
    
    def go_home(e=None):
        page.views.clear()
        page.views.append(view_home())
        page.go("/")

    def go_category(e, spec_name):
        page.views.append(view_category(spec_name))
        page.go(f"/category/{spec_name}")

    def go_detail(e, spec_name, cat_name):
        page.views.append(view_detail(spec_name, cat_name))
        page.go(f"/detail/{spec_name}/{cat_name}")

    def pop_view(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_view_pop = pop_view

    # --- VUE 1 : ACCUEIL (SPÉCIALITÉS) ---
    def view_home():
        # Liste des spécialités
        spec_list = ft.ListView(expand=True, spacing=10, padding=20)
        
        # Ajout du bouton d'infos générales
        def show_info(e):
            # Création du contenu de la boîte de dialogue
            content_col = ft.Column(scroll="auto", height=400)
            for key, val in RFE_GENERALES.items():
                content_col.controls.append(ft.Text(val["titre"], weight="bold", size=16, color="blue"))
                content_col.controls.append(ft.Text(val["reco"], size=14))
                content_col.controls.append(ft.Text(val["grade"], size=12, italic=True, color="orange"))
                content_col.controls.append(ft.Divider())

            dlg = ft.AlertDialog(
                title=ft.Text("Recommandations Générales"),
                content=ft.Container(content=content_col),
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        for spec in SFAR_DATA.keys():
            card = ft.Card(
                elevation=2,
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color="blue"),
                    title=ft.Text(spec, weight="bold"),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14),
                    on_click=lambda e, s=spec: go_category(e, s)
                )
            )
            spec_list.controls.append(card)

        return ft.View(
            "/",
            controls=[
                ft.AppBar(
                    title=ft.Text("Antibio SFAR 2024"), 
                    bgcolor="blue", 
                    color="white",
                    actions=[ft.IconButton(ft.Icons.INFO_OUTLINE, on_click=show_info)]
                ),
                spec_list
            ]
        )

    # --- VUE 2 : CATÉGORIES ---
    def view_category(spec_name):
        cat_list = ft.ListView(expand=True, spacing=10, padding=20)
        
        categories = SFAR_DATA.get(spec_name, {})
        
        for cat in categories.keys():
            card = ft.Card(
                elevation=2,
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.FOLDER_OPEN, color="orange"),
                    title=ft.Text(cat, weight="bold"),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14),
                    on_click=lambda e, c=cat: go_detail(e, spec_name, c)
                )
            )
            cat_list.controls.append(card)

        return ft.View(
            f"/category/{spec_name}",
            controls=[
                ft.AppBar(title=ft.Text(spec_name), bgcolor="blue", color="white"),
                cat_list
            ]
        )

    # --- VUE 3 : DÉTAIL (SÉLECTION INTERVENTION) ---
    def view_detail(spec_name, cat_name):
        interventions_dict = SFAR_DATA[spec_name][cat_name]
        intervention_names = list(interventions_dict.keys())
        
        # Eléments d'affichage des résultats
        txt_molecule = ft.Text("-", size=18, weight="bold", color="blue")
        txt_dose = ft.Text("-", size=16)
        txt_reinjection = ft.Text("-", size=16)
        txt_grade = ft.Text("-", italic=True, color="orange")
        txt_allergie = ft.Text("-", color="red", weight="bold")
        
        result_card = ft.Card(
            visible=False, # Caché au début
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Molécule :", size=12, color="grey"),
                    txt_molecule,
                    ft.Divider(),
                    ft.Text("Dose Initiale :", size=12, color="grey"),
                    txt_dose,
                    ft.Divider(),
                    ft.Text("Réinjection :", size=12, color="grey"),
                    txt_reinjection,
                    ft.Divider(),
                    ft.Text("Grade :", size=12, color="grey"),
                    txt_grade,
                    ft.Divider(),
                    ft.Text("Allergie / Alternative :", size=12, color="grey"),
                    txt_allergie
                ])
            )
        )

        def on_change_dropdown(e):
            selected_inter = dd_interventions.value
            if selected_inter:
                data = interventions_dict[selected_inter]
                
                txt_molecule.value = data["molecule"]
                if "PAS D'ANTIBIO" in data["molecule"]:
                    txt_molecule.color = "red"
                else:
                    txt_molecule.color = "blue"
                    
                txt_dose.value = data["dose"]
                txt_reinjection.value = data["reinjection"]
                txt_grade.value = data["grade"]
                txt_allergie.value = data["allergie"]
                
                result_card.visible = True
                page.update()

        dd_interventions = ft.Dropdown(
            label="Choisir l'intervention",
            options=[ft.dropdown.Option(i) for i in intervention_names],
            on_change=on_change_dropdown,
            text_size=14
        )

        return ft.View(
            f"/detail/{spec_name}/{cat_name}",
            controls=[
                ft.AppBar(title=ft.Text(cat_name), bgcolor="blue", color="white"),
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text("Sélectionnez l'acte chirurgical :", weight="bold"),
                        dd_interventions,
                        ft.Divider(height=20, color="transparent"),
                        result_card
                    ])
                )
            ]
        )

    # Lancement initial
    page.go("/")
    page.views.append(view_home())
    page.update()

ft.app(target=main)