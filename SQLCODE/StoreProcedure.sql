USE Hachiko;

DROP PROCEDURE IF EXISTS DeleteProduct;
DROP PROCEDURE IF EXISTS ChangeProductInformation;
DROP PROCEDURE IF EXISTS GetUser;
DROP PROCEDURE IF EXISTS CountUser;
DROP PROCEDURE IF EXISTS InsertUser;
DROP PROCEDURE IF EXISTS CountMembers;
DROP PROCEDURE IF EXISTS CountMembersVIP;
DROP PROCEDURE IF EXISTS GetUserId;
DROP PROCEDURE IF EXISTS GetAccount;
DROP PROCEDURE IF EXISTS InsertAccount;
DROP PROCEDURE IF EXISTS UpdateAccount;
DROP PROCEDURE IF EXISTS GetPoint;
DROP PROCEDURE IF EXISTS UpdateUser;
DROP PROCEDURE IF EXISTS GetProducts;
DROP PROCEDURE IF EXISTS GetProductItem;
DROP PROCEDURE IF EXISTS GetProductDetail;
DROP PROCEDURE IF EXISTS GetAllCategories;
DROP PROCEDURE IF EXISTS GetProductAdmin;
DROP PROCEDURE IF EXISTS GetBrand;
DROP PROCEDURE IF EXISTS GetBrandID;
DROP PROCEDURE IF EXISTS InsertProduct;
DROP PROCEDURE IF EXISTS InsertBills;
DROP PROCEDURE IF EXISTS GetBillsCount;
DROP PROCEDURE IF EXISTS GetBills;
DROP PROCEDURE IF EXISTS GetNotify;
DROP PROCEDURE IF EXISTS InsertNotifyUser;
DROP PROCEDURE IF EXISTS ExistsInNotifyUser;
DROP PROCEDURE IF EXISTS GetNotifyUser;
DROP PROCEDURE IF EXISTS InsertProductSizes;
DROP PROCEDURE IF EXISTS GetProductSizes;

DELIMITER //
CREATE PROCEDURE `DeleteProduct` (
  IN product_name VARCHAR(100)
)
BEGIN
  -- Check if the product exists
  IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductName = product_name) THEN
    SELECT 'The product does not exist';
  END IF;

  -- Delete the product from the table
  DELETE FROM Products WHERE ProductName = product_name;

  SELECT 'Product deleted successfully';
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE `ChangeProductInformation` (
  IN product_name VARCHAR(100),
  IN new_category INT,
  IN new_inventory INT,
  IN new_product_photo VARCHAR(200),
  IN new_product_detailed INT,
  IN new_description TEXT,
  IN new_price DOUBLE
)
BEGIN
  -- Check if the product exists
  IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductName = product_name) THEN
    SELECT 'The product does not exist';
  END IF;

  -- Update the product information
  UPDATE Products
  SET Category = new_category,
      Inventory = new_inventory,
      ProductPhoto = new_product_photo,
      ProductDetailed = new_product_detailed,
      Description = new_description,
      Price = new_price
  WHERE ProductName = product_name;

  SELECT 'Product information changed successfully';
END //

DELIMITER ;
SET SQL_SAFE_UPDATES = 0;

UPDATE users
SET point = point * 10

----------------------------login_controlle----------------------------

DELIMITER //
-- Tạo Stored Procedure để đếm số lượng users
CREATE PROCEDURE CountUser()
BEGIN
    SELECT COUNT(*) FROM users;
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để đếm số lượng members
CREATE PROCEDURE CountMembers()
BEGIN
    SELECT COUNT(*) FROM users WHERE money > 5000000;
END //

DELIMITER //
-- Tạo Stored Procedure để đếm số lượng memberVIP
CREATE PROCEDURE CountMembersVIP()
BEGIN
    SELECT COUNT(*) FROM users WHERE money > 10000000;
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để lấy ID của người dùng dựa trên tên người dùng
CREATE PROCEDURE GetUserId(IN p_username VARCHAR(255))
BEGIN
    SELECT user_id FROM users WHERE username = p_username;
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để lấy thông tin tài khoản
CREATE PROCEDURE GetAccount()
BEGIN
    SELECT * FROM accounts;
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để chèn thông tin người dùng mới
CREATE PROCEDURE InsertUser(IN p_username VARCHAR(255), IN p_name VARCHAR(255), IN p_email VARCHAR(255), IN p_phonenumber VARCHAR(255), IN p_avatar VARCHAR(255), IN p_point INT)
BEGIN
    INSERT INTO users (username, name, email, phonenumber, avatar, point)
    VALUES (p_username, p_name, p_email, p_phonenumber, p_avatar, p_point);
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để chèn thông tin tài khoản mới
CREATE PROCEDURE InsertAccount(IN p_username VARCHAR(255), IN p_password VARCHAR(255), IN p_type VARCHAR(255))
BEGIN
    INSERT INTO accounts (username, password, type)
    VALUES (p_username, p_password, p_type);
END //
DELIMITER ;

DELIMITER //
-- Tạo Stored Procedure để cập nhật thông tin tài khoản
CREATE PROCEDURE UpdateAccount(IN p_username VARCHAR(255), IN p_password VARCHAR(255), IN p_newpassword VARCHAR(255))
BEGIN
    UPDATE accounts SET password = p_newpassword WHERE username = p_username AND password = p_password;
END //
DELIMITER ;

----------------------------User_Controller----------------------------
DELIMITER //
CREATE PROCEDURE GetUser(IN p_username VARCHAR(255))
BEGIN
    SELECT * FROM users WHERE username = p_username;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetPoint(IN p_username VARCHAR(255))
