:- dynamic historial/7.
:- dynamic sintoma_aprendido/1.
:- dynamic enfermedad_aprendida/4.
:- dynamic consulta_realizada/4.
:- dynamic historial_logico/8.

% =========================
% Base de conocimiento
% =========================

sintoma(fiebre).
sintoma(tos).
sintoma(dificultad_respiratoria).
sintoma(dolor_garganta).
sintoma(congestion_nasal).
sintoma(estornudos).
sintoma(dolor_cabeza).
sintoma(fatiga).
sintoma(dolor_muscular).
sintoma(nauseas).
sintoma(vomitos).
sintoma(diarrea).
sintoma(dolor_pecho).
sintoma(sensibilidad_luz).
sintoma(erupcion_cutanea).
sintoma(picazon_ojos).
sintoma(perdida_olfato).
sintoma(sed_excesiva).
sintoma(miccion_frecuente).
sintoma(vision_borrosa).
sintoma(dolor_abdominal).
sintoma(escalofrios).
sintoma(rigidez_cuello).
sintoma(sibilancias).
sintoma(presion_arterial_alta).

tratamiento(gripe, 'Reposo, hidratacion, control de fiebre y vigilancia en casa.').
tratamiento(covid19, 'Aislamiento, control de saturacion, hidratacion y valoracion medica si empeora.').
tratamiento(alergia, 'Antihistaminicos, evitar desencadenantes y lavado nasal.').
tratamiento(migrana, 'Reposo en ambiente oscuro, analgesia prescrita y control de estres.').
tratamiento(gastroenteritis, 'Rehidratacion oral, dieta blanda y vigilancia de signos de deshidratacion.').
tratamiento(neumonia, 'Evaluacion medica inmediata, estudios respiratorios y antibiotico si procede.').
tratamiento(diabetes, 'Control glucemico, alimentacion supervisada y seguimiento clinico continuo.').
tratamiento(hipertension, 'Control de presion, dieta baja en sodio, ejercicio y seguimiento medico.').

categoria_riesgo(gripe, moderado).
categoria_riesgo(covid19, alto).
categoria_riesgo(alergia, bajo).
categoria_riesgo(migrana, moderado).
categoria_riesgo(gastroenteritis, moderado).
categoria_riesgo(neumonia, alto).
categoria_riesgo(diabetes, alto).
categoria_riesgo(hipertension, alto).

factor_urgencia(gripe, 2).
factor_urgencia(covid19, 4).
factor_urgencia(alergia, 1).
factor_urgencia(migrana, 3).
factor_urgencia(gastroenteritis, 3).
factor_urgencia(neumonia, 5).
factor_urgencia(diabetes, 4).
factor_urgencia(hipertension, 4).

% enfermedad(Nombre, SintomasRequeridos, Tratamiento, ExplicacionBase).
enfermedad(gripe,
    [fiebre, tos, dolor_garganta, fatiga, dolor_muscular],
    'Reposo, liquidos, antipireticos bajo indicacion y monitoreo de evolucion.',
    'La gripe combina fiebre, sintomas respiratorios y malestar general musculoesqueletico.').

enfermedad(covid19,
    [fiebre, tos, dificultad_respiratoria, perdida_olfato, fatiga],
    'Aislamiento, seguimiento de oxigenacion y valoracion medica si hay deterioro respiratorio.',
    'COVID-19 se asocia con fiebre, tos y alteraciones respiratorias o del olfato.').

enfermedad(alergia,
    [congestion_nasal, estornudos, picazon_ojos, dolor_garganta],
    'Antihistaminicos, evitar alergenos y limpieza ambiental.',
    'La alergia respiratoria destaca por congestion, estornudos e irritacion ocular.').

enfermedad(migrana,
    [dolor_cabeza, nauseas, sensibilidad_luz, vomitos],
    'Reposo en oscuridad, manejo del dolor y evitar detonantes.',
    'La migrana suele reunir cefalea intensa, nauseas y fotofobia.').

enfermedad(gastroenteritis,
    [diarrea, vomitos, nauseas, dolor_abdominal, fiebre],
    'Rehidratacion y dieta blanda con seguimiento clinico.',
    'La gastroenteritis reune sintomas digestivos agudos con posible fiebre.').

enfermedad(neumonia,
    [fiebre, tos, dificultad_respiratoria, dolor_pecho, escalofrios],
    'Evaluacion inmediata por riesgo respiratorio y posible manejo antibiotico.',
    'La neumonia combina fiebre con compromiso pulmonar y dolor toracico.').

enfermedad(diabetes,
    [sed_excesiva, miccion_frecuente, fatiga, vision_borrosa],
    'Control glucemico y evaluacion medica integral.',
    'La diabetes puede manifestarse con poliuria, sed excesiva y cansancio persistente.').

