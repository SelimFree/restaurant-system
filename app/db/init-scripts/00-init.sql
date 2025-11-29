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

--  ENUM TYPES
CREATE TYPE user_role AS ENUM ('admin','manager','waiter','cook','customer');
CREATE TYPE table_status AS ENUM ('free','occupied','reserved');
CREATE TYPE order_status AS ENUM ('created','sent','cooking','ready','served','cancelled');
CREATE TYPE order_item_status AS ENUM ('pending','cooking','ready');

--  USERS
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    role user_role NOT NULL,
    hashed_password TEXT NOT NULL,
    meta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

--  RESTAURANTS
CREATE TABLE IF NOT EXISTS restaurants (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

--  STAFF
CREATE TABLE IF NOT EXISTS staff (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    restaurant_id BIGINT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    role_meta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, restaurant_id)
);

--  TABLES
CREATE TABLE IF NOT EXISTS tables (
    id BIGSERIAL PRIMARY KEY,
    restaurant_id BIGINT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name_number TEXT NOT NULL,
    capacity INT NOT NULL CHECK (capacity >= 1),
    status table_status NOT NULL DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(restaurant_id, name_number)
);

--  MENUS
CREATE TABLE IF NOT EXISTS menus (
    id BIGSERIAL PRIMARY KEY,
    restaurant_id BIGINT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(restaurant_id, name)
);

--  MENU ITEMS
CREATE TABLE IF NOT EXISTS menu_items (
    id BIGSERIAL PRIMARY KEY,
    menu_id BIGINT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    available BOOLEAN NOT NULL DEFAULT TRUE,
    prep_time INT NOT NULL DEFAULT 0 CHECK (prep_time >= 0),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(menu_id, name)
);

--  ITEM MODIFIERS
CREATE TABLE IF NOT EXISTS item_modifiers (
    id BIGSERIAL PRIMARY KEY,
    item_id BIGINT NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    price_delta NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(item_id, name)
);

--  ORDERS
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    table_id BIGINT NOT NULL REFERENCES tables(id) ON DELETE RESTRICT,
    waiter_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status order_status NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    total NUMERIC(12,2) NOT NULL DEFAULT 0
);

--  ORDER ITEMS
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_id BIGINT NOT NULL REFERENCES menu_items(id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity >= 1),
    status order_item_status NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

--  NOTIFICATIONS
CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    payload JSONB NOT NULL,
    read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);

--  INDEXES
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_table ON orders(table_id);
CREATE INDEX IF NOT EXISTS idx_orders_waiter ON orders(waiter_id);

CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_menu_items_menu ON menu_items(menu_id);

CREATE INDEX IF NOT EXISTS idx_tables_restaurant ON tables(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_staff_restaurant ON staff(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_menus_restaurant ON menus(restaurant_id);

-- DO NOT REMOVE - DB INIT LOGGING
CREATE TABLE IF NOT EXISTS _init_log (
    script_name VARCHAR(255) PRIMARY KEY,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO _init_log (script_name) VALUES ('00-init.sql') ON CONFLICT DO NOTHING;