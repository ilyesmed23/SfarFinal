import logging
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

# -----------------------------------------------------------------------------
# 1. DONNÉES TEXTUELLES : RECOMMANDATIONS GÉNÉRALES
# -----------------------------------------------------------------------------
RFE_GENERALES = {
    "R1.1 - Délai d'administration": {
        "titre": "R1.1 - Quand administrer l'antibioprophylaxie ?",
        "reco": "Il est recommandé d'administrer l'antibioprophylaxie par céphalosporine (ou ses alternatives en cas d'allergie, hors vancomycine) au plus tôt 60 minutes avant et au plus tard avant l'incision chirurgicale ou le début de la procédure interventionnelle pour diminuer l'incidence d'infection du site opératoire.",
        "grade": "GRADE 1 (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nL'administration doit précéder l'incision pour assurer une concentration tissulaire efficace dès l'ouverture cutanée. Le délai optimal est dans les 60 minutes précédant l'incision. Une administration trop précoce (>60 min) risque de voir les concentrations diminuer sous le seuil efficace."
    },
    "R1.2 - Délai Vancomycine": {
        "titre": "R1.2 - Cas particulier de la Vancomycine",
        "reco": "En cas d'utilisation de la vancomycine en antibioprophylaxie, les experts suggèrent d'en débuter l'administration intraveineuse sur 60 minutes chez le patient non obèse au plus tôt 60 minutes avant, et au plus tard 30 minutes avant l'incision chirurgicale ou le début de la procédure interventionnelle, pour diminuer l'incidence d'infection du site opératoire.",
        "grade": "Avis d'experts (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nLa Vancomycine nécessite une perfusion lente (1h) pour éviter le 'Red Man Syndrome'. L'intervalle optimal de début de perfusion est 60 à 30 minutes avant l'incision."
    },
    "R1.3 - Réinjection peropératoire": {
        "titre": "R1.3 - Faut-il réinjecter en cours d'intervention ?",
        "reco": (
            "R1.3.1 - Il est recommandé de réadministrer une à plusieurs dose(s) peropératoire(s) d'antibioprophylaxie en cas de prolongation de la chirurgie ou de l'acte interventionnel pour diminuer l'incidence d'infection du site opératoire.\n\n"
            "R1.3.2 - Il est probablement recommandé de réadministrer cette (ces) dose(s) peropératoire(s), à une posologie de la moitié de la dose initiale, toutes les deux demi-vies de l'antibiotique utilisé pour diminuer l'incidence d'infection du site opératoire; soit durant la période peropératoire :\n"
            "- toutes les 2 heures pour la céfoxitine (1 g), le céfuroxime (0,75 g) et l'amoxicilline/clavulanate (1 g)\n"
            "- toutes les 4 heures pour la céfazoline (1 g) et la clindamycine (450 mg)\n"
            "- toutes les 8 heures pour la vancomycine (10 mg/kg).\n"
            "Du fait de leur demi-vie très longue, la gentamicine, le métronidazole et la teicoplanine ne nécessitent pas de réinjection peropératoire."
        ),
        "grade": "GRADE 1 & GRADE 2 (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nL'objectif est de maintenir une concentration efficace tout au long de la chirurgie. Une réinjection doit aussi être discutée en cas de saignement majeur."
    },
    "R1.4 - Durée de l'antibioprophylaxie": {
        "titre": "R1.4 - Combien de temps poursuivre ?",
        "reco": "Il n'est pas recommandé, dans la très grande majorité des cas (et hors exceptions mentionnées dans chaque tableau), de prolonger l'administration de l'antibioprophylaxie au-delà de la fin de la chirurgie pour diminuer l'incidence d'infection du site opératoire.",
        "grade": "GRADE 1 (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nProlonger l'antibioprophylaxie n'apporte aucun bénéfice sur le taux d'ISO et augmente le risque de résistance."
    },
    "R1.5 - Patient Obèse (Bêtalactamines)": {
        "titre": "R1.5 - Obésité et Bêtalactamines",
        "reco": "Il n'est probablement pas recommandé d'augmenter la dose unitaire de céphalosporine utilisée en antibioprophylaxie chez le patient obèse pour diminuer l'incidence d'ISO, en dehors de cas particuliers (IMC supérieur à 50 kg/m²).",
        "grade": "GRADE 2 (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nLes céphalosporines diffusent peu dans la graisse. La dose standard suffit si les réinjections sont respectées. Pour les IMC > 50, une adaptation est discutable."
    },
    "R1.6 - Patient Obèse (Autres molécules)": {
        "titre": "R1.6 - Obésité et Alternatives",
        "reco": (
            "R1.6 - Pour les molécules utilisées en alternatives aux bêtalactamines en cas d'allergie, les experts suggèrent d'utiliser les doses suivantes chez le patient obèse pour diminuer l'incidence d'ISO :\n"
            "- clindamycine : 900 mg pour des IMC entre 30 et 45 kg/m²; 1200 mg pour des IMC entre 45 et 60 kg/m²; 1600 mg pour des IMC > 60 kg/m²\n"
            "- gentamicine : 6 à 7 mg/kg de poids ajusté\n"
            "- vancomycine : 20 mg/kg de poids total (comme chez le non-obèse).\n"
            "Du fait de l'absence de donnée dans cette population, la teicoplanine n'est pas recommandée chez le patient obèse."
        ),
        "grade": "Avis d'experts (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nAdaptation nécessaire pour ces molécules lipophiles ou à risque toxique (Gentamicine)."
    },
    "R1.7 - Colonisation E-BLSE": {
        "titre": "R1.7 - Patient porteur de BLSE",
        "reco": (
            "R1.7.1 - Dans les centres où la prévalence de colonisation digestive à entérobactéries productrices de bêta-lactamase à spectre étendu (E-BLSE) des patients devant être opérés de chirurgie colorectale est supérieure ou égale à 10%, les experts suggèrent de réaliser un dépistage de la colonisation rectale à E-BLSE chez ces patients, dans le mois précédant la chirurgie, afin d'adapter l'antibioprophylaxie et de diminuer l'incidence d'infection du site opératoire.\n\n"
            "R1.7.2 - En cas de positivité du dépistage de la colonisation rectale à E-BLSE, les experts suggèrent d'administrer, pour une chirurgie colo-rectale, une antibioprophylaxie ciblée active sur la souche d'E-BLSE identifiée lors du dépistage, pour diminuer l'incidence d'infection du site opératoire.\n\n"
            "R1.7.3 - Dans le cadre de la chirurgie colo-rectale, les experts suggèrent une prise en charge multidisciplinaire incluant un anesthésiste-réanimateur, un chirurgien, un infectiologue (ou un référent en infectiologie) et un microbiologiste pour individualiser l'antibioprophylaxie des patients colonisés au niveau rectal à E-BLSE."
        ),
        "grade": "Avis d'experts (Accord FORT)",
        "argumentaire": "Résumé de l'argumentaire :\nStratégie à discuter de manière multidisciplinaire pour la chirurgie colorectale."
    }
}

