-- 1. Habilitar extensión trigram e índice GIN
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX IF NOT EXISTS idx_excersices_name_trgm ON excersices USING gin (name gin_trgm_ops);

-- 2. Índices de rendimiento B-Tree adicionales
CREATE INDEX IF NOT EXISTS idx_user_profiles_goal_level ON user_profiles(goal_id, level_id);
CREATE INDEX IF NOT EXISTS idx_user_pathology_user_cond ON user_pathology(user_id, pathology_id);
CREATE INDEX IF NOT EXISTS idx_user_disease_user_cond ON user_disease(user_id, disease_id);
CREATE INDEX IF NOT EXISTS idx_user_equipment_user_eq ON user_equipment(user_id, equipment_id);
CREATE INDEX IF NOT EXISTS idx_excersice_goal_ex_goal ON excersice_goal(excersice_id, goal_id);
CREATE INDEX IF NOT EXISTS idx_excersice_condition_ex_cond ON excersice_condition(excersice_id, condition_id);
CREATE INDEX IF NOT EXISTS idx_excersice_equipment_ex_eq ON excersice_equipment(excersice_id, equipment_id);
CREATE INDEX IF NOT EXISTS idx_programming_matrix_goal_level ON programming_matrix(goal_code, level_code);
