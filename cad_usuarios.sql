 CREATE TABLE cad_usuarios (
 id_usuario int primary key auto_increment,
 nome varchar (50) not null,
 funcao varchar (50),
 nivel_acesso enum ('ADMIM', 'GERENTE', 'OPERADOR') NOT NULL,
 usuario varchar (50) unique not null,
 senha varchar (100) not null
 );