# -----------------------------------------------------------------------------
# 2. BASE DE DONNÉES CLINIQUES (SFAR 2024) - COMPLÈTE
# -----------------------------------------------------------------------------
SFAR_DATA = {
    "Neurochirurgie & Neuroradiologie": {
        "Chirurgie Cranienne": {
            "Craniotomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Ventriculoscopie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Visiochirurgie intracrânienne": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Biopsie cérébrale": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Neurochirurgie trans-sphénoïdale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Neurochirurgie trans-labyrinthique": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Plaies cranio-cérébrales": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h, puis toutes les 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Cotrimoxazole (Bactrim). \nRemarque: Prolonger 24-48h max si plaie souillée."},
            "Fracture de la base du crâne": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Dérivations & Matériel": {
            "Dérivation ventriculaire externe (DVE)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Dérivation lombaire externe (DLE)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Dérivation ventriculo-péritonéale (DVP)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Dérivation ventriculo-atriale (DVA)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Pose d'électrode de stimulation": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Pose de stimulateur": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Pose de pompe intrathécale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."}
        },
        "Chirurgie Rachidienne": {
            "Chirurgie instrumentée du rachis (1 temps)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie instrumentée du rachis (2 temps)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Reprise de matériel rachidien": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie du rachis percutanée avec matériel": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Cimentoplastie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h, puis toutes les 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie du rachis sans matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Remarque: Céfazoline discutable si risque de brèche."},
            "Ablation de matériel du rachis": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Remarque: Céfazoline discutable si risque de brèche."}
        },
        "Neuroradiologie interventionnelle": {
            "Angiographie diagnostique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Angioplastie / Stent / Endoprothèse": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Embolisation (Anévrysme, MAV)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Thermo-coagulation du trijumeau": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "ORL (Oto-Rhino-Laryngologie)": {
        "Chirurgie rhino-sinusienne": {
            "Chirurgie sinusienne (Polypose/Sinusite)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Méatotomie / Ethmoidectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Chirurgie rhinologique SANS greffon": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Chirurgie rhinologique AVEC greffon": {"molecule": "Céfazoline (Alternative: Amoxicilline/Clavulanate)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cef) / > 2h (Amox)", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Reprise chirurgicale rhinologique": {"molecule": "Céfazoline (Alternative: Amoxicilline/Clavulanate)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cef) / > 2h (Amox)", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie sinusienne tumorale": {"molecule": "Céfazoline (Alternative: Amoxicilline/Clavulanate)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cef) / > 2h (Amox)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."}
        },
        "Chirurgie Cervicale & Carcinologique": {
            "Chirurgie carcinologique avec lambeau": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h, puis toutes les 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL (48h max)."},
            "Laryngectomie": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h, puis toutes les 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Pharyngo-laryngectomie": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h, puis toutes les 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Curage cervical": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Cervicotomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Thyroïdectomie totale": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Thyroïdectomie partielle": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Parathyroïdectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Trachéotomie chirurgicale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Trachéotomie percutanée": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie des glandes salivaires": {
            "Glandes salivaires SANS accès buccal": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Glandes salivaires AVEC accès buccal": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."}
        },
        "Chirurgie amygdalienne": {
            "Amygdalectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Adénoïdectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie otologique": {
            "Tympanoplastie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Myringoplastie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Tympanotomie exploratrice": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Chirurgie de la chaine ossiculaire": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Stapédectomie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Chirurgie de cholestéatome (non infecté)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Implants cochléaires": {"molecule": "Céfazoline (Alternative: Amoxicilline/Clavulanate)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cef) / > 2h (Amox)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."}
        },
        "Laryngoscopie": {
            "Laryngoscopie en suspension (Diagnostique)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Laryngoscopie en suspension (Thérapeutique)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "Stomatologie & Chirurgie Maxillo-Faciale": {
        "Chirurgie orthognatique": {
            "Chirurgie orthognatique": {"molecule": "Céfazoline (Alternative: Amoxicilline/Clavulanate)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cef) ou > 2h (Amox)", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL. \nRemarque: Poursuivre 48h postop max."},
            "Ablation de matériel d'ostéosynthèse": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie alvéolo-dentaire": {
            "Extractions de dents incluses": {"molecule": "Amoxicilline", "dose": "2g IVL (ou 2g per os 1-2h avant)", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 600mg per os ou 900mg IVL."},
            "Extractions de dents ectopiques": {"molecule": "Amoxicilline", "dose": "2g IVL (ou 2g per os 1-2h avant)", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 600mg per os ou 900mg IVL."},
            "Désinclusion dentaire": {"molecule": "Amoxicilline", "dose": "2g IVL (ou 2g per os 1-2h avant)", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 600mg per os ou 900mg IVL."},
            "Extractions de dents sur arcade": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Pose de matériel d'ancrage orthodontique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis experts", "allergie": "N/A"},
            "Chirurgie apicale": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis experts", "allergie": "N/A"},
            "Greffe osseuse d'apposition": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL. \nRemarque: Poursuivre 24h max."},
            "Sinus lift": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL. \nRemarque: Poursuivre 24h max."}
        },
        "Traumatologie maxillo-faciale": {
            "Fracture de mandibule (ouverte ou fermée)": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline)", "dose": "2g IVL", "reinjection": "1g si > 2h (Amox) / > 4h (Cef)", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL. \nRemarque: Poursuivre 24h postop max."},
            "Fractures du massif facial (Lefort, Zygoma...)": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline)", "dose": "2g IVL", "reinjection": "1g si > 2h (Amox) / > 4h (Cef)", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL. \nRemarque: Poursuivre 24h postop max."}
        }
    },
    "Ophtalmologie": {
        "Chirurgie du globe oculaire": {
            "Chirurgie de la cataracte simple": {"molecule": "Céfuroxime (Injection intra-camérulaire)", "dose": "1mg dans 0.1 mL", "reinjection": "Dose unique fin intervention", "grade": "GRADE 1", "allergie": "Si allergie : Moxifloxacine intra-camérulaire (0.48mg/0.3mL)."},
            "Chirurgie de la cataracte combinée": {"molecule": "Céfuroxime (Injection intra-camérulaire)", "dose": "1mg dans 0.1 mL", "reinjection": "Dose unique fin intervention", "grade": "GRADE 1", "allergie": "Si allergie : Moxifloxacine intra-camérulaire."},
            "Chirurgie de la cornée": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Remarque: Si combiné cataracte -> voir Cataracte."},
            "Chirurgie du glaucome": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Remarque: Si combiné cataracte -> voir Cataracte."},
            "Chirurgie de la rétine et du vitré": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Remarque: Si combiné cataracte -> voir Cataracte."},
            "Traumatismes à globe ouvert": {"molecule": "Vancomycine + Ceftazidime (Injection intra-vitréenne)", "dose": "1mg + 2.25mg (IVT)", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "Si allergie Ceftazidime : Amikacine 0.4mg intra-vitréenne. Pas d'AB systémique."}
        },
        "Chirurgie péri-oculaire": {
            "Chirurgie des paupières": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Chirurgie des voies lacrymales": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Chirurgie du strabisme": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Chirurgie de l'orbite": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"}
        }
    },
    "Chirurgie Thoracique & Pneumologie": {
        "Chirurgie d'exérèse pulmonaire": {
            "Pneumonectomie": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1 (GRADE 2 pour Amox/Clav si BPCO)", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Lobectomie pulmonaire": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Pleuro-pneumonectomie": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Exérèse partielle (Wedge)": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Segmentectomie pulmonaire": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Réduction de volume pulmonaire": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Résection de bulle d'emphysème": {"molecule": "Choix 1 : Amox-Clav (Si BPCO) / Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Exérèse de kyste hydatique": {"molecule": "Choix 1 : Amoxicilline/Clavulanate\nOU Choix 2 : Céfazoline", "dose": "2g (Amox) / 2g (Cefaz)", "reinjection": "Amox: 1g/2h | Cefaz: 1g/4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."}
        },
        "Chirurgies médiastinales": {
            "Chirurgie du médiastin": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL (ou 1.5g IVL)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Chirurgie du pneumothorax": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL (ou 1.5g IVL)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Chirurgie de la plèvre": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL (ou 1.5g IVL)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Chirurgie de paroi thoracique": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL (ou 1.5g IVL)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Médiastinoscopie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Thoracoscopie / Pleuroscopie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Drainage thoracique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Voies aériennes & Oesophage": {
            "Trachéotomie chirurgicale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Suture de bronche ou trachée": {"molecule": "Céfazoline (Alternative: Amox-Clav)", "dose": "2g IVL", "reinjection": "Cefaz: 4h | Amox: 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Résection-anastomose (bronche/trachée)": {"molecule": "Céfazoline (Alternative: Amox-Clav)", "dose": "2g IVL", "reinjection": "Cefaz: 4h | Amox: 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg IVL."},
            "Trachéotomie percutanée": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Œsophagectomie": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie vraie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Diverticule de l'œsophage": {"molecule": "Céfazoline (Alternative : Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie vraie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."}
        },
        "Procédures Interventionnelles (Pneumo)": {
            "Pose de valves Zéphyr": {"molecule": "Amoxicilline/Clavulanate (Alternative: Pristinamycine)", "dose": "1g IVL (Amox) / 1g per os (Pristina)", "reinjection": "N/A - Poursuivre 48h per os", "grade": "Avis d'experts", "allergie": "Si allergie : Pristinamycine."},
            "Prothèse trachéo-bronchique": {"molecule": "Amoxicilline/Clavulanate (Alternative: Pristinamycine)", "dose": "1g IVL (Amox) / 1g per os (Pristina)", "reinjection": "N/A - Poursuivre 48h per os", "grade": "Avis d'experts", "allergie": "Si allergie : Pristinamycine."},
            "Radiologie interventionnelle (Radiofréquence)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Fibroscopie bronchique / EBUS": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        }
    },
    "Cardiaque & Vasculaire": {
        "Chirurgie Cardiaque": {
            "Chirurgie valvulaire": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL (+1g priming CEC)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Pontages coronariens": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL (+1g priming CEC)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Chirurgie de l'aorte thoracique": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL (+1g priming CEC)", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Drainage péricardique": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Fenêtre pleuropéricardique": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Hémostase postopératoire": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si > 4h (Cefaz) / 0.75g si > 2h (Cefu)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Implantation de Pacemaker": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Implantation de Défibrillateur": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Changement de boitier / sonde": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Transplantation cardiaque": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."}
        },
        "Cardiologie structurelle": {
            "TAVI (Bioprothèse aortique)": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline)", "dose": "2g IVL", "reinjection": "1g si > 2h (Amox) / > 4h (Cefaz)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "MitraClip": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline)", "dose": "2g IVL", "reinjection": "1g si > 2h (Amox) / > 4h (Cefaz)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Fermeture d'auricule / CIA / FOP": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline)", "dose": "2g IVL", "reinjection": "1g si > 2h (Amox) / > 4h (Cefaz)", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Exploration électrophysiologique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE (Sauf si prothèse en place)", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Ablation de trouble du rythme": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE (Sauf si prothèse en place)", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie Vasculaire": {
            "Chirurgie artérielle périphérique": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h (Cefaz)", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine/Teicoplanine OU Clindamycine + Gentamicine."},
            "Chirurgie de l'aorte abdominale": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h (Cefaz)", "grade": "GRADE 1", "allergie": "Si allergie : Vancomycine/Teicoplanine OU Clindamycine + Gentamicine."},
            "Chirurgie carotidienne AVEC matériel": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h (Cefaz)", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine OU Clindamycine + Gentamicine."},
            "Chirurgie carotidienne SANS matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Chirurgie des varices (Scarpa)": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine OU Clindamycine + Gentamicine."},
            "Chirurgie des varices (Sans Scarpa)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Création de FAV avec matériel": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine OU Clindamycine + Gentamicine."},
            "Création de FAV SANS matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Amputation de membre (Hors septique)": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 600mg toutes les 6h (pendant 48h)."}
        },
        "Radiologie Vasculaire": {
            "Pose de stent couvert / Endoprothèse": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine."},
            "Pose de stent nu (Patient à risque*)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine. *Risque: réintervention <7j, prothèse existante, cathéter >6h."},
            "Pose de stent nu (Patient sans risque)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"}
        }
    },
    "Orthopédie & Traumato": {
        "Chirurgie Programmée (Membre Inférieur)": {
            "Prothèse de hanche": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg. (Si voie antérieure: Vanco/Teico préférables)."},
            "Prothèse de genou": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg."},
            "Ostéotomie / Arthrodèse": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg."},
            "Matériel (clou, vis, plaque)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg."},
            "Ligamentoplastie avec matériel": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg."},
            "Arthroscopie SANS matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Ablation de matériel d'ostéosynthèse": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Sauf cas complexe (Céfazoline)."}
        },
        "Chirurgie Programmée (Membre Supérieur)": {
            "Prothèse d'épaule": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico préférables (Cutibacterium)."},
            "Prothèse de coude": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico préférables."},
            "Chirurgie de luxation récidivante / Butée": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico préférables."},
            "Matériel osseux épaule/coude": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico préférables."},
            "Arthroscopie épaule/coude SANS matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie du Rachis (Orthopédique)": {
            "Chirurgie instrumentée (1 temps)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie instrumentée (2 temps)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Cimentoplastie / Expansion": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Chirurgie sans matériel": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Traumatologie": {
            "Fracture fermée (Ostéosynthèse)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Fracture fermée (Enclouage)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Fracture ouverte Gustilo 1": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg."},
            "Fracture ouverte Gustilo 2 ou 3": {"molecule": "Amoxicilline/Clavulanate (Alternative: Céfazoline + Gentamicine)", "dose": "2g IVL", "reinjection": "1g si durée > 2h (Amox)", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg."},
            "Plaie souillée (tellurique/fécale)": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg."},
            "Plaie articulaire": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg."},
            "Morsure": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Clindamycine 900mg + Gentamicine 6-7mg/kg. (Traitement curatif 5 jours)."}
        }
    },
    "Chirurgie Digestive": {
        "Chirurgie Œso-Gastrique": {
            "Gastrectomie totale": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico."},
            "Gastrectomie partielle": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico."}
        },
        "Chirurgie Bariatrique": {
            "Anneau gastrique": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine 20mg/kg ou Teicoplanine 12mg/kg."},
            "Bypass gastrique": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "Sleeve gastrectomie": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."}
        },
        "Chirurgie Colorectale": {
            "Colectomie": {"molecule": "Céfoxitine (Per-op) + Tobramycine/Métronidazole (Veille)", "dose": "2g IVL (Céfoxitine)", "reinjection": "1g si durée > 2h (Céfoxitine)", "grade": "GRADE 1", "allergie": "Si allergie Céfoxitine: Gentamicine 6-7mg/kg + Métronidazole 1g IVL."},
            "Proctectomie": {"molecule": "Céfoxitine (Per-op) + Tobramycine/Métronidazole (Veille)", "dose": "2g IVL (Céfoxitine)", "reinjection": "1g si durée > 2h (Céfoxitine)", "grade": "GRADE 1", "allergie": "Si allergie Céfoxitine: Gentamicine 6-7mg/kg + Métronidazole 1g IVL."},
            "Rétablissement de continuité": {"molecule": "Céfoxitine (Per-op) + Tobramycine/Métronidazole (Veille)", "dose": "2g IVL (Céfoxitine)", "reinjection": "1g si durée > 2h (Céfoxitine)", "grade": "GRADE 1", "allergie": "Si allergie Céfoxitine: Gentamicine 6-7mg/kg + Métronidazole 1g IVL."},
            "Appendicectomie": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."}
        },
        "Chirurgie Hépato-Biliaire": {
            "Cholecystectomie simple (Coelioscopie)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Cholecystectomie à risque / Laparotomie": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine/Teicoplanine."},
            "Hépatectomie sans chirurgie biliaire": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vancomycine/Teicoplanine."},
            "Anastomose bilio-digestive": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "Splénectomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Vanco/Teico."}
        },
        "Chirurgie Pancréatique": {
            "DPC (Sans drainage préop)": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "DPC (Avec drainage préop)": {"molecule": "Pipéracilline + Tazobactam", "dose": "4g IVL", "reinjection": "2g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "Pancréatectomie Gauche / Totale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vanco/Teico."}
        },
        "Chirurgie de Paroi & Proctologie": {
            "Cure de hernie inguinale AVEC prothèse": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Vancomycine/Teicoplanine."},
            "Cure de hernie inguinale SANS prothèse": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"},
            "Hémorroïdes": {"molecule": "Métronidazole", "dose": "1g IVL", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "N/A"},
            "Kyste pilonidal / Fistule anale": {"molecule": "Métronidazole", "dose": "1g IVL", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Endoscopie & Radiologie Digestive": {
            "CPRE (Drainage complet)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "CPRE (Drainage incomplet)": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "Si allergie : Genta + Metro."},
            "Gastrostomie percutanée (PEG)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "Dose unique", "grade": "GRADE 1", "allergie": "Si allergie : Vanco/Teico."},
            "Coloscopie diagnostique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"}
        }
    },
    "Urologie": {
        "Chirurgie de la Prostate": {
            "RTUP (Résection Prostate)": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Adénomectomie chirurgicale": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Laser prostate (HoLEP, ThuLEP...)": {"molecule": "Céfazoline (Alternative: Céfuroxime)", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Biopsies de prostate": {"molecule": "Fosfomycine-trométamol (Alternative: Ciprofloxacine)", "dose": "3g per os (Fosfo) 2h avant", "reinjection": "Dose unique", "grade": "GRADE 1", "allergie": "Si allergie Fosfo : Ciprofloxacine 500mg per os."},
            "Prostatectomie totale": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie de la Vessie": {
            "Cystoscopie diagnostique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "RTUV (Résection Vessie)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Cystectomie (Totale/Partielle)": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."}
        },
        "Voies Excrétrices & Reins": {
            "Urétéroscopie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 1", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Néphrolithotomie percutanée": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Sonde JJ / Néphrostomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine 6-7mg/kg."},
            "Lithotritie extra-corporelle (LEC)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"}
        },
        "Organes Génitaux": {
            "Implant prothèse pénienne": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Clindamycine."},
            "Implant prothèse testiculaire": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Clindamycine."},
            "Chirurgie scrotale sans prothèse": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Cure de prolapsus": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Clindamycine."}
        }
    },
    "Chirurgie Plastique, Reconstructrice & Esthétique": {
        "Chirurgie du Sein": {
            "Tumorectomie sans curage": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Tumorectomie avec ganglion sentinelle": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Tumorectomie avec curage axillaire": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Mastectomie sans reconstruction": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Mastectomie avec reconstruction": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Augmentation mammaire (prothèse)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Lipofilling mammaire (>200cc ou >2h)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Réduction mammaire": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Mastopexie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie de Silhouette": {
            "Abdominoplastie > 2h": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Abdominoplastie < 2h": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Body-lift": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Cruroplastie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Lipoaspiration isolée": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Chirurgie de la Face": {
            "Rhinoplastie avec greffe": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine ou Vancomycine/Teicoplanine."},
            "Lifting cervico-facial > 2h": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine ou Vancomycine/Teicoplanine."},
            "Otoplastie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Blépharoplastie": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Affirmation de Genre": {
            "Vaginoplastie": {"molecule": "Amoxicilline/Clavulanate", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "Colo-Vaginoplastie": {"molecule": "Céfoxitine (+ Tobra/Metro veille)", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "GRADE 1", "allergie": "Si allergie : Gentamicine + Métronidazole."},
            "Phalloplastie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."}
        },
        "Brûlés": {
            "Pansement / Excision": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Greffe matrice artificielle": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine ou Vanco/Teico."},
            "Autogreffe cutanée": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "Sauf cas particulier (bactériologie)."}
        }
    },
    "Gynécologie & Obstétrique": {
        "Chirurgie des Annexes": {
            "Cœlioscopie diagnostique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Ligature de trompe / Détorsion": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Kystectomie ovarienne": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Annexectomie (Coelioscopie)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine."},
            "Annexectomie (Laparotomie)": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine."},
            "Résection endométriose rectale": {"molecule": "Céfazoline + Métronidazole", "dose": "2g + 1g", "reinjection": "1g (Cef) si > 4h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine + Gentamicine."}
        },
        "Chirurgie de l'Utérus": {
            "Hystérectomie totale (Coelio/Laparo)": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine + Gentamicine."},
            "Hystérectomie vaginale": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine + Gentamicine."},
            "Hystérectomie subtotale": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine."},
            "Myomectomie": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine."},
            "Conisation": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"},
            "Cerclage du col": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Hystéroscopie & Curetage": {
            "Hystéroscopie diagnostique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Curetage thérapeutique": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Resection de Polype / Myome": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Pose de DIU": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "Obstétrique": {
            "Césarienne programmée": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Césarienne en urgence": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "1g si durée > 4h", "grade": "GRADE 2", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Délivrance artificielle": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Révision utérine": {"molecule": "Céfazoline", "dose": "2g IVL", "reinjection": "Dose unique", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine 900mg IVL."},
            "Hystérectomie d'hémostase": {"molecule": "Céfoxitine", "dose": "2g IVL", "reinjection": "1g si durée > 2h", "grade": "Avis d'experts", "allergie": "Si allergie : Clindamycine + Gentamicine."},
            "Curetage post-partum": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "Avis d'experts", "allergie": "N/A"}
        },
        "PMA & IVG": {
            "Ponction ovocytes": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "Transfert d'embryon": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 1", "allergie": "N/A"},
            "IVG par aspiration (1er trimestre)": {"molecule": "PAS D'ANTIBIOPROPHYLAXIE", "dose": "N/A", "reinjection": "N/A", "grade": "GRADE 2", "allergie": "N/A"}
        }
    }
}

