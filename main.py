"""
MediMind AI
Interfaz grafica mejorada para sistema experto medico con Prolog.
Requiere: pyswip, customtkinter, SWI-Prolog instalado.
"""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
from pyswip import Prolog


class MediMindAI:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("medimind_ai.pl")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("MediMind AI - Diagnostico y Seguimiento")
        self.root.geometry("1450x880")
        self.root.minsize(1280, 780)

        self.patient_name = ctk.StringVar()
        self.learned_symptom = ctk.StringVar()
        self.history_patient = ctk.StringVar()
        self.symptom_vars = {}
        self.output_boxes = []

        self.base_symptoms = [
            "fiebre", "tos", "dificultad_respiratoria", "dolor_garganta", "congestion_nasal",
            "estornudos", "dolor_cabeza", "fatiga", "dolor_muscular", "nauseas",
            "vomitos", "diarrea", "dolor_pecho", "sensibilidad_luz", "erupcion_cutanea",
            "picazon_ojos", "perdida_olfato", "sed_excesiva", "miccion_frecuente",
            "vision_borrosa", "dolor_abdominal", "escalofrios", "rigidez_cuello",
            "sibilancias", "presion_arterial_alta"
        ]

        self.build_ui()
        self.refresh_catalogs()
        self.clear_outputs()

    def build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self.root, corner_radius=18)
        left.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)

        right = ctk.CTkFrame(self.root, corner_radius=18)
        right.grid(row=0, column=1, padx=(0, 16), pady=16, sticky="nsew")
        right.grid_columnconfigure((0, 1), weight=1)
        right.grid_rowconfigure(2, weight=1)
        right.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(left, fg_color="transparent")
        header.grid(row=0, column=0, padx=16, pady=(18, 6), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="MediMind AI", font=("Segoe UI", 28, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Diagnostico, seguimiento y explicabilidad clinica", font=("Segoe UI", 13)).grid(row=1, column=0, sticky="w", pady=(2, 0))

        patient_frame = ctk.CTkFrame(left)
        patient_frame.grid(row=1, column=0, padx=16, pady=8, sticky="ew")
        patient_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(patient_frame, text="Datos del paciente", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")
        ctk.CTkEntry(patient_frame, textvariable=self.patient_name, placeholder_text="Nombre del paciente").grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")

        symptoms_frame = ctk.CTkScrollableFrame(left, label_text="Seleccion de sintomas", corner_radius=16)
        symptoms_frame.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")
        symptoms_frame.grid_columnconfigure((0, 1), weight=1)

        for idx, symptom in enumerate(self.base_symptoms):
            var = ctk.BooleanVar(value=False)
            self.symptom_vars[symptom] = var
            cb = ctk.CTkCheckBox(symptoms_frame, text=symptom.replace("_", " ").title(), variable=var)
            cb.grid(row=idx // 2, column=idx % 2, padx=10, pady=6, sticky="w")

        actions = ctk.CTkTabview(left)
        actions.grid(row=3, column=0, padx=16, pady=(8, 16), sticky="ew")
        actions.add("Consultas")
        actions.add("Dinamica")
        actions.add("Historial")

        qtab = actions.tab("Consultas")
        qtab.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkButton(qtab, text="Diagnosticar", command=self.run_diagnosis).grid(row=0, column=0, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Posibles enfermedades", command=self.show_possible_diseases).grid(row=0, column=1, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Riesgo y urgencia", command=self.show_risk).grid(row=0, column=2, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Recomendacion", command=self.show_recommendation).grid(row=1, column=0, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Prediccion preventiva", command=self.show_prediction).grid(row=1, column=1, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Comparar diagnosticos", command=self.compare_diagnoses).grid(row=1, column=2, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Limpiar seleccion", command=self.clear_selection).grid(row=2, column=0, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Limpiar paneles", command=self.clear_outputs).grid(row=2, column=1, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(qtab, text="Registrar consulta", command=self.register_only).grid(row=2, column=2, padx=6, pady=8, sticky="ew")

        dtab = actions.tab("Dinamica")
        dtab.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkEntry(dtab, textvariable=self.learned_symptom, placeholder_text="Nuevo sintoma aprendido").grid(row=0, column=0, padx=8, pady=10, sticky="ew")
        ctk.CTkButton(dtab, text="Agregar sintoma", command=self.add_symptom).grid(row=0, column=1, padx=8, pady=10, sticky="ew")
        ctk.CTkButton(dtab, text="Eliminar sintoma aprendido", command=self.remove_symptom).grid(row=1, column=0, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(dtab, text="Mostrar enfermedades", command=self.show_diseases_catalog).grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(dtab, text="Mostrar tratamientos", command=self.show_treatments_catalog).grid(row=2, column=0, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(dtab, text="Mostrar estadisticas", command=self.show_statistics).grid(row=2, column=1, padx=8, pady=8, sticky="ew")

        htab = actions.tab("Historial")
        htab.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkEntry(htab, textvariable=self.history_patient, placeholder_text="Paciente para consultar o borrar historial").grid(row=0, column=0, columnspan=3, padx=8, pady=10, sticky="ew")
        ctk.CTkButton(htab, text="Consultar historial", command=self.load_history).grid(row=1, column=0, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(htab, text="Borrado logico", command=self.logical_delete).grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(htab, text="Borrado fisico", command=self.physical_delete).grid(row=1, column=2, padx=8, pady=8, sticky="ew")

        ctk.CTkLabel(right, text="Panel clinico", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, columnspan=2, padx=16, pady=(18, 6), sticky="w")

        self.summary_box = self.create_output_box(right, 1, 0, "Resumen diagnostico")
        self.alert_box = self.create_output_box(right, 1, 1, "Riesgo, prediccion y alertas")
        self.explain_box = self.create_output_box(right, 2, 0, "Explicacion del razonamiento")
        self.history_box = self.create_output_box(right, 2, 1, "Historial del paciente")
        self.catalog_box = self.create_output_box(right, 3, 0, "Catalogo del sistema")
        self.recommend_box = self.create_output_box(right, 3, 1, "Recomendaciones y acciones")

    def create_output_box(self, parent, row, column, title):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=column, padx=12, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 16, "bold")).grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")
        box = ctk.CTkTextbox(frame, corner_radius=12, wrap="word")
        box.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.output_boxes.append(box)
        return box

    def set_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.configure(state="disabled")

    def clear_outputs(self):
        for box in self.output_boxes:
            self.set_text(box, "Panel listo para mostrar resultados.")

    def selected_symptoms(self):
        return [name for name, var in self.symptom_vars.items() if var.get()]

    def clear_selection(self):
        for var in self.symptom_vars.values():
            var.set(False)

    def prolog_atom(self, text):
        return text.strip().lower().replace(" ", "_")

    def prolog_list(self, items):
        return "[" + ",".join(items) + "]"

    def query_one(self, query):
        results = list(self.prolog.query(query))
        return results[0] if results else None

    def validate_patient_symptoms(self):
        patient = self.patient_name.get().strip()
        symptoms = self.selected_symptoms()
        if not patient:
            messagebox.showwarning("Validacion", "Ingrese el nombre del paciente.")
            return None, None
        if not symptoms:
            messagebox.showwarning("Validacion", "Seleccione al menos un sintoma.")
            return None, None
        return patient, symptoms

    def validate_symptoms_only(self):
        symptoms = self.selected_symptoms()
        if not symptoms:
            messagebox.showwarning("Validacion", "Seleccione al menos un sintoma.")
            return None
        return symptoms

    def run_diagnosis(self):
        patient, symptoms = self.validate_patient_symptoms()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        diag = self.query_one(f"diagnostico_principal({s_list},E,P,N,R,T,EX)")
        expl = self.query_one(f"explicacion_diagnostico({s_list},Texto)")
        rec = self.query_one(f"recomendacion_medica({s_list},Reco)")
        pred = self.query_one(f"prediccion_preventiva({s_list},Alerta)")
        urg = self.query_one(f"riesgo_urgencia({s_list},Urgencia,Puntaje)")
        poss = self.query_one(f"posibles_enfermedades({s_list},Lista)")
        comp = self.query_one(f"comparar_diagnosticos({s_list},C)")

        if not diag:
            self.set_text(self.summary_box, "No se encontro un diagnostico con evidencia suficiente.")
            self.set_text(self.explain_box, "Agregue mas sintomas o amplie la base de conocimiento dinamica.")
            return

        list(self.prolog.query(f"registrar_consulta({self.prolog_atom(patient)},{s_list})"))

        summary = (
            f"Paciente: {patient}\n"
            f"Diagnostico principal: {diag['E']}\n"
            f"Coincidencia: {diag['P']}%\n"
            f"Nivel de confianza: {diag['N']}\n"
            f"Riesgo base: {diag['R']}\n"
            f"Tratamiento base: {diag['T']}"
        )
        alerts = (
            f"Urgencia estimada: {urg['Urgencia']} (puntaje {urg['Puntaje']})\n\n"
            f"Prediccion preventiva:\n{pred['Alerta']}\n\n"
            f"Comparacion diagnostica:\n{comp['C']}"
        )
        explain = f"{expl['Texto']}\n\nPosibles enfermedades relacionadas:\n{poss['Lista']}"
        recommend = rec['Reco']

        self.set_text(self.summary_box, summary)
        self.set_text(self.alert_box, alerts)
        self.set_text(self.explain_box, explain)
        self.set_text(self.recommend_box, recommend)
        self.load_history(auto=True)
        self.refresh_catalogs()

    def register_only(self):
        patient, symptoms = self.validate_patient_symptoms()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        if self.query_one(f"diagnostico_principal({s_list},E,P,N,R,T,EX)"):
            list(self.prolog.query(f"registrar_consulta({self.prolog_atom(patient)},{s_list})"))
            self.set_text(self.recommend_box, "Consulta registrada correctamente en el historial dinamico.")
            self.load_history(auto=True)
            self.refresh_catalogs()
        else:
            messagebox.showinfo("Registro", "No se puede registrar sin un diagnostico minimo compatible.")

    def show_possible_diseases(self):
        symptoms = self.validate_symptoms_only()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        poss = self.query_one(f"posibles_enfermedades({s_list},Lista)")
        self.set_text(self.explain_box, f"Posibles enfermedades relacionadas:\n\n{poss['Lista'] if poss else []}")

    def show_risk(self):
        symptoms = self.validate_symptoms_only()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        urg = self.query_one(f"riesgo_urgencia({s_list},Urgencia,Puntaje)")
        if urg:
            self.set_text(self.alert_box, f"Nivel de urgencia: {urg['Urgencia']}\nPuntaje acumulado: {urg['Puntaje']}")
        else:
            self.set_text(self.alert_box, "No se pudo calcular urgencia con la seleccion actual.")

    def show_recommendation(self):
        symptoms = self.validate_symptoms_only()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        rec = self.query_one(f"recomendacion_medica({s_list},Reco)")
        self.set_text(self.recommend_box, rec['Reco'] if rec else "No hay recomendacion para la combinacion actual.")

    def show_prediction(self):
        symptoms = self.validate_symptoms_only()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        pred = self.query_one(f"prediccion_preventiva({s_list},Alerta)")
        self.set_text(self.alert_box, pred['Alerta'] if pred else "No se genero alerta preventiva.")

    def compare_diagnoses(self):
        symptoms = self.validate_symptoms_only()
        if not symptoms:
            return
        s_list = self.prolog_list(symptoms)
        comp = self.query_one(f"comparar_diagnosticos({s_list},C)")
        self.set_text(self.explain_box, f"Comparacion de diagnosticos alternativos:\n\n{comp['C'] if comp else []}")

    def load_history(self, auto=False):
        patient = self.patient_name.get().strip().lower() or self.history_patient.get().strip().lower()
        if not patient:
            if not auto:
                self.set_text(self.history_box, "Ingrese un nombre para consultar historial.")
            return
        result = self.query_one(f"consultar_historial({self.prolog_atom(patient)},Registros)")
        self.set_text(self.history_box, f"Historial de {patient}:\n\n{result['Registros'] if result else 'Sin historial disponible.'}")

    def add_symptom(self):
        symptom = self.prolog_atom(self.learned_symptom.get())
        if not symptom:
            messagebox.showwarning("Validacion", "Ingrese un sintoma nuevo.")
            return
        list(self.prolog.query(f"agregar_sintoma_dinamico({symptom})"))
        self.learned_symptom.set("")
        self.refresh_catalogs()
        self.set_text(self.catalog_box, f"Sintoma aprendido agregado correctamente: {symptom}\n\n" + self.current_catalog_text())

    def remove_symptom(self):
        symptom = self.prolog_atom(self.learned_symptom.get())
        if not symptom:
            messagebox.showwarning("Validacion", "Ingrese un sintoma para eliminar.")
            return
        list(self.prolog.query(f"eliminar_sintoma_aprendido({symptom})"))
        self.learned_symptom.set("")
        self.refresh_catalogs()
        self.set_text(self.catalog_box, f"Solicitud de eliminacion procesada para: {symptom}\n\n" + self.current_catalog_text())

    def logical_delete(self):
        patient = self.history_patient.get().strip()
        if not patient:
            messagebox.showwarning("Validacion", "Ingrese el paciente para borrado logico.")
            return
        list(self.prolog.query(f"borrado_logico_historial({self.prolog_atom(patient)},solicitud_usuario)"))
        self.set_text(self.history_box, f"Se aplico borrado logico sobre el historial de {patient}.")
        self.refresh_catalogs()

    def physical_delete(self):
        patient = self.history_patient.get().strip()
        if not patient:
            messagebox.showwarning("Validacion", "Ingrese el paciente para borrado fisico.")
            return
        confirm = messagebox.askyesno("Confirmacion", "Este borrado elimina completamente el historial. Desea continuar?")
        if not confirm:
            return
        list(self.prolog.query(f"borrado_fisico_historial({self.prolog_atom(patient)})"))
        self.set_text(self.history_box, f"Se aplico borrado fisico completo sobre {patient}.")
        self.refresh_catalogs()

    def show_diseases_catalog(self):
        diseases = self.query_one("mostrar_enfermedades(L)")
        self.set_text(self.catalog_box, f"Enfermedades registradas:\n\n{diseases['L'] if diseases else []}")

    def show_treatments_catalog(self):
        treatments = self.query_one("mostrar_tratamientos(T)")
        self.set_text(self.catalog_box, f"Tratamientos disponibles:\n\n{treatments['T'] if treatments else []}")

    def show_statistics(self):
        stats = self.query_one("estadisticas_consultas(Total,Pacientes)")
        text = (
            f"Estadisticas del sistema:\n\n"
            f"Consultas totales: {stats['Total'] if stats else 0}\n"
            f"Pacientes unicos: {stats['Pacientes'] if stats else 0}"
        )
        self.set_text(self.catalog_box, text)

    def current_catalog_text(self):
        diseases = self.query_one("mostrar_enfermedades(L)")
        treatments = self.query_one("mostrar_tratamientos(T)")
        stats = self.query_one("estadisticas_consultas(Total,Pacientes)")
        learned = list(self.prolog.query("sintoma_aprendido(S)"))
        learned_list = [x["S"] for x in learned]
        return (
            f"Enfermedades registradas:\n{diseases['L'] if diseases else []}\n\n"
            f"Tratamientos disponibles:\n{treatments['T'] if treatments else []}\n\n"
            f"Sintomas aprendidos:\n{learned_list}\n\n"
            f"Consultas totales: {stats['Total'] if stats else 0}\n"
            f"Pacientes unicos: {stats['Pacientes'] if stats else 0}"
        )

    def refresh_catalogs(self):
        self.set_text(self.catalog_box, self.current_catalog_text())

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MediMindAI()
    app.run()
