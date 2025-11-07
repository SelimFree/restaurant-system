-- This script runs SECOND to populate the database with seed/test data.
-- Yahya: Please add test data here.

/*
-- --- TODO: Add Test Data ---

-- 1. Add a default restaurant
INSERT INTO restaurants (name, address) VALUES ('The PatternForge Grill', '123 Docker Way');

-- 2. Add test users (password is 'password')
-- $2b$12$EixZaYISc1j.A.5.kVAW5uY.a8.wT.i33rJ.0uRkl.wcn4Dq.G.rm
INSERT INTO users (name, email, role, hashed_password) VALUES 
('Admin User', 'admin@example.com', 'admin', '...hashed_password...'),
('Waiter User', 'waiter@example.com', 'waiter', '...hashed_password...'),
('Cook User', 'cook@example.com', 'cook', '...hashed_password...');

-- 3. Add tables
INSERT INTO tables (restaurant_id, name_number, capacity) VALUES
(1, 'T1', 4),
(1, 'T2', 2),
(1, 'T3', 6);

-- 4. Add menus and items
INSERT INTO menus (restaurant_id, name) VALUES (1, 'Main Menu');
INSERT INTO menu_items (menu_id, name, price) VALUES
(1, 'Cheeseburger', 12.50),
(1, 'Fries', 4.00);
*/

-- Log that this script also ran
INSERT INTO _init_log (script_name) VALUES ('01-seed.sql') ON CONFLICT DO NOTHING;