KV_STR = '''
ScreenManager:
    HomeScreen:
    CategoryScreen:
    DetailScreen:

<HomeScreen>:
    name: 'home'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Antibio SFAR 2024"
            right_action_items: [["information-outline", lambda x: app.show_info()]]
        MDScrollView:
            MDList:
                id: spec_list

<CategoryScreen>:
    name: 'category'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: root.title_text
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        MDScrollView:
            MDList:
                id: cat_list

<DetailScreen>:
    name: 'detail'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Détails"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)
            
            MDLabel:
                text: "Choisissez l'intervention :"
                font_style: "Subtitle1"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: self.texture_size[1]
                
            MDRaisedButton:
                id: drop_item
                text: "Sélectionner..."
                pos_hint: {'center_x': .5}
                on_release: app.open_menu(self)

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(5)
                    elevation: 2
                    
                    MDLabel:
                        text: "Molécule"
                        font_style: "Caption"
                        theme_text_color: "Hint"
                    MDLabel:
                        id: lbl_molecule
                        text: "---"
                        font_style: "H6"
                        theme_text_color: "Primary"

                    MDLabel:
                        text: "Dose"
                        font_style: "Caption"
                        theme_text_color: "Hint"
                    MDLabel:
                        id: lbl_dose
                        text: "---"
                        font_style: "Body1"

                    MDLabel:
                        text: "Réinjection"
                        font_style: "Caption"
                        theme_text_color: "Hint"
                    MDLabel:
                        id: lbl_reinjection
                        text: "---"
                        font_style: "Body1"
                        
                    MDLabel:
                        text: "Allergie / Remarques"
                        font_style: "Caption"
                        theme_text_color: "Error"
                    MDLabel:
                        id: lbl_allergie
                        text: "---"
                        font_style: "Body2"
            
            Widget:
'''

