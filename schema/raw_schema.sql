
CREATE TABLE `sales_data` (
  `OrderID` varchar(10) DEFAULT NULL,
  `CustomerID` varchar(10) DEFAULT NULL,
  `CustomerName` varchar(50) DEFAULT NULL,
  `Region` varchar(30) DEFAULT NULL,
  `ProductID` varchar(10) DEFAULT NULL,
  `ProductName` varchar(50) DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `TotalAmount` decimal(12,2) DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  `SalesChannel` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


