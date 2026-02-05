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
  img VARCHAR(45) NOT NULL,
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
('Título Noticia 1', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-01-01', '2026-01-01'),
('Título Noticia 2', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-02-02', '2026-02-02'),
('Título Noticia 3', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-03-03', '2026-03-03'),
('Título Noticia 4', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-04-04', '2026-04-04'),
('Título Noticia 5', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-05-05', '2026-05-05'),
('Título Noticia 6', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
 '2026-06-06', '2026-06-06');

INSERT INTO wm_news_gallery (alt, img, news_id)
VALUES 
('news-01', 'news-01.jpg', 1),
('news-02', 'news-02.jpg', 1),
('news-03', 'news-03.jpg', 1),
('news-02', 'news-02.jpg', 2),
('news-03', 'news-03.jpg', 2),
('news-01', 'news-01.jpg', 2),
('news-03', 'news-03.jpg', 3),
('news-01', 'news-01.jpg', 3),
('news-02', 'news-02.jpg', 3),
('news-01', 'news-01.jpg', 4),
('news-03', 'news-03.jpg', 4),
('news-02', 'news-02.jpg', 4),
('news-02', 'news-02.jpg', 5),
('news-01', 'news-01.jpg', 5),
('news-03', 'news-03.jpg', 5),
('news-03', 'news-03.jpg', 6),
('news-02', 'news-02.jpg', 6),
('news-01', 'news-01.jpg', 6);