class HomeScreen(Screen):
    def on_enter(self):
        self.ids.spec_list.clear_widgets()
        for spec in SFAR_DATA.keys():
            item = OneLineIconListItem(text=spec, on_release=self.select_spec)
            icon = IconLeftWidget(icon="doctor")
            item.add_widget(icon)
            self.ids.spec_list.add_widget(item)

    def select_spec(self, instance):
        app = MDApp.get_running_app()
        app.current_spec = instance.text
        app.root.current = 'category'

class CategoryScreen(Screen):
    title_text = StringProperty("Catégories")

    def on_enter(self):
        app = MDApp.get_running_app()
        self.title_text = app.current_spec
        self.ids.cat_list.clear_widgets()
        
        cats = SFAR_DATA.get(app.current_spec, {})
        for cat in cats.keys():
            item = OneLineIconListItem(text=cat, on_release=self.select_cat)
            icon = IconLeftWidget(icon="folder-outline")
            item.add_widget(icon)
            self.ids.cat_list.add_widget(item)

    def select_cat(self, instance):
        app = MDApp.get_running_app()
        app.current_cat = instance.text
        app.root.current = 'detail'

    def go_back(self):
        MDApp.get_running_app().root.current = 'home'

class DetailScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        # Reset labels
        self.ids.drop_item.text = "Sélectionner..."
        self.ids.lbl_molecule.text = "---"
        self.ids.lbl_dose.text = "---"
        self.ids.lbl_reinjection.text = "---"
        self.ids.lbl_allergie.text = "---"
        app.create_menu(self.ids.drop_item)

    def go_back(self):
        MDApp.get_running_app().root.current = 'category'

