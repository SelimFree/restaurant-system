-- This script runs FIRST and defines the database schema.
-- Yahya: Please define the schema here based on the ER diagram and data model. We can discuss the changes if there are any

/*
-- --- TODO: Define custom types ---
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'waiter', 'cook');
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'cooking', 'ready', 'served', 'cancelled');
CREATE TYPE order_item_status AS ENUM ('pending', 'cooking', 'ready', 'served');

-- --- TODO: Create tables ---
CREATE TABLE IF NOT EXISTS users ( ... );
CREATE TABLE IF NOT EXISTS restaurants ( ... );
CREATE TABLE IF NOT EXISTS staff ( ... );
CREATE TABLE IF NOT EXISTS tables ( ... );
CREATE TABLE IF NOT EXISTS menus ( ... );
CREATE TABLE IF NOT EXISTS menu_items ( ... );
CREATE TABLE IF NOT EXISTS item_modifiers ( ... );
CREATE TABLE IF NOT EXISTS orders ( ... );
CREATE TABLE IF NOT EXISTS order_items ( ... );
CREATE TABLE IF NOT EXISTS notifications ( ... );

-- --- TODO: Add Indexes for performance ---
CREATE INDEX ...
*/

-- This table confirms that the init scripts are being executed.
CREATE TABLE IF NOT EXISTS _init_log (
    script_name VARCHAR(255) PRIMARY KEY,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO _init_log (script_name) VALUES ('00-init.sql') ON CONFLICT DO NOTHING;