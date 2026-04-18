-- ============================================
-- PhilHealthy Database Setup for MySQL/XAMPP
-- ============================================
-- Run this in phpMyAdmin or MySQL CLI:
--   mysql -u root -p < database_setup.sql
-- ============================================

CREATE DATABASE IF NOT EXISTS philhealthy;
USE philhealthy;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    expiry_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inventory log
CREATE TABLE IF NOT EXISTS inventory_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    action ENUM('restock', 'sold', 'expired', 'adjustment') NOT NULL,
    quantity INT NOT NULL,
    notes TEXT,
    performed_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Deliveries table
CREATE TABLE IF NOT EXISTS deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier VARCHAR(200) NOT NULL,
    items TEXT NOT NULL,
    status ENUM('Pending', 'Approved', 'In Transit', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    approved BOOLEAN DEFAULT FALSE,
    approved_by INT,
    delivery_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Sales / Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_code VARCHAR(20) UNIQUE NOT NULL,
    customer_name VARCHAR(100),
    total DECIMAL(10,2) NOT NULL,
    status ENUM('Completed', 'Pending', 'Cancelled') DEFAULT 'Pending',
    processed_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (processed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Transaction items (line items)
CREATE TABLE IF NOT EXISTS transaction_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    report_type ENUM('daily', 'weekly', 'monthly', 'custom') DEFAULT 'daily',
    content TEXT,
    generated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Sample data
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@philhealthy.com', 'admin123', 'admin'),
('Staff User', 'staff@philhealthy.com', 'staff123', 'staff');

INSERT INTO products (name, category, price, stock, expiry_date) VALUES
('Paracetamol 500mg', 'Pain Relief', 5.50, 250, '2026-08-15'),
('Amoxicillin 500mg', 'Antibiotics', 12.00, 180, '2025-12-01'),
('Cetirizine 10mg', 'Allergy', 8.00, 300, '2026-05-20'),
('Losartan 50mg', 'Cardiovascular', 15.00, 5, '2025-06-30'),
('Metformin 500mg', 'Diabetes', 10.00, 0, '2026-01-10'),
('Omeprazole 20mg', 'Gastro', 9.50, 120, '2025-07-15'),
('Vitamin C 500mg', 'Vitamins', 6.00, 400, '2027-03-01'),
('Ibuprofen 200mg', 'Pain Relief', 7.00, 15, '2025-09-20');

SELECT 'PhilHealthy database setup complete!' AS status;
