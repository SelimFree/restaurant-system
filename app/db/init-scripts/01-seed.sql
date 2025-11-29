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

-- RESTAURANT
INSERT INTO restaurants (name, address)
VALUES ('The PatternForge Grill', '123 Docker Way, Budapest')
RETURNING id;

-- USERS (password = "password")
-- bcrypt hash for password: 
-- $2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C
INSERT INTO users (name, email, phone, role, hashed_password)
VALUES
('Admin User', 'admin@example.com',  '111-111', 'admin',  '$2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C'),
('John Waiter', 'waiter@example.com','222-222', 'waiter', '$2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C'),
('Bob Cook',    'cook@example.com',  '333-333', 'cook',   '$2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C'),
('Manager Mia', 'manager@example.com','444-444','manager','$2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C'),
('Test Customer','customer@example.com','555-555','customer','$2b$12$pLnl5GAeA.PIX/kpPSjN7evOc5m8iRW6dRc9r0oOBAFBcEMSleh9C');

-- STAFF (link employees to restaurant)
INSERT INTO staff (user_id, restaurant_id)
SELECT id, 1 FROM users WHERE role IN ('admin','manager','waiter','cook');


-- TABLES
INSERT INTO tables (restaurant_id, name_number, capacity)
VALUES
(1, 'T1', 4),
(1, 'T2', 2),
(1, 'T3', 6),
(1, 'T4', 4);


-- MENUS
INSERT INTO menus (restaurant_id, name)
VALUES
(1, 'Main Menu'),
(1, 'Drinks');


-- MENU ITEMS
INSERT INTO menu_items (menu_id, name, description, price, available, prep_time)
VALUES
-- Main Menu Items
((SELECT id FROM menus WHERE name='Main Menu'),
 'Cheeseburger', 'Beef burger with cheese and fries', 12.50, TRUE, 10),
((SELECT id FROM menus WHERE name='Main Menu'),
 'Chicken Pasta', 'Creamy pasta with grilled chicken', 11.00, TRUE, 12),
((SELECT id FROM menus WHERE name='Main Menu'),
 'Garden Salad', 'Fresh salad with vinaigrette', 7.50, TRUE, 5),

-- Drinks
((SELECT id FROM menus WHERE name='Drinks'),
 'Cola', 'Cold soft drink', 2.90, TRUE, 0),
((SELECT id FROM menus WHERE name='Drinks'),
 'Espresso', 'Strong Italian coffee', 2.50, TRUE, 2),
((SELECT id FROM menus WHERE name='Drinks'),
 'Lemonade', 'Fresh homemade lemonade', 3.80, TRUE, 1);


-- ITEM MODIFIERS
INSERT INTO item_modifiers (item_id, name, price_delta)
VALUES
((SELECT id FROM menu_items WHERE name='Cheeseburger'), 'Extra Cheese', 1.00),
((SELECT id FROM menu_items WHERE name='Cheeseburger'), 'Double Patty', 3.00),
((SELECT id FROM menu_items WHERE name='Chicken Pasta'), 'Gluten-Free Pasta', 1.50);


-- SAMPLE ORDER (for testing waiter/kitchen UIs)
INSERT INTO orders (table_id, waiter_id, status)
VALUES (
    (SELECT id FROM tables WHERE name_number='T1'),
    (SELECT id FROM users WHERE role='waiter'),
    'created'
)
RETURNING id;

INSERT INTO order_items (order_id, item_id, quantity, status, notes)
VALUES
(currval('orders_id_seq'), (SELECT id FROM menu_items WHERE name='Cheeseburger'), 2, 'pending', 'No onions'),
(currval('orders_id_seq'), (SELECT id FROM menu_items WHERE name='Espresso'), 1, 'pending', NULL);

-- Log that this script also ran
INSERT INTO _init_log (script_name) VALUES ('01-seed.sql') ON CONFLICT DO NOTHING;