CREATE OR REPLACE FUNCTION fn_get_viable_exercises(p_user_id INT)
RETURNS TABLE (
    exercise_id INT,
    exercise_code VARCHAR,
    exercise_name VARCHAR,
    muscle_group VARCHAR,
    pattern VARCHAR,
    complexity VARCHAR,
    caution_warnings TEXT[]
) AS $$
DECLARE
    v_level_code VARCHAR;
    v_level_val INT;
    v_goal_id INT;
BEGIN
    -- 1. Obtener datos del perfil del usuario (objetivo y nivel)
    SELECT up.goal_id, l.code INTO v_goal_id, v_level_code
    FROM user_profiles up
    LEFT JOIN levels l ON up.level_id = l.id
    WHERE up.id = p_user_id;

    -- Si no hay nivel asignado, por defecto es NIV1
    IF v_level_code IS NULL THEN
        v_level_code := 'NIV1';
    END IF;

    -- Mapeo de niveles a valores numéricos para comparación
    v_level_val := CASE v_level_code
        WHEN 'NIV1' THEN 1
        WHEN 'Básico' THEN 1
        WHEN 'NIV2' THEN 2
        WHEN 'Intermedio' THEN 2
        WHEN 'NIV3' THEN 3
        WHEN 'Avanzado' THEN 3
        WHEN 'NIV4' THEN 4
        WHEN 'Alto Rendimiento' THEN 4
        ELSE 1
    END;

    RETURN QUERY
    WITH 
    -- Unificar las condiciones médicas/patologías/lesiones del usuario
    user_conditions AS (
        SELECT pathology_id AS condition_id FROM user_pathology WHERE user_id = p_user_id
        UNION
        SELECT disease_id AS condition_id FROM user_disease WHERE user_id = p_user_id
    ),
    -- Obtener equipamiento del usuario
    user_equips AS (
        SELECT equipment_id FROM user_equipment WHERE user_id = p_user_id
    ),
    -- Ejercicios filtrados por nivel y objetivo
    filtered_exercises AS (
        SELECT e.id, e.code, e.name, e.muscle_group, e.pattern::VARCHAR as pattern, e.complexity
        FROM excersices e
        LEFT JOIN excersice_goal eg ON e.id = eg.excersice_id
        WHERE (v_goal_id IS NULL OR eg.goal_id = v_goal_id)
          AND (
            CASE e.level
                WHEN 'NIV1' THEN 1
                WHEN 'Básico' THEN 1
                WHEN 'NIV2' THEN 2
                WHEN 'Intermedio' THEN 2
                WHEN 'NIV3' THEN 3
                WHEN 'Avanzado' THEN 3
                WHEN 'NIV4' THEN 4
                WHEN 'Alto Rendimiento' THEN 4
                ELSE 1
            END <= v_level_val
          )
    ),
    -- Excluir ejercicios que sean prohibidos (FORBIDDEN) para el usuario
    health_filtered AS (
        SELECT fe.id, fe.code, fe.name, fe.muscle_group, fe.pattern, fe.complexity
        FROM filtered_exercises fe
        WHERE NOT EXISTS (
            SELECT 1 
            FROM excersice_condition ec
            JOIN user_conditions uc ON ec.condition_id = uc.condition_id
            WHERE ec.excersice_id = fe.id 
              AND ec.relationship = 'FORBIDDEN'
        )
    ),
    -- Filtrar por equipamiento primario (excluye si no tiene el equipamiento requerido)
    equip_filtered AS (
        SELECT hf.id, hf.code, hf.name, hf.muscle_group, hf.pattern, hf.complexity
        FROM health_filtered hf
        WHERE NOT EXISTS (
            SELECT 1
            FROM excersice_equipment ee
            JOIN equipment eq ON ee.equipment_id = eq.id
            WHERE ee.excersice_id = hf.id
              AND ee.is_primary = TRUE
              -- Si el ejercicio requiere equipo que el usuario no posee (excluyendo peso corporal)
              AND eq.name NOT IN ('Propio Peso', 'Ninguna')
              AND ee.equipment_id NOT IN (SELECT equipment_id FROM user_equips)
        )
    ),
    -- Agrupar advertencias (CAUTION) aplicables para los ejercicios viables
    exercise_cautions AS (
        SELECT ec.excersice_id, array_agg(c.name::TEXT) as warnings
        FROM excersice_condition ec
        JOIN conditions c ON ec.condition_id = c.id
        JOIN user_conditions uc ON ec.condition_id = uc.condition_id
        WHERE ec.relationship = 'CAUTION'
        GROUP BY ec.excersice_id
    )
    -- Seleccionar resultado final
    SELECT 
        ef.id as exercise_id,
        ef.code as exercise_code,
        ef.name as exercise_name,
        ef.muscle_group,
        ef.pattern,
        ef.complexity,
        COALESCE(ec.warnings, ARRAY[]::TEXT[]) as caution_warnings
    FROM equip_filtered ef
    LEFT JOIN exercise_cautions ec ON ef.id = ec.excersice_id;
END;
$$ LANGUAGE plpgsql;
