SELECT
  (SELECT COUNT(*) FROM wm_loan_policies) AS count_loan_policies,
  (SELECT COUNT(*) FROM wm_user_status) AS count_user_status,
  (SELECT COUNT(*) FROM wm_user_role) AS count_user_role,
  (SELECT COUNT(*) FROM wm_copy_status) AS count_copy_status,
  (SELECT COUNT(*) FROM wm_reservation_status) AS count_reservation_status,
  (SELECT COUNT(*) FROM wm_loan_status) AS count_loan_status,
  (SELECT COUNT(*) FROM wm_regions) AS count_regions,
  (SELECT COUNT(*) FROM wm_provinces) AS count_provinces,
  (SELECT COUNT(*) FROM wm_communes) AS count_communes;

SELECT
  (SELECT COUNT(*) FROM wm_notifications) AS count_notifications,
  (SELECT COUNT(*) FROM wm_loans) AS count_loans,
  (SELECT COUNT(*) FROM wm_reservations) AS count_reservations,
  (SELECT COUNT(*) FROM wm_users) AS count_users;

DROP TABLE IF EXISTS wm_notifications CASCADE;
DROP TABLE IF EXISTS wm_loans CASCADE;
DROP TABLE IF EXISTS wm_reservations CASCADE;
DROP TABLE IF EXISTS wm_news_gallery CASCADE;
DROP TABLE IF EXISTS wm_book_author CASCADE;
DROP TABLE IF EXISTS wm_book_subject CASCADE;
DROP TABLE IF EXISTS wm_edition_format CASCADE;
DROP TABLE IF EXISTS wm_copies CASCADE;
DROP TABLE IF EXISTS wm_editions CASCADE;
DROP TABLE IF EXISTS wm_books CASCADE;
DROP TABLE IF EXISTS wm_news CASCADE;
DROP TABLE IF EXISTS wm_users CASCADE;
DROP TABLE IF EXISTS wm_communes CASCADE;
DROP TABLE IF EXISTS wm_provinces CASCADE;
DROP TABLE IF EXISTS wm_regions CASCADE;
DROP TABLE IF EXISTS wm_user_role CASCADE;
DROP TABLE IF EXISTS wm_user_status CASCADE;
DROP TABLE IF EXISTS wm_reservation_status CASCADE;
DROP TABLE IF EXISTS wm_loan_status CASCADE;
DROP TABLE IF EXISTS wm_copy_status CASCADE;
DROP TABLE IF EXISTS wm_editorials CASCADE;
DROP TABLE IF EXISTS wm_authors CASCADE;
DROP TABLE IF EXISTS wm_subjects CASCADE;
DROP TABLE IF EXISTS wm_genres CASCADE;
DROP TABLE IF EXISTS wm_formats CASCADE;
DROP TABLE IF EXISTS wm_loan_policies CASCADE;

