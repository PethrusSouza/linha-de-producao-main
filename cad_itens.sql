CREATE TABLE cad_itens (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    P_12 INT,
    descricao_item VARCHAR(300) NOT NULL,
    medidas ENUM('BL', 'TL', 'M²', 'CM', 'UND'),
    acabamento VARCHAR(300) NOT NULL
);
