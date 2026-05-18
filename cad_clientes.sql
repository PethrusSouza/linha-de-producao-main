CREATE TABLE cad_clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome_cliente VARCHAR(100) NOT NULL UNIQUE,
    cnpj VARCHAR(20),
    endereco VARCHAR(50)
);
