-- V1__Create_tables.sql
-- Create notifications table
CREATE TABLE notifications (
    id VARCHAR(36) PRIMARY KEY,
    recipient_id VARCHAR(100) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    subject VARCHAR(255),
    message TEXT,
    recipient_address VARCHAR(255) NOT NULL,
    template_id VARCHAR(36),
    status VARCHAR(50) NOT NULL,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    priority VARCHAR(20) DEFAULT 'NORMAL',
    error_message TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    metadata TEXT
);

-- Create notification_templates table
CREATE TABLE notification_templates (
    id VARCHAR(36) PRIMARY KEY,
    template_name VARCHAR(255) NOT NULL UNIQUE,
    channel VARCHAR(50) NOT NULL,
    subject VARCHAR(255),
    body TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Create user_preferences table
CREATE TABLE user_preferences (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL UNIQUE,
    email_enabled BOOLEAN DEFAULT true,
    sms_enabled BOOLEAN DEFAULT true,
    push_enabled BOOLEAN DEFAULT true,
    email_address VARCHAR(255),
    phone_number VARCHAR(20),
    push_device_token VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_recipient_id ON notifications(recipient_id);
CREATE INDEX idx_status ON notifications(status);
CREATE INDEX idx_channel ON notifications(channel);
CREATE INDEX idx_created_at ON notifications(created_at);
CREATE INDEX idx_user_id ON user_preferences(user_id);
