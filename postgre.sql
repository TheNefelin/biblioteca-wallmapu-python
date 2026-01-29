DROP TABLE IF EXISTS wm_communes;
DROP TABLE IF EXISTS wm_user_status;
DROP TABLE IF EXISTS wm_user_role;
DROP TABLE IF EXISTS wm_users;

SELECT * FROM wm_communes;
SELECT * FROM wm_user_status;
SELECT * FROM wm_user_role;
SELECT * FROM wm_users;

CREATE TABLE wm_communes (
  id_commune INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  commune VARCHAR(45),
  province_id INTEGER,
  CONSTRAINT wm_communs_wm_provinces_fk
    FOREIGN KEY (province_id) REFERENCES wm_provinces(id_province)
);

CREATE TABLE wm_user_status (
  id_user_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  status VARCHAR(45)
);

CREATE TABLE wm_user_role (
  id_user_role INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  role VARCHAR(45) NOT NULL
);

CREATE TABLE wm_users (
  id_user INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email VARCHAR(100),
  name VARCHAR(45),
  lastname VARCHAR(45),
  rut VARCHAR(12),
  address VARCHAR(256),
  phone VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  commune_id INTEGER,
  user_role_id INTEGER,
  user_status_id INTEGER,
  -- CONSTRAINT users_commune_fk FOREIGN KEY (commune_id) REFERENCES wm_communs(id_commun),
  CONSTRAINT users_types_fk FOREIGN KEY (user_role_id) REFERENCES wm_user_role(id_user_role),
  CONSTRAINT users_status_fk FOREIGN KEY (user_status_id) REFERENCES wm_user_status(id_user_status)
);

INSERT INTO wm_user_status (status)
VALUES 
('Activo/a'),
('Activo/a'),
('Bloqueado/a')

INSERT INTO wm_user_role (role)
VALUES 
('Super Admin'),
('Admin'),
('Lector')