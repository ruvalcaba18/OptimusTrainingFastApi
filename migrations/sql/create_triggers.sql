-- 1. Trigger para actualizar el campo updated_at automáticamente
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_users_timestamp ON users;
CREATE TRIGGER trg_update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION fn_update_timestamp();

DROP TRIGGER IF EXISTS trg_update_user_profiles_timestamp ON user_profiles;
CREATE TRIGGER trg_update_user_profiles_timestamp
BEFORE UPDATE ON user_profiles
FOR EACH ROW
EXECUTE FUNCTION fn_update_timestamp();

-- 2. Trigger para rotación de rutinas (máximo 12 y borrado cada 3 meses)
CREATE OR REPLACE FUNCTION fn_rotate_user_training_plans()
RETURNS TRIGGER AS $$
DECLARE
    v_plan_count INT;
    v_oldest_date TIMESTAMP;
BEGIN
    SELECT COUNT(*) INTO v_plan_count 
    FROM training_plans 
    WHERE athlete_id = NEW.athlete_id;

    IF v_plan_count >= 12 THEN
        -- TODO: Enviar al Cold Storage para trazabilidad antes de eliminar
        DELETE FROM training_plans
        WHERE id IN (
            SELECT id FROM training_plans
            WHERE athlete_id = NEW.athlete_id
            ORDER BY created_at ASC
            LIMIT 1
        );
    END IF;

    SELECT MIN(created_at) INTO v_oldest_date
    FROM training_plans
    WHERE athlete_id = NEW.athlete_id;

    IF v_oldest_date IS NOT NULL AND v_oldest_date < NOW() - INTERVAL '3 months' THEN
        -- TODO: Enviar al Cold Storage para trazabilidad antes de eliminar
        DELETE FROM training_plans
        WHERE id IN (
            SELECT id FROM training_plans
            WHERE athlete_id = NEW.athlete_id
            ORDER BY created_at ASC
            LIMIT 2
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_rotate_training_plans ON training_plans;
CREATE TRIGGER trg_rotate_training_plans
BEFORE INSERT ON training_plans
FOR EACH ROW
EXECUTE FUNCTION fn_rotate_user_training_plans();
