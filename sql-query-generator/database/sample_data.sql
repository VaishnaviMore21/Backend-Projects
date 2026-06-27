-- Sample Data for sql-query-generator

-- Insert Categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Home & Garden', 'Home and garden products'),
('Books', 'Physical and educational books'),
('Clothing', 'Apparel and fashion items'),
('Sports', 'Sports equipment and gear');

-- Insert Users
INSERT INTO users (email, first_name, last_name, phone, status, created_at, last_login) VALUES
('john.doe@example.com', 'John', 'Doe', '555-0101', 'active', '2023-01-15', '2024-01-10 14:30:00'),
('jane.smith@example.com', 'Jane', 'Smith', '555-0102', 'active', '2023-02-20', '2024-01-12 09:15:00'),
('bob.johnson@example.com', 'Bob', 'Johnson', '555-0103', 'active', '2023-03-10', '2024-01-05 11:45:00'),
('alice.wilson@example.com', 'Alice', 'Wilson', '555-0104', 'inactive', '2022-11-30', '2023-08-22 16:20:00'),
('charlie.brown@example.com', 'Charlie', 'Brown', '555-0105', 'active', '2023-06-05', '2024-01-11 13:00:00'),
('diana.prince@example.com', 'Diana', 'Prince', '555-0106', 'active', '2023-07-12', '2024-01-09 10:30:00'),
('evan.hunt@example.com', 'Evan', 'Hunt', '555-0107', 'active', '2023-08-01', '2024-01-08 15:45:00'),
('fiona.green@example.com', 'Fiona', 'Green', '555-0108', 'active', '2023-09-18', '2024-01-12 12:00:00');

-- Insert Products
INSERT INTO products (sku, name, description, category, price, cost, stock_quantity, reorder_level, status) VALUES
('ELEC-001', 'Wireless Headphones', 'Premium noise-cancelling headphones', 'Electronics', 149.99, 60.00, 45, 10, 'active'),
('ELEC-002', 'USB-C Cable', '2-meter durable USB-C charging cable', 'Electronics', 12.99, 3.50, 150, 50, 'active'),
('ELEC-003', 'Portable Power Bank', '20000mAh power bank with fast charging', 'Electronics', 34.99, 15.00, 25, 10, 'active'),
('HOME-001', 'Stainless Steel Cookware Set', '10-piece professional cookware', 'Home & Garden', 199.99, 80.00, 12, 5, 'active'),
('HOME-002', 'Ceramic Plant Pot', '10-inch decorative ceramic pot', 'Home & Garden', 24.99, 8.00, 80, 20, 'active'),
('BOOK-001', 'Data Science Fundamentals', 'Comprehensive guide to data science', 'Books', 45.00, 15.00, 30, 5, 'active'),
('BOOK-002', 'Cloud Computing Mastery', 'AWS and Azure best practices', 'Books', 55.00, 18.00, 20, 5, 'active'),
('CLTH-001', 'Cotton T-Shirt', 'Premium organic cotton t-shirt', 'Clothing', 19.99, 5.00, 120, 30, 'active'),
('CLTH-002', 'Denim Jeans', 'Classic fit blue denim jeans', 'Clothing', 59.99, 20.00, 60, 15, 'active'),
('SPRT-001', 'Yoga Mat', 'Non-slip 6mm thick yoga mat', 'Sports', 29.99, 8.00, 40, 10, 'active'),
('SPRT-002', 'Dumbbells Set', 'Adjustable 5-25 lb dumbbell set', 'Sports', 89.99, 35.00, 15, 5, 'active'),
('ELEC-004', 'Smartphone Stand', 'Universal phone holder for desk', 'Electronics', 9.99, 2.00, 200, 50, 'active'),
('HOME-003', 'LED Desk Lamp', 'Adjustable brightness LED lamp', 'Home & Garden', 34.99, 12.00, 35, 10, 'active'),
('BOOK-003', 'Machine Learning Guide', 'ML algorithms and implementations', 'Books', 65.00, 20.00, 15, 5, 'inactive');