BEGIN
    SELECT point FROM users WHERE username = p_username;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateUser(IN p_name VARCHAR(255), IN p_phone VARCHAR(255), IN p_dob DATE, IN p_email VARCHAR(255), IN p_id INT)
BEGIN
    UPDATE users SET name = p_name, phonenumber = p_phone, birthday = p_dob, email = p_email WHERE user_id = p_id;
END //
DELIMITER ;

----------------------------Product_Controller----------------------------
DELIMITER //
CREATE PROCEDURE GetProducts()
BEGIN
    SELECT p.*, d.rating
    FROM product p
    LEFT JOIN product_detailed d ON p.product_id = d.product_id
    ORDER BY p.created_time DESC
    LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetProductItem(IN p_productID INT)
BEGIN
    SELECT *
    FROM product
    WHERE product_id = p_productID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetProductDetail(IN p_productID INT)
BEGIN
    SELECT *
    FROM product_detailed
    WHERE product_id = p_productID;
END //
DELIMITER ;

----------------------------Product_Controller----------------------------
DELIMITER //
CREATE PROCEDURE GetProductAdmin()
BEGIN
    SELECT *
    FROM product;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetBrand()
BEGIN
    SELECT brand_name
    FROM Brand;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetBrandID(IN p_brand_name VARCHAR(255))
BEGIN
    SELECT brand_id
    FROM Brand
    WHERE brand_name = p_brand_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE InsertProduct(IN p_product_id INT, IN p_category VARCHAR(255), IN p_inventory INT, IN p_product_name VARCHAR(255), IN p_product_photo VARCHAR(255), IN p_description TEXT, IN p_price DECIMAL(10, 2), IN p_brand VARCHAR(255), IN p_gender VARCHAR(255))
BEGIN
    INSERT INTO Product (product_id, category, inventory, product_name, product_photo, description, Price, brand, gender)
    VALUES (p_product_id, p_category, p_inventory, p_product_name, p_product_photo, p_description, p_price, p_brand, p_gender);
END //
DELIMITER ;

-- Stored procedure to insert the sizes
DELIMITER //
CREATE PROCEDURE InsertProductSizes()
BEGIN
    -- Insert sizes for product category 'Shoes'
    INSERT INTO Product_Size (product_id, size)
    SELECT product_id, '35' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '36' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '37' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '38' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '39' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '40' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '41' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, '42' FROM Product WHERE category = (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes');
    
    -- Insert sizes for other categories
    INSERT INTO Product_Size (product_id, size)
    SELECT product_id, 'S' FROM Product WHERE category <> (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, 'M' FROM Product WHERE category <> (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, 'L' FROM Product WHERE category <> (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes')
    UNION ALL
    SELECT product_id, 'XL' FROM Product WHERE category <> (SELECT cate_id FROM Product_category WHERE product_name = 'Shoes');
END //

DELIMITER ;

CALL InsertProductSizes();

-- Get product size in productDetail
DELIMITER //
CREATE PROCEDURE GetProductSizes(IN productID INT)
BEGIN
    SELECT size 
    FROM Product_Size
    WHERE product_id = productID;
END //
DELIMITER ;

----------------------------Category_Controller----------------------------
DELIMITER //
CREATE PROCEDURE GetAllCategories()
BEGIN
    SELECT *
    FROM Product_category;
END //
DELIMITER ;

----------------------------Bills_Controller----------------------------
DELIMITER //
CREATE PROCEDURE InsertBills(
    IN p_order_Id INT,
    IN p_customer_id INT,
    IN p_name VARCHAR(255),
    IN p_address VARCHAR(255),
    IN p_Additional VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_phonenumber VARCHAR(255),
    IN p_total_amount DECIMAL(10, 2),
    IN p_payment_kind VARCHAR(255),
    IN p_transaction_id VARCHAR(255),
    IN p_billing_date DATE
)
BEGIN
    INSERT INTO Bills (order_Id, customer_id, name, address, Additional, email, phonenumber, total_amount, payment_kind, transaction_id, billing_date)
    VALUES (p_order_Id, p_customer_id, p_name, p_address, p_Additional, p_email, p_phonenumber, p_total_amount, p_payment_kind, p_transaction_id, p_billing_date);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetBillsCount()
BEGIN
    SELECT COUNT(*) FROM Bills;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetBills()
BEGIN
    SELECT us.username, us.avatar, bi.billing_date
    FROM users us, bills bi
    WHERE us.user_id = bi.customer_id;
END //
DELIMITER ;

----------------------------Notify_Controller----------------------------
DELIMITER //
CREATE PROCEDURE GetNotify()
BEGIN
    SELECT *
    FROM Notifi;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE InsertNotifyUser(
    IN p_notifi_id INT,
    IN p_user_id INT
)
BEGIN
    INSERT INTO notifi_user (Notifi_id, customer_id)
    VALUES (p_notifi_id, p_user_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ExistsInNotifyUser(
    IN p_notifi_id INT,
    IN p_user_id INT,
    OUT p_exists INT
)
BEGIN
    SELECT COUNT(*) INTO p_exists
    FROM notifi_user
    WHERE Notifi_id = p_notifi_id AND customer_id = p_user_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetNotifyUser(
    IN p_user_id INT
)
BEGIN
    SELECT n.header, n.detailed, n.image
    FROM notifi_user nu, Notifi n
    WHERE nu.Notifi_id = n.Notifi_id AND nu.Customer_id = p_user_id;
END //
DELIMITER ;