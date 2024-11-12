CREATE DATABASE to_do_app;
USE to_do_app;
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    priority ENUM('Baja', 'Media', 'Alta') DEFAULT 'Media',
    completed BOOLEAN DEFAULT FALSE
);