enfermedad(hipertension,
    [dolor_cabeza, vision_borrosa, dolor_pecho, presion_arterial_alta],
    'Control de presion arterial, cambios de estilo de vida y revision medica.',
    'La hipertension de riesgo puede acompañarse de cefalea, sintomas visuales y elevacion tensional.').

% =========================
% Utilidades
% =========================

miembro(X, [X|_]).
miembro(X, [_|T]) :- miembro(X, T).

contar_coincidencias([], _, 0).
contar_coincidencias([H|T], Lista, N) :-
    miembro(H, Lista),
    contar_coincidencias(T, Lista, N1),
    N is N1 + 1.
contar_coincidencias([H|T], Lista, N) :-
    \+ miembro(H, Lista),
    contar_coincidencias(T, Lista, N).

porcentaje_coincidencia(SintomasPaciente, SintomasEnfermedad, Porcentaje, Coincide, Total) :-
    contar_coincidencias(SintomasEnfermedad, SintomasPaciente, Coincide),
    length(SintomasEnfermedad, Total),
    Total > 0,
    Porcentaje is (Coincide * 100) // Total.

nivel_confianza(Porcentaje, confirmado) :- Porcentaje >= 80.
nivel_confianza(Porcentaje, probable) :- Porcentaje >= 50, Porcentaje < 80.
nivel_confianza(Porcentaje, preventivo) :- Porcentaje >= 25, Porcentaje < 50.

recomendacion_por_riesgo(alto, 'Acudir a valoracion medica prioritaria y evitar automedicacion.').
recomendacion_por_riesgo(moderado, 'Realizar seguimiento de sintomas, hidratacion y consulta si persiste o empeora.').
recomendacion_por_riesgo(bajo, 'Mantener autocuidado, observacion y medidas preventivas generales.').

% =========================
% Motor de inferencia
% =========================

diagnostico_principal(SintomasPaciente, Enfermedad, Porcentaje, Nivel, Riesgo, Tratamiento, Explicacion) :-
    findall([E,P,N,R,T,Ex],
        (
            enfermedad(E, SintomasBase, T, ExpBase),
            porcentaje_coincidencia(SintomasPaciente, SintomasBase, P, Coincide, Total),
            P >= 25,
            nivel_confianza(P, N),
            categoria_riesgo(E, R),
            atomic_list_concat([
                'Coinciden ', Coincide, ' de ', Total,
                ' sintomas clave. ', ExpBase,
                ' Nivel inferido: ', N
            ], ExpLocal),
            Ex = ExpLocal
        ),
        Resultados),
    Resultados \= [],
    mejor_resultado(Resultados, [Enfermedad,Porcentaje,Nivel,Riesgo,Tratamiento,Explicacion]).

mejor_resultado([X], X).
mejor_resultado([[E1,P1,N1,R1,T1,Ex1],[E2,P2,N2,R2,T2,Ex2]|Resto], Mejor) :-
    (P1 >= P2 ->
        mejor_resultado([[E1,P1,N1,R1,T1,Ex1]|Resto], Mejor)
    ;
        mejor_resultado([[E2,P2,N2,R2,T2,Ex2]|Resto], Mejor)
    ).

posibles_enfermedades(SintomasPaciente, Lista) :-
    findall(resultado(E,P,N,R,T,Ex),
        (
            enfermedad(E, SintomasBase, T, ExpBase),
            porcentaje_coincidencia(SintomasPaciente, SintomasBase, P, Coincide, Total),
            P >= 25,
            nivel_confianza(P, N),
            categoria_riesgo(E, R),
            atomic_list_concat([
                'Se detectaron ', Coincide, '/', Total,
                ' sintomas compatibles con ', E, '. ', ExpBase
            ], Ex)
        ),
        Lista).

riesgo_urgencia(SintomasPaciente, NivelUrgencia, Puntaje) :-
    findall(F,
        (
            enfermedad(E, SintomasBase, _, _),
            porcentaje_coincidencia(SintomasPaciente, SintomasBase, P, _, _),
            P >= 50,
            factor_urgencia(E, F)
        ), Factores),
    sumar_lista(Factores, Puntaje),
    clasificar_urgencia(Puntaje, NivelUrgencia).

sumar_lista([], 0).
sumar_lista([H|T], S) :- sumar_lista(T, S1), S is H + S1.

clasificar_urgencia(P, critica) :- P >= 8.
clasificar_urgencia(P, alta) :- P >= 5, P < 8.
clasificar_urgencia(P, media) :- P >= 3, P < 5.
clasificar_urgencia(P, baja) :- P < 3.