-- ---------------------------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS wm_regions (
  id_region INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  region VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE IF NOT EXISTS wm_provinces (
  id_province INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  province VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  region_id INTEGER NOT NULL,
  CONSTRAINT provinces_regions_fk FOREIGN KEY (region_id) REFERENCES wm_regions(id_region)
);

CREATE TABLE IF NOT EXISTS wm_communes (
  id_commune INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  province_id INTEGER NOT NULL,
  CONSTRAINT communes_provinces_fk FOREIGN KEY (province_id) REFERENCES wm_provinces(id_province)
);

CREATE TABLE IF NOT EXISTS wm_user_status (
  id_user_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(45),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE IF NOT EXISTS wm_user_role (
  id_user_role INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_users (
  id_user UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(100),
  name VARCHAR(45),
  lastname VARCHAR(45),
  rut VARCHAR(12),
  address VARCHAR(256),
  phone VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  commune_id INTEGER,
  user_role_id INTEGER NOT NULL,
  user_status_id INTEGER NOT NULL,
  CONSTRAINT users_commune_fk FOREIGN KEY (commune_id) REFERENCES wm_communes(id_commune),
  CONSTRAINT users_types_fk FOREIGN KEY (user_role_id) REFERENCES wm_user_role(id_user_role),
  CONSTRAINT users_status_fk FOREIGN KEY (user_status_id) REFERENCES wm_user_status(id_user_status)
);

CREATE TABLE IF NOT EXISTS wm_news (
  id_news INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1),
  title VARCHAR(100) NOT NULL,
  subtitle VARCHAR(256) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_news_gallery (
  id_news_gallery INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1),
  alt VARCHAR(100) NOT NULL,
  url VARCHAR(256) NOT NULL,
  news_id INTEGER NOT NULL,
  CONSTRAINT news_gallery_fk FOREIGN KEY (news_id) REFERENCES wm_news(id_news)
);

CREATE TABLE IF NOT EXISTS wm_authors (
  id_author INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_editorials (
  id_editorial INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_subjects (
  id_subject INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_genres (
  id_genre INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_formats (
  id_format INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_copy_status (
  id_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS wm_books (
  id_book INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  summary TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  genre_id INTEGER NOT NULL,

  CONSTRAINT wm_genres_wm_books_fk FOREIGN KEY (genre_id) REFERENCES wm_genres(id_genre)
);

CREATE TABLE IF NOT EXISTS wm_editions (
  id_edition INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  edition VARCHAR(50),
  isbn VARCHAR(20),
  publication_year INTEGER NOT NULL,
  pages INTEGER NOT NULL,
  cover_image VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  book_id INTEGER NOT NULL,
  editorial_id INTEGER NOT NULL,
  
  CONSTRAINT wm_editions_wm_books_fk FOREIGN KEY (book_id) REFERENCES wm_books(id_book),
  CONSTRAINT wm_editions_wm_editorials_fk FOREIGN KEY (editorial_id) REFERENCES wm_editorials(id_editorial)
);

CREATE TABLE IF NOT EXISTS wm_edition_format (
  id_format INTEGER NOT NULL,
  id_edition INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_edition_format PRIMARY KEY (id_edition, id_format),
  CONSTRAINT fk_ef_format FOREIGN KEY (id_format) REFERENCES wm_formats(id_format),
  CONSTRAINT fk_ef_edition FOREIGN KEY (id_edition) REFERENCES wm_editions(id_edition)
);

CREATE TABLE IF NOT EXISTS wm_copies (
  id_copy INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  barcode VARCHAR(100) NOT NULL UNIQUE,
  signature_topography VARCHAR(100) NOT NULL UNIQUE,
  copy_number INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  edition_id INTEGER NOT NULL,
  status_id INTEGER NOT NULL,

  CONSTRAINT wm_copies_wm_editions_fk FOREIGN KEY (edition_id) REFERENCES wm_editions(id_edition),
  CONSTRAINT wm_copies_wm_status_fk FOREIGN KEY (status_id) REFERENCES wm_copy_status(id_status)
);

CREATE TABLE IF NOT EXISTS wm_book_author (
  id_author INTEGER NOT NULL,
  id_book INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_book_author PRIMARY KEY (id_book, id_author),
  CONSTRAINT fk_ba_book FOREIGN KEY (id_book) REFERENCES wm_books(id_book),
  CONSTRAINT fk_ba_author FOREIGN KEY (id_author) REFERENCES wm_authors(id_author)
);

CREATE TABLE IF NOT EXISTS wm_book_subject (
  id_subject INTEGER NOT NULL,
  id_book INTEGER NOT NULL,  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_book_subject PRIMARY KEY (id_book, id_subject),
  CONSTRAINT fk_bs_book FOREIGN KEY (id_book) REFERENCES wm_books(id_book),
  CONSTRAINT fk_bs_subject FOREIGN KEY (id_subject) REFERENCES wm_subjects(id_subject)
);

CREATE TABLE IF NOT EXISTS wm_reservation_status (
  id_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS wm_reservations (
  id_reservation INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 10000) PRIMARY KEY,
  reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expiration_date TIMESTAMP NOT NULL,

  user_id UUID NOT NULL,
  copy_id INTEGER NOT NULL,
  reservation_status_id INTEGER NOT NULL DEFAULT 1,

  CONSTRAINT fk_res_user FOREIGN KEY (user_id) REFERENCES wm_users(id_user),
  CONSTRAINT fk_res_copy FOREIGN KEY (copy_id) REFERENCES wm_copies(id_copy),
  CONSTRAINT fk_res_status FOREIGN KEY (reservation_status_id) REFERENCES wm_reservation_status(id_status)
);

CREATE TABLE IF NOT EXISTS wm_loan_status (
  id_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS wm_loans (
  id_loan INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 10000) PRIMARY KEY,
  loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
  due_date DATE NOT NULL,
  return_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  copy_id INTEGER NOT NULL,
  user_id UUID NOT NULL,
  loan_status_id INTEGER NOT NULL DEFAULT 1,

  CONSTRAINT loans_copies_fk FOREIGN KEY (copy_id) REFERENCES wm_copies(id_copy),
  CONSTRAINT loans_users_fk FOREIGN KEY (user_id) REFERENCES wm_users(id_user),
  CONSTRAINT loans_status_fk FOREIGN KEY (loan_status_id) REFERENCES wm_loan_status(id_status)
);

CREATE TABLE IF NOT EXISTS wm_loan_policies (
  id_policy INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(100),
  max_books INTEGER,
  max_days INTEGER,
  reservation_days INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS wm_notifications (
  id_notification INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  message TEXT NOT NULL,
  is_priority BOOLEAN DEFAULT FALSE,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  user_id UUID NOT NULL,

  CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES wm_users(id_user)
);

CREATE INDEX idx_notif_user ON wm_notifications(user_id);
CREATE INDEX idx_notif_user_unread ON wm_notifications(user_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_edition_isbn ON wm_editions(isbn);
CREATE INDEX idx_book_title ON wm_books(title);
CREATE INDEX idx_book_summary ON wm_books(summary);
CREATE INDEX idx_book_genre ON wm_books(genre_id);
CREATE INDEX idx_author_id ON wm_book_author(id_author);
CREATE INDEX idx_editorial_id ON wm_editions(editorial_id);
CREATE INDEX idx_reservation_copy ON wm_reservations(copy_id);
CREATE INDEX idx_reservation_user ON wm_reservations(user_id);

-- ---------------------------------------------------------------------------------

INSERT INTO wm_loan_policies (name, max_books, max_days, reservation_days) VALUES
('Lectores', 3, 14, 3);

INSERT INTO wm_user_status (name)
VALUES 
('Activo/a'),
('Deudor/a'),
('Bloqueado/a');

INSERT INTO wm_user_role (name)
VALUES 
('Super Admin'),
('Admin'),
('Lector');

INSERT INTO wm_copy_status (name) VALUES
('Disponible'),
('En reparación'),
('Extraviado'),
('Dado de baja');

INSERT INTO wm_reservation_status (name) VALUES
('Pendiente de retiro'),
('Completada'),
('Cancelada'),
('Vencido');

INSERT INTO wm_loan_status (name) VALUES
('En Préstamo'),
('Devuelto'),
('Vencido');

INSERT INTO wm_formats (name) VALUES
('Versión Original completa'),
('Versión Comentada'),
('Versión Resumida'),
('Adaptación infantil'),
('Adaptación juvenil'),
('Traducción / Bilingüe'),
('Idioma inglés'),
('Adaptación moderna'),
('Edición Ilustrada'),
('Accesible (tipografía grande)'),
('Libro álbum');

INSERT INTO wm_regions (region) VALUES
('Región de Arica y Parinacota'),
('Región de Tarapacá'),
('Región de Antofagasta'),
('Región de Atacama'),
('Región de Coquimbo'),
('Región de Valparaíso'),
('Región Metropolitana de Santiago'),
('Región del Libertador General Bernardo O''Higgins'),
('Región del Maule'),
('Región de Ñuble'),
('Región del Biobío'),
('Región de La Araucanía'),
('Región de Los Ríos'),
('Región de Los Lagos'),
('Región de Aysén del General Carlos Ibáñez del Campo'),
('Región de Magallanes y de la Antártica Chilena');

INSERT INTO wm_provinces (province, region_id) VALUES
('Arica', 1),
('Parinacota', 1),
('Iquique', 2),
('Tamarugal', 2),
('Antofagasta', 3),
('El Loa', 3),
('Tocopilla', 3),
('Chañaral', 4),
('Copiapó', 4),
('Huasco', 4),
('Elqui', 5),
('Limarí', 5),
('Choapa', 5),
('Valparaíso', 6),
('Isla de Pascua', 6),
('Los Andes', 6),
('Petorca', 6),
('San Antonio', 6),
('San Felipe de Aconcagua', 6),
('Quillota', 6),
('Marga Marga', 6),
('Santiago', 7),
('Cordillera', 7),
('Chacabuco', 7),
('Maipo', 7),
('Melipilla', 7),
('Talagante', 7),
('Cachapoal', 8),
('Cardenal Caro', 8),
('Colchagua', 8),
('Talca', 9),
('Curicó', 9),
('Linares', 9),
('Cauquenes', 9),
('Diguillín', 10),
('Itata', 10),
('Punilla', 10),
('Concepción', 11),
('Biobío', 11),
('Arauco', 11),
('Cautín', 12),
('Malleco', 12),
('Valdivia', 13),
('Ranco', 13),
('Llanquihue', 14),
('Chiloé', 14),
('Osorno', 14),
('Palena', 14),
('Coyhaique', 15),
('Aysén', 15),
('General Carrera', 15),
('Capitán Prat', 15),
('Magallanes', 16),
('Última Esperanza', 16),
('Tierra del Fuego', 16),
('Antártica Chilena', 16);

INSERT INTO wm_communes (name, province_id) VALUES
-- Región de Arica y Parinacota
('Arica', 1),
('Camarones', 1),
('Putre', 2),
('General Lagos', 2),
-- Región de Tarapacá
('Iquique', 3),
('Alto Hospicio', 3),
('Pozo Almonte', 4),
('Camiña', 4),
('Colchane', 4),
('Huara', 4),
('Pica', 4),
-- Región de Antofagasta
('Antofagasta', 5),
('Mejillones', 5),
('Sierra Gorda', 5),
('Taltal', 5),
('Calama', 6),
('Ollagüe', 6),
('San Pedro de Atacama', 6),
('Tocopilla', 7),
('María Elena', 7),
-- Región de Atacama
('Chañaral', 8),
('Diego de Almagro', 8),
('Copiapó', 9),
('Caldera', 9),
('Tierra Amarilla', 9),
('Vallenar', 10),
('Alto del Carmen', 10),
('Freirina', 10),
('Huasco', 10),
-- Región de Coquimbo
('La Serena', 11),
('Coquimbo', 11),
('Andacollo', 11),
('Vicuña', 11),
('Paihuano', 11),
('La Higuera', 11),
('Ovalle', 12),
('Monte Patria', 12),
('Punitaqui', 12),
('Combarbalá', 12),
('Río Hurtado', 12),
('Illapel', 13),
('Canela', 13),
('Los Vilos', 13),
('Salamanca', 13),
-- Región de Valparaíso
('Valparaíso', 14),
('Viña del Mar', 14),
('Concón', 14),
('Quintero', 14),
('Puchuncaví', 14),
('Casablanca', 14),
('Juan Fernández', 14),
('Isla de Pascua', 15),
('Los Andes', 16),
('San Esteban', 16),
('Calle Larga', 16),
('Rinconada', 16),
('Petorca', 17),
('La Ligua', 17),
('Cabildo', 17),
('Papudo', 17),
('Zapallar', 17),
('San Antonio', 18),
('Cartagena', 18),
('El Tabo', 18),
('El Quisco', 18),
('Algarrobo', 18),
('Santo Domingo', 18),
('San Felipe', 19),
('Putaendo', 19),
('Santa María', 19),
('Panquehue', 19),
('Llaillay', 19),
('Catemu', 19),
('Quillota', 20),
('La Calera', 20),
('Hijuelas', 20),
('La Cruz', 20),
('Nogales', 20),
('Quilpué', 21),
('Villa Alemana', 21),
('Limache', 21),
('Olmué', 21),
-- Región Metropolitana de Santiago
('Santiago', 22),
('Cerrillos', 22),
('Cerro Navia', 22),
('Conchalí', 22),
('El Bosque', 22),
('Estación Central', 22),
('Huechuraba', 22),
('Independencia', 22),
('La Cisterna', 22),
('La Florida', 22),
('La Granja', 22),
('La Pintana', 22),
('La Reina', 22),
('Las Condes', 22),
('Lo Barnechea', 22),
('Lo Espejo', 22),
('Lo Prado', 22),
('Macul', 22),
('Maipú', 22),
('Ñuñoa', 22),
('Pedro Aguirre Cerda', 22),
('Peñalolén', 22),
('Providencia', 22),
('Pudahuel', 22),
('Quilicura', 22),
('Quinta Normal', 22),
('Recoleta', 22),
('Renca', 22),
('San Joaquín', 22),
('San Miguel', 22),
('San Ramón', 22),
('Vitacura', 22),
('Puente Alto', 23),
('Pirque', 23),
('San José de Maipo', 23),
('Colina', 24),
('Lampa', 24),
('Til Til', 24),
('San Bernardo', 25),
('Buin', 25),
('Calera de Tango', 25),
('Paine', 25),
('Melipilla', 26),
('Alhué', 26),
('Curacaví', 26),
('María Pinto', 26),
('San Pedro', 26),
('Talagante', 27),
('Peñaflor', 27),
('El Monte', 27),
('Isla de Maipo', 27),
('Padre Hurtado', 27),
-- Región de O'Higgins
('Rancagua', 28),
('Machalí', 28),
('Graneros', 28),
('Mostazal', 28),
('Codegua', 28),
('Olivar', 28),
('Doñihue', 28),
('Requínoa', 28),
('Rengo', 28),
('Malloa', 28),
('San Vicente', 28),
('Peumo', 28),
('Las Cabras', 28),
('Coltauco', 28),
('Coinco', 28),
('Quinta de Tilcoco', 28),
('Pichidegua', 28),
('Pichilemu', 29),
('La Estrella', 29),
('Litueche', 29),
('Navidad', 29),
('Marchigüe', 29),
('Paredones', 29),
('San Fernando', 30),
('Chimbarongo', 30),
('Nancagua', 30),
('Placilla', 30),
('Santa Cruz', 30),
('Palmilla', 30),
('Peralillo', 30),
('Pumanque', 30),
('Chépica', 30),
('Lolol', 30),
-- Región del Maule
('Talca', 31),
('Constitución', 31),
('Curepto', 31),
('Empedrado', 31),
('Maule', 31),
('Pelarco', 31),
('Pencahue', 31),
('Río Claro', 31),
('San Clemente', 31),
('San Javier', 31),
('Curicó', 32),
('Hualañé', 32),
('Licantén', 32),
('Molina', 32),
('Rauco', 32),
('Romeral', 32),
('Sagrada Familia', 32),
('Teno', 32),
('Vichuquén', 32),
('Linares', 33),
('Colbún', 33),
('Longaví', 33),
('Parral', 33),
('Retiro', 33),
('San Fabián', 33),
('Villa Alegre', 33),
('Yerbas Buenas', 33),
('Cauquenes', 34),
('Chanco', 34),
('Pelluhue', 34),
-- Región de Ñuble
('Chillán', 35),
('Chillán Viejo', 35),
('Bulnes', 35),
('Yungay', 35),
('Pemuco', 35),
('Pinto', 35),
('El Carmen', 35),
('San Ignacio', 35),
('Quillón', 35),
('Quirihue', 36),
('Cobquecura', 36),
('Ninhue', 36),
('Ránquil', 36),
('Treguaco', 36),
('Portezuelo', 36),
('Coelemu', 36),
('San Carlos', 37),
('San Fabián', 37),
('San Nicolás', 37),
('Coihueco', 37),
('Ñiquén', 37),
-- Región del Biobío
('Concepción', 38),
('Coronel', 38),
('Chiguayante', 38),
('Florida', 38),
('Hualqui', 38),
('Lota', 38),
('Penco', 38),
('San Pedro de la Paz', 38),
('Santa Juana', 38),
('Talcahuano', 38),
('Tomé', 38),
('Hualpén', 38),
('Los Ángeles', 39),
('Antuco', 39),
('Cabrero', 39),
('Laja', 39),
('Mulchén', 39),
('Nacimiento', 39),
('Negrete', 39),
('Quilaco', 39),
('Quilleco', 39),
('San Rosendo', 39),
('Santa Bárbara', 39),
('Tucapel', 39),
('Yumbel', 39),
('Alto Biobío', 39),
('Lebu', 40),
('Arauco', 40),
('Cañete', 40),
('Contulmo', 40),
('Curanilahue', 40),
('Los Álamos', 40),
('Tirúa', 40),
-- Región de La Araucanía
('Temuco', 41),
('Carahue', 41),
('Cunco', 41),
('Curarrehue', 41),
('Freire', 41),
('Galvarino', 41),
('Gorbea', 41),
('Lautaro', 41),
('Loncoche', 41),
('Melipeuco', 41),
('Nueva Imperial', 41),
('Padre Las Casas', 41),
('Perquenco', 41),
('Pitrufquén', 41),
('Pucón', 41),
('Saavedra', 41),
('Teodoro Schmidt', 41),
('Toltén', 41),
('Vilcún', 41),
('Villarrica', 41),
('Cholchol', 41),
('Angol', 42),
('Collipulli', 42),
('Curacautín', 42),
('Ercilla', 42),
('Lonquimay', 42),
('Los Sauces', 42),
('Lumaco', 42),
('Purén', 42),
('Renaico', 42),
('Traiguén', 42),
('Victoria', 42),
-- Región de Los Ríos
('Valdivia', 43),
('Mariquina', 43),
('Lanco', 43),
('Los Lagos', 43),
('Paillaco', 43),
('Panguipulli', 43),
('Corral', 43),
('Máfil', 43),
('La Unión', 44),
('Futrono', 44),
('Lago Ranco', 44),
('Río Bueno', 44),
-- Región de Los Lagos
('Puerto Montt', 45),
('Puerto Varas', 45),
('Llanquihue', 45),
('Frutillar', 45),
('Fresia', 45),
('Los Muermos', 45),
('Maullín', 45),
('Calbuco', 45),
('Cochamó', 45),
('Castro', 46),
('Ancud', 46),
('Chonchi', 46),
('Curaco de Vélez', 46),
('Dalcahue', 46),
('Puqueldón', 46),
('Queilén', 46),
('Quellón', 46),
('Quinchao', 46),
('Quemchi', 46),
('Osorno', 47),
('Puerto Octay', 47),
('Purranque', 47),
('Puyehue', 47),
('Río Negro', 47),
('San Juan de la Costa', 47),
('San Pablo', 47),
('Chaitén', 48),
('Futaleufú', 48),
('Hualaihué', 48),
('Palena', 48),
-- Región de Aysén
('Coyhaique', 49),
('Lago Verde', 49),
('Aysén', 50),
('Cisnes', 50),
('Guaitecas', 50),
('Chile Chico', 51),
('Río Ibáñez', 51),
('Cochrane', 52),
('O''Higgins', 52),
('Tortel', 52),
-- Región de Magallanes y de la Antártica Chilena
('Punta Arenas', 53),
('Laguna Blanca', 53),
('Río Verde', 53),
('San Gregorio', 53),
('Puerto Natales', 54),
('Torres del Paine', 54),
('Porvenir', 55),
('Primavera', 55),
('Timaukel', 55),
('Cabo de Hornos', 56),
('Antártica', 56);
