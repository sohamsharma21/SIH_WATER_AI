-- SIH WATER AI Database Schema
-- Run this migration to create all required tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sensors table: Stores real-time sensor readings
CREATE TABLE IF NOT EXISTS sensors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    parameter_name VARCHAR(100) NOT NULL,
    value DECIMAL(15, 4) NOT NULL,
    unit VARCHAR(20),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    location VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Predictions table: Stores ML model predictions
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    input_data JSONB NOT NULL,
    predictions JSONB NOT NULL,
    quality_score DECIMAL(5, 2),
    contamination_index DECIMAL(5, 2),
    confidence DECIMAL(5, 4),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Models table: Stores ML model metadata
CREATE TABLE IF NOT EXISTS models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_name VARCHAR(100) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    model_path TEXT NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    training_date TIMESTAMPTZ NOT NULL,
    accuracy DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    r2_score DECIMAL(5, 4),
    training_params JSONB,
    feature_columns TEXT[],
    target_column VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(dataset_name, model_version)
);

-- Reports table: Stores PDF report metadata
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    storage_path TEXT NOT NULL,
    public_url TEXT,
    file_size BIGINT,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    generated_by UUID REFERENCES auth.users(id),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Treatment recommendations table: Stores optimization outputs
CREATE TABLE IF NOT EXISTS treatment_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prediction_id UUID REFERENCES predictions(id),
    treatment_stage VARCHAR(50) NOT NULL,
    recommendations JSONB NOT NULL,
    dosing_ml DECIMAL(10, 2),
    expected_recovery DECIMAL(5, 2),
    reuse_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sensors_timestamp ON sensors(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sensors_sensor_id ON sensors(sensor_id);
CREATE INDEX IF NOT EXISTS idx_sensors_sensor_type ON sensors(sensor_type);
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_model_name ON predictions(model_name);
CREATE INDEX IF NOT EXISTS idx_models_dataset_name ON models(dataset_name);
CREATE INDEX IF NOT EXISTS idx_models_is_active ON models(is_active);
CREATE INDEX IF NOT EXISTS idx_reports_generated_at ON reports(generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_treatment_recommendations_prediction_id ON treatment_recommendations(prediction_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