explicacion_diagnostico(SintomasPaciente, Texto) :-
    diagnostico_principal(SintomasPaciente, Enfermedad, Porcentaje, Nivel, Riesgo, _, ExpBase),
    riesgo_urgencia(SintomasPaciente, Urgencia, Puntaje),
    atomic_list_concat([
        'Diagnostico principal: ', Enfermedad,
        '. Coincidencia: ', Porcentaje, '%',
        '. Nivel de confianza: ', Nivel,
        '. Riesgo clinico base: ', Riesgo,
        '. Urgencia estimada: ', Urgencia,
        ' (puntaje ', Puntaje, '). ', ExpBase
    ], Texto).

recomendacion_medica(SintomasPaciente, RecomendacionFinal) :-
    diagnostico_principal(SintomasPaciente, Enfermedad, _, _, Riesgo, Tratamiento, _),
    recomendacion_por_riesgo(Riesgo, RecomendacionRiesgo),
    atomic_list_concat([
        'Tratamiento sugerido para ', Enfermedad, ': ', Tratamiento,
        ' Recomendacion general: ', RecomendacionRiesgo
    ], RecomendacionFinal).

prediccion_preventiva(SintomasPaciente, Alerta) :-
    ( miembro(fiebre, SintomasPaciente), miembro(tos, SintomasPaciente), \+ miembro(dificultad_respiratoria, SintomasPaciente) ->
        Alerta = 'Patron preventivo respiratorio: vigilar posible progresion a COVID-19 o neumonia si aparece dificultad respiratoria.'
    ; miembro(sed_excesiva, SintomasPaciente), miembro(fatiga, SintomasPaciente), \+ miembro(miccion_frecuente, SintomasPaciente) ->
        Alerta = 'Patron metabolico preventivo: conviene monitorizar glucosa y aparicion de miccion frecuente.'
    ; miembro(congestion_nasal, SintomasPaciente), miembro(estornudos, SintomasPaciente), \+ miembro(picazon_ojos, SintomasPaciente) ->
        Alerta = 'Patron alergico preventivo: puede evolucionar a alergia respiratoria si aparece irritacion ocular.'
    ; Alerta = 'Sin prediccion preventiva critica con los sintomas actuales.'
    ).

comparar_diagnosticos(SintomasPaciente, Comparacion) :-
    findall(E-P,
        (
            enfermedad(E, SintomasBase, _, _),
            porcentaje_coincidencia(SintomasPaciente, SintomasBase, P, _, _),
            P >= 25
        ),
        Comparacion).

registrar_consulta(Paciente, SintomasPaciente) :-
    diagnostico_principal(SintomasPaciente, Enfermedad, Porcentaje, Nivel, Riesgo, _, _),
    get_time(TS),
    assertz(historial(Paciente, SintomasPaciente, Enfermedad, Porcentaje, Nivel, Riesgo, TS)),
    assertz(consulta_realizada(Paciente, Enfermedad, Porcentaje, TS)).

consultar_historial(Paciente, Registros) :-
    findall(historial(Paciente,S,E,P,N,R,TS), historial(Paciente,S,E,P,N,R,TS), Registros).

agregar_sintoma_dinamico(Sintoma) :-
    \+ sintoma_aprendido(Sintoma),
    assertz(sintoma_aprendido(Sintoma)).

eliminar_sintoma_aprendido(Sintoma) :-
    retract(sintoma_aprendido(Sintoma)).

agregar_enfermedad_dinamica(Nombre, ListaSintomas, Tratamiento, Explicacion) :-
    assertz(enfermedad_aprendida(Nombre, ListaSintomas, Tratamiento, Explicacion)).

mostrar_enfermedades(Lista) :-
    findall(E, enfermedad(E, _, _, _), Base),
    findall(A, enfermedad_aprendida(A, _, _, _), Aprendidas),
    append(Base, Aprendidas, Lista).

mostrar_tratamientos(Lista) :-
    findall(E-T, tratamiento(E, T), Lista).

estadisticas_consultas(Total, PacientesUnicos) :-
    findall(P, consulta_realizada(P, _, _, _), Pacientes),
    length(Pacientes, Total),
    sort(Pacientes, Unicos),
    length(Unicos, PacientesUnicos).

borrado_logico_historial(Paciente, Motivo) :-
    historial(Paciente,S,E,P,N,R,TS),
    assertz(historial_logico(Paciente,S,E,P,N,R,TS,Motivo)),
    retract(historial(Paciente,S,E,P,N,R,TS)),
    fail.
borrado_logico_historial(_, _).

borrado_fisico_historial(Paciente) :-
    retractall(historial(Paciente,_,_,_,_,_,_)),
    retractall(historial_logico(Paciente,_,_,_,_,_,_,_)),
    retractall(consulta_realizada(Paciente,_,_,_)).
