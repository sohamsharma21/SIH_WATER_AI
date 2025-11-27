-- Additional migration for models table enhancements
-- This ensures the models table has all required fields

-- Add updated_at column if it doesn't exist
ALTER TABLE models ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Add model metrics column for additional performance metrics
ALTER TABLE models ADD COLUMN IF NOT EXISTS model_metrics JSONB;

-- Create a view for active models only
CREATE OR REPLACE VIEW active_models AS
SELECT 
    id,
    dataset_name,
    model_name,
    model_version,
    model_type,
    training_date,
    accuracy,
    f1_score,
    r2_score,
    is_active,
    created_at
FROM models
WHERE is_active = true
ORDER BY training_date DESC;

-- Create a function to deactivate old models when a new version is uploaded
CREATE OR REPLACE FUNCTION deactivate_old_models()
RETURNS TRIGGER AS $$
BEGIN
    -- Deactivate other versions of the same dataset model
    UPDATE models
    SET is_active = false
    WHERE dataset_name = NEW.dataset_name
    AND model_name = NEW.model_name
    AND id != NEW.id
    AND is_active = true;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically deactivate old models
DROP TRIGGER IF EXISTS trigger_deactivate_old_models ON models;
CREATE TRIGGER trigger_deactivate_old_models
    AFTER INSERT ON models
    FOR EACH ROW
    WHEN (NEW.is_active = true)
    EXECUTE FUNCTION deactivate_old_models();

