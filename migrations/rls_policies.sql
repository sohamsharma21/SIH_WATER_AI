-- Row Level Security (RLS) Policies for SIH WATER AI
-- Enable RLS on all tables and define policies

-- Enable Row Level Security
ALTER TABLE sensors ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE models ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE treatment_recommendations ENABLE ROW LEVEL SECURITY;

-- Sensors table policies
-- Public read access for sensor data (adjust based on requirements)
CREATE POLICY "Public read access for sensors"
    ON sensors FOR SELECT
    USING (true);

-- Authenticated users can insert sensor data
CREATE POLICY "Authenticated users can insert sensors"
    ON sensors FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Admins can update/delete sensors
CREATE POLICY "Admins can modify sensors"
    ON sensors FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Predictions table policies
-- Authenticated users can read predictions
CREATE POLICY "Authenticated users can read predictions"
    ON predictions FOR SELECT
    TO authenticated
    USING (true);

-- Service role can insert predictions (for backend API)
CREATE POLICY "Service role can insert predictions"
    ON predictions FOR INSERT
    TO service_role
    WITH CHECK (true);

-- Authenticated users can create predictions
CREATE POLICY "Authenticated users can create predictions"
    ON predictions FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Models table policies
-- Public read access for active models
CREATE POLICY "Public read access for active models"
    ON models FOR SELECT
    USING (is_active = true);

-- Admins can manage all models
CREATE POLICY "Admins can manage models"
    ON models FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Service role can insert models (for backend training)
CREATE POLICY "Service role can manage models"
    ON models FOR ALL
    TO service_role
    USING (true);

-- Reports table policies
-- Users can read their own reports
CREATE POLICY "Users can read own reports"
    ON reports FOR SELECT
    TO authenticated
    USING (auth.uid() = generated_by);

-- Authenticated users can create reports
CREATE POLICY "Authenticated users can create reports"
    ON reports FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = generated_by);

-- Service role can manage all reports
CREATE POLICY "Service role can manage reports"
    ON reports FOR ALL
    TO service_role
    USING (true);

-- Treatment recommendations policies
-- Authenticated users can read recommendations
CREATE POLICY "Authenticated users can read recommendations"
    ON treatment_recommendations FOR SELECT
    TO authenticated
    USING (true);

-- Service role can create recommendations
CREATE POLICY "Service role can create recommendations"
    ON treatment_recommendations FOR INSERT
    TO service_role
    WITH CHECK (true);

-- Note: Adjust these policies based on your specific security requirements
-- The above policies provide a baseline security model

