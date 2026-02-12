DROP TABLE IF EXISTS wm_communes;
DROP TABLE IF EXISTS wm_user_status;
DROP TABLE IF EXISTS wm_user_role;
DROP TABLE IF EXISTS wm_users;

DROP TABLE wm_news;
DROP TABLE wm_news_gallery;

SELECT * FROM wm_communes;
SELECT * FROM wm_user_status;
SELECT * FROM wm_user_role;
SELECT * FROM wm_users;

SELECT * FROM wm_news;
SELECT * FROM wm_news_gallery;

CREATE TABLE IF NOT EXISTS wm_communes (
  id_commune INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  commune VARCHAR(45),
  province_id INTEGER,
  CONSTRAINT wm_communs_wm_provinces_fk
    FOREIGN KEY (province_id) REFERENCES wm_provinces(id_province)
);

CREATE TABLE IF NOT EXISTS wm_user_status (
  id_user_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  status VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS wm_user_role (
  id_user_role INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  role VARCHAR(45) NOT NULL
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
  user_role_id INTEGER,
  user_status_id INTEGER,
  -- CONSTRAINT users_commune_fk FOREIGN KEY (commune_id) REFERENCES wm_communs(id_commun),
  CONSTRAINT users_types_fk FOREIGN KEY (user_role_id) REFERENCES wm_user_role(id_user_role),
  CONSTRAINT users_status_fk FOREIGN KEY (user_status_id) REFERENCES wm_user_status(id_user_status)
);

CREATE TABLE IF NOT EXISTS wm_news (
  id_news INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1),
  title VARCHAR(45) NOT NULL,
  subtitle VARCHAR(256) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_news_gallery (
  id_news_gallery INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY (INCREMENT 1),
  alt VARCHAR(45) NOT NULL,
  url VARCHAR(256) NOT NULL,
  news_id INTEGER,
  CONSTRAINT news_gallery_fk FOREIGN KEY (news_id) REFERENCES wm_news(id_news)
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

INSERT INTO wm_news (title, subtitle, body, created_at, updated_at)
VALUES 
('Nueva Ley de Tecnología', 
 'El congreso aprueba nueva legislación sobre innovación tecnológica y startups.', 
 'Hoy se aprobó una nueva ley que busca fomentar la innovación tecnológica y proteger a las startups locales, garantizando inversión y desarrollo sostenible.', 
 '2026-02-01', '2026-02-01'),
('Descubrimiento Científico', 
 'Científicos anuncian un avance en la investigación de células madre.', 
 'Investigadores han logrado un avance significativo en la manipulación de células madre para regeneración de tejidos, lo que podría revolucionar la medicina.', 
 '2026-02-02', '2026-02-02'),
('Festival Cultural 2026', 
 'La ciudad prepara el festival anual con exposiciones y conciertos.', 
 'El festival cultural de este año incluirá exposiciones de arte, conciertos en vivo y actividades para toda la familia, promoviendo la cultura local e internacional.', 
 '2026-02-03', '2026-02-03'),
('Avances en Energía Solar', 
 'Nueva tecnología solar aumenta la eficiencia energética en un 20%.', 
 'Una empresa nacional ha desarrollado paneles solares con mayor eficiencia, permitiendo reducir costos y aumentar la capacidad de generación eléctrica renovable.', 
 '2026-02-04', '2026-02-04'),
('Deporte Local Destacado', 
 'Equipo de fútbol juvenil gana campeonato regional.', 
 'El equipo juvenil de la ciudad se coronó campeón regional, destacando el esfuerzo y talento de los jóvenes deportistas en competiciones locales y nacionales.', 
 '2026-02-05', '2026-02-05'),
('Innovación Educativa', 
 'Escuelas implementan nueva metodología de aprendizaje digital.', 
 'Las instituciones educativas comienzan a implementar plataformas digitales interactivas para mejorar el aprendizaje de los estudiantes y preparar competencias del siglo XXI.', 
 '2026-02-06', '2026-02-06'),
('Salud y Bienestar', 
 'Campaña de vacunación contra la gripe alcanza nuevas metas.', 
 'La reciente campaña de vacunación ha logrado cubrir a más del 80% de la población objetivo, previniendo enfermedades respiratorias y promoviendo hábitos saludables.', 
 '2026-02-07', '2026-02-07'),
('Arte Urbano', 
 'Mural gigante embellece el centro de la ciudad.', 
 'Un grupo de artistas locales ha creado un mural que representa la diversidad cultural y la historia de la ciudad, convirtiéndose en un atractivo turístico y educativo.', 
 '2026-02-08', '2026-02-08'),
('Tecnología Verde', 
 'Empresa lanza iniciativa de reciclaje electrónico.', 
 'Una compañía tecnológica inicia un programa de reciclaje de dispositivos electrónicos, fomentando la economía circular y reduciendo el impacto ambiental de residuos electrónicos.', 
 '2026-02-09', '2026-02-09'),
('Exploración Espacial', 
 'Nueva misión espacial promete descubrimientos sobre Marte.', 
 'La agencia espacial anunció el lanzamiento de una misión para estudiar la superficie de Marte, buscando información sobre su geología, clima y posibilidad de vida pasada.', 
 '2026-02-10', '2026-02-10');

INSERT INTO wm_news_gallery (alt, url, news_id)
VALUES 
('Aloy', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860243/news/ruatveggaye123paqwbv.webp', 10),
('Aloy', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860244/news/uquhnjg0defxet7vawkl.webp', 10),
('Dragon', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860245/news/xvjx03svzsctiotaftyb.webp', 10),
('Cyberpunk', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860393/news/ib5ijb2eqvlwlriqt5dt.webp', 9),
('Cyberpunk', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860394/news/muic3sun26nyhyvkyinw.webp', 9),
('Background', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860395/news/nlvkwmvuevwpsbgqmclk.webp', 9),
('Warrior 1', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860511/news/veijqx6hkmrjeiaep38i.webp', 8),
('Warrior 2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860512/news/ifd5hha9slht66wjq1yo.webp', 8),
('Warrior 3', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860512/news/osmixxxzacglli8iikhb.webp', 8);