-- Insert Orders
INSERT INTO orders (user_id, order_number, status, total_amount, tax_amount, shipping_cost, discount_amount, created_at, shipped_at, delivered_at) VALUES
(1, 'ORD-2024-001', 'delivered', 199.99, 16.00, 10.00, 0, '2024-01-01 10:00:00', '2024-01-02 09:00:00', '2024-01-05 14:30:00'),
(2, 'ORD-2024-002', 'shipped', 339.97, 27.20, 10.00, 10.00, '2024-01-03 14:15:00', '2024-01-04 08:00:00', NULL),
(1, 'ORD-2024-003', 'delivered', 89.99, 7.20, 10.00, 0, '2024-01-05 11:30:00', '2024-01-06 09:00:00', '2024-01-08 16:45:00'),
(3, 'ORD-2024-004', 'pending', 299.97, 24.00, 10.00, 20.00, '2024-01-10 09:45:00', NULL, NULL),
(5, 'ORD-2024-005', 'delivered', 179.98, 14.40, 10.00, 0, '2024-01-07 16:20:00', '2024-01-08 08:00:00', '2024-01-11 12:00:00'),
(6, 'ORD-2024-006', 'processing', 409.95, 32.80, 10.00, 15.00, '2024-01-08 13:10:00', NULL, NULL),
(7, 'ORD-2024-007', 'delivered', 249.96, 20.00, 10.00, 0, '2024-01-06 10:00:00', '2024-01-07 08:00:00', '2024-01-09 14:15:00'),
(8, 'ORD-2024-008', 'shipped', 139.99, 11.20, 10.00, 5.00, '2024-01-09 15:30:00', '2024-01-10 09:00:00', NULL),
(2, 'ORD-2024-009', 'delivered', 499.99, 40.00, 10.00, 25.00, '2024-01-02 12:00:00', '2024-01-03 08:00:00', '2024-01-06 11:30:00'),
(1, 'ORD-2024-010', 'pending', 359.96, 28.80, 10.00, 0, '2024-01-11 10:15:00', NULL, NULL);

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_percent, line_total) VALUES
(1, 1, 1, 149.99, 0, 149.99),
(1, 4, 1, 199.99, 0, 49.99),  -- 25% discount
(2, 3, 2, 34.99, 0, 69.98),
(2, 7, 1, 55.00, 20, 44.00),
(3, 10, 3, 29.99, 0, 89.99),
(4, 6, 2, 45.00, 0, 90.00),
(4, 11, 1, 89.99, 0, 89.99),
(4, 2, 6, 12.99, 5, 74.07),
(5, 8, 3, 19.99, 0, 59.97),
(5, 9, 1, 59.99, 0, 59.99),
(5, 13, 1, 34.99, 10, 31.49),
(6, 5, 2, 24.99, 0, 49.98),
(6, 12, 2, 9.99, 0, 19.98),
(6, 1, 2, 149.99, 15, 255.00),
(7, 2, 10, 12.99, 10, 116.91),
(7, 10, 1, 29.99, 0, 29.99),
(8, 3, 1, 34.99, 0, 34.99),
(8, 13, 2, 34.99, 0, 69.98),
(9, 1, 3, 149.99, 5, 427.47),
(9, 6, 1, 45.00, 0, 45.00),
(10, 4, 2, 199.99, 0, 399.98),
(10, 9, 1, 59.99, 0, 59.99);

-- Insert Payments
INSERT INTO payments (order_id, payment_method, amount, status, transaction_id, created_at, processed_at) VALUES
(1, 'credit_card', 199.99, 'completed', 'TXN-001', '2024-01-01 10:05:00', '2024-01-01 10:10:00'),
(2, 'credit_card', 339.97, 'completed', 'TXN-002', '2024-01-03 14:20:00', '2024-01-03 14:25:00'),
(3, 'debit_card', 89.99, 'completed', 'TXN-003', '2024-01-05 11:35:00', '2024-01-05 11:40:00'),
(4, 'paypal', 299.97, 'pending', 'TXN-004', '2024-01-10 09:50:00', NULL),
(5, 'credit_card', 179.98, 'completed', 'TXN-005', '2024-01-07 16:25:00', '2024-01-07 16:30:00'),
(6, 'credit_card', 409.95, 'pending', 'TXN-006', '2024-01-08 13:15:00', NULL),
(7, 'debit_card', 249.96, 'completed', 'TXN-007', '2024-01-06 10:05:00', '2024-01-06 10:10:00'),
(8, 'credit_card', 139.99, 'completed', 'TXN-008', '2024-01-09 15:35:00', '2024-01-09 15:40:00'),
(9, 'credit_card', 499.99, 'completed', 'TXN-009', '2024-01-02 12:05:00', '2024-01-02 12:10:00'),
(10, 'paypal', 359.96, 'pending', 'TXN-010', '2024-01-11 10:20:00', NULL);

-- Insert Inventory Transactions
INSERT INTO inventory_transactions (product_id, transaction_type, quantity_change, reason, created_at, user_id) VALUES
(1, 'sale', -1, 'Order ORD-2024-001', '2024-01-01 10:00:00', NULL),
(1, 'sale', -3, 'Order ORD-2024-009', '2024-01-02 12:00:00', NULL),
(1, 'restock', 50, 'Supplier shipment', '2024-01-12 08:00:00', NULL),
(2, 'sale', -6, 'Order ORD-2024-007', '2024-01-06 10:00:00', NULL),
(3, 'sale', -2, 'Order ORD-2024-002', '2024-01-03 14:15:00', NULL),
(3, 'sale', -1, 'Order ORD-2024-008', '2024-01-09 15:30:00', NULL),
(4, 'sale', -1, 'Order ORD-2024-001', '2024-01-01 10:00:00', NULL),
(10, 'sale', -3, 'Order ORD-2024-003', '2024-01-05 11:30:00', NULL),
(11, 'sale', -1, 'Order ORD-2024-004', '2024-01-10 09:45:00', NULL);

-- Insert Reviews
INSERT INTO reviews (product_id, user_id, order_id, rating, title, comment, helpful_count) VALUES
(1, 1, 1, 5, 'Excellent sound quality', 'These headphones are amazing! Great noise cancellation and battery life.', 25),
(10, 1, 3, 4, 'Good yoga mat', 'Very comfortable for daily practice. Bit slippery on tiles though.', 12),
(3, 2, 2, 5, 'Perfect power bank', 'Fast charging and portable. Exactly what I needed.', 18),
(7, 2, 2, 4, 'Informative read', 'Good overview of cloud platforms. Some chapters could be more detailed.', 8),
(8, 5, 5, 5, 'Great value', 'Quality t-shirt at an affordable price. Fits perfectly.', 15),
(9, 8, 8, 4, 'Good jeans', 'Comfortable fit, though they needed washing before wear.', 10),
(1, 3, 9, 5, 'Worth every penny', 'Upgraded to these after losing my old pair. Even better!', 31);

-- Update product stock_quantity to reflect sales
UPDATE products SET stock_quantity = stock_quantity - (SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE product_id = products.id);
