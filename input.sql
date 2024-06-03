-- Este es un comentario
CREATE TABLE empleados (       
    id INT PRIMARY KEY,        
    nombre VARCHAR(50),        
    salario DECIMAL(10, 2)     
);

INSERT INTO empleados (id, nombre, salario) VALUES (1, 'Juan', 3000.50); 

SELECT nombre, salario          
FROM empleados                  
WHERE salario > 2500;           
