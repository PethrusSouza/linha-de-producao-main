create table Ordem_servico(
num_pedido varchar (20) primary key,
nome_cliente varchar (100) not null,
status_geral ENUM(
        'EM_PRODUCAO',
        'FINALIZADA',
        'NF_EMITIDA',
        'ENTREGUE'
    ) DEFAULT 'EM_PRODUCAO',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foreign key (nome_cliente) references cad_clientes(nome_cliente)
);