from enum import Enum
from typing import final


@final
class ExcersicePattern(str, Enum):
    DOMINANTE_RODILLA = "Dominante Rodilla"
    DOMINANTE_CADERA = "Dominante Cadera"
    DOMINANTE_CADERA_UNILATERAL = "Dominante Cadera Unilateral"

    UNILATERAL = "Unilateral"

    FLEXION_RODILLA = "Flexión Rodilla"
    EXTENSION_RODILLA = "Extensión Rodilla"

    FLEXION_PLANTAR = "Flexión Plantar"
    EXTENSION_CADERA = "Extensión Cadera"

    ABDUCCION = "Abducción"
    ADUCCION = "Aducción"

    ISOMETRICO = "Isométrico"
    PLIOMETRIA = "Pliometría"
    PLIOMETRICO = "Pliométrico"

    EMPUJE_HORIZONTAL = "Empuje Horizontal"
    EMPUJE_INCLINADO = "Empuje Inclinado"
    EMPUJE_DECLINADO = "Empuje Declinado"
    EMPUJE_UNILATERAL = "Empuje Unilateral"
    EMPUJE_VERTICAL = "Empuje Vertical"
    EMPUJE_VERTICAL_EXPLOSIVO = "Empuje Vertical Explosivo"
    EMPUJE_DIAGONAL = "Empuje Diagonal"
    EMPUJE_DINAMICO = "Empuje Dinámico"

    TRACCION_HORIZONTAL = "Tracción Horizontal"
    TRACCION_HORIZONTAL_UNILATERAL = "Tracción Horizontal Unilateral"
    TRACCION_VERTICAL = "Tracción Vertical"
    TRACCION_PARCIAL = "Tracción Parcial"

    ADUCCION_HORIZONTAL = "Aducción Horizontal"
    ABDUCCION_HORIZONTAL = "Abducción Horizontal"
    ABDUCCION_HOMBRO = "Abducción Hombro"

    EXTENSION_HOMBRO = "Extensión Hombro"
    FLEXION_HOMBRO = "Flexión Hombro"

    ELEVACION_ESCAPULAR = "Elevación Escapular"
    RETRACCION_ESCAPULAR = "Retracción Escapular"
    CONTROL_ESCAPULAR = "Control Escapular"
    ESTABILIDAD_ESCAPULAR = "Estabilidad Escapular"

    EXTENSION_ESPINAL = "Extensión Espinal"

    TRANSPORTE_DE_CARGA = "Transporte de Carga"
    LOCOMOCION = "Locomoción"
    LOCOMOCION_NO_ACCENT = "Locomocion"

    ANTI_ROTACION = "Anti-Rotación"
    ANTIROTACIONAL = "Antirotacional"
    ANTIROTACIONAL_METABOLICO = "Antirotacional / Metabólico"
    ROTACIONAL = "Rotacional"

    FLEXION_DE_CODO = "Flexión de Codo"
    FLEXION_DE_CODO_NEUTRA = "Flexión de Codo Neutra"
    FLEXION_DE_CODO_UNILATERAL = "Flexión de Codo Unilateral"
    EXTENSION_DE_CODO = "Extensión de Codo"

    ROTACION_EXTERNA_EMPUJE = "Rotación Externa + Empuje"

    CORE_ANTERIOR = "Core Anterior"
    CORE_POSTERIOR = "Core Posterior"
    CORE_LATERAL = "Core Lateral"
    CORE_AVANZADO = "Core Avanzado"
    MOVILIDAD_CORE = "Movilidad Core"

    ESTABILIZACION = "Estabilización"
    
    AEROBICO = "Aeróbico"
    ANAEROBICO = "Anaeróbico"
    MIXTO = "Mixto"
    AGILIDAD = "Agilidad"
    CORE_METABOLICO = "Core Metabólico"