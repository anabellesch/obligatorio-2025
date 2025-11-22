USE gestion_salas;

-- Logins (passwords se guardan hasheadas)
INSERT INTO login (correo, password_hash, rol_sistema, ci_participante)
VALUES ('ana.gomez@example.com', 'PENDING_HASH', 'admin', '1000001'),
       ('juan.perez@example.com', 'PENDING_HASH', 'usuario', '1000002');