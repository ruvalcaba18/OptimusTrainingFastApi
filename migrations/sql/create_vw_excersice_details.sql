CREATE OR REPLACE VIEW vw_excersice_details AS
SELECT 
    e.id AS exercise_id,
    e.code AS exercise_code,
    e.name AS exercise_name,
    e.muscle_group,
    e.pattern::VARCHAR AS pattern,
    e.complexity,
    e.level,
    e.category,
    g.id AS goal_id,
    g.code AS goal_code,
    g.name AS goal_name,
    -- Equipamiento Primario
    MAX(CASE WHEN ee.is_primary = TRUE THEN eq.name ELSE NULL END) AS primary_equipment,
    -- Equipamiento Secundario
    MAX(CASE WHEN ee.is_primary = FALSE THEN eq.name ELSE NULL END) AS secondary_equipment
FROM excersices e
LEFT JOIN excersice_goal eg ON e.id = eg.excersice_id
LEFT JOIN goals g ON eg.goal_id = g.id
LEFT JOIN excersice_equipment ee ON e.id = ee.excersice_id
LEFT JOIN equipment eq ON ee.equipment_id = eq.id
GROUP BY e.id, g.id, g.code, g.name;
