def get_create_tables_sql():
    return """CREATE TABLE IF NOT EXISTS `product`
(
    `id`                    int not null AUTO_INCREMENT PRIMARY KEY,
    `product_name`          varchar(255),
    `product_genre_id`      int,
    `price`                 double,
    `created_at`            timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            timestamp DEFAULT CURRENT_TIMESTAMP,
    `created_by`            varchar(100)
);

CREATE TABLE IF NOT EXISTS `product_genre`
(
    `id`                    int not null AUTO_INCREMENT PRIMARY KEY,
    `name`                  varchar(100),
    `created_at`            timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            timestamp DEFAULT CURRENT_TIMESTAMP,
    `created_by`            varchar(100)
);
"""


def get_insert_data_sql():
    return """INSERT INTO `product_genre` (`name`, `created_by`)
VALUES
    ('Books', 'admin'),
    ('Electronics', 'admin'),
    ('Furniture', 'admin'),
    ('Clothing', 'admin'),
    ('Toys', 'admin');

INSERT INTO `product` (`product_name`, `product_genre_id`, `price`, `created_by`)
VALUES
    ('Fiction Book', 1, 15.99, 'admin'),
    ('Wireless Earbuds', 2, 59.99, 'admin'),
    ('Office Chair', 3, 129.99, 'admin'),
    ('Denim Jacket', 4, 49.99, 'admin'),
    ('Building Blocks', 5, 19.99, 'admin');
"""