class AntibioApp(MDApp):
    current_spec = ""
    current_cat = ""
    menu = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV_STR)

    def create_menu(self, caller):
        interventions = list(SFAR_DATA[self.current_spec][self.current_cat].keys())
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in interventions
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )

    def open_menu(self, caller):
        if self.menu:
            self.menu.open()

    def menu_callback(self, text_item):
        self.root.get_screen('detail').ids.drop_item.text = text_item
        self.menu.dismiss()
        self.update_data(text_item)

    def update_data(self, intervention):
        data = SFAR_DATA[self.current_spec][self.current_cat][intervention]
        screen = self.root.get_screen('detail')
        screen.ids.lbl_molecule.text = data["molecule"]
        screen.ids.lbl_dose.text = data["dose"]
        screen.ids.lbl_reinjection.text = data["reinjection"]
        screen.ids.lbl_allergie.text = data["allergie"]

    def show_info(self):
        text = ""
        for k, v in RFE_GENERALES.items():
            text += f"[b]{v['titre']}[/b]\n{v['reco']}\n\n"
            
        self.dialog = MDDialog(
            title="Recommandations Générales",
            text=text,
            buttons=[MDFlatButton(text="FERMER", on_release=lambda x: self.dialog.dismiss())],
        )
        self.dialog.open()

if __name__ == "__main__":
    AntibioApp().run()