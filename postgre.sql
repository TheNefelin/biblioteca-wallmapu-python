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
('Assassin’s Creed Valhalla, aventura vikinga',
 'Explora Inglaterra como un vikingo',
 'Assassin’s Creed Valhalla transporta a los jugadores al siglo IX, donde encarnan a Eivor, un guerrero vikingo. Con un mundo abierto lleno de exploración, combates y decisiones que afectan la historia, el juego busca combinar acción y narrativa histórica para los fanáticos de la saga.',
 '2026-02-08 00:00:00',
 '2026-02-13 02:06:15.28171'),
('Cyberpunk 2077 sigue evolucionando',
 'Night City recibe mejoras y nuevas historias',
 'Cyberpunk 2077 ha logrado reinventarse tras su lanzamiento inicial, ofreciendo una experiencia más pulida y profunda en la icónica Night City. Con gráficos mejorados, misiones ampliadas y correcciones de bugs, los jugadores pueden sumergirse en un mundo futurista lleno de intrigas, tecnología avanzada y decisiones que afectan la historia. Cada actualización refuerza la narrativa y la libertad de exploración, manteniendo a Cyberpunk como un referente del RPG de mundo abierto en un entorno distópico y vibrante.',
 '2026-02-09 00:00:00',
 '2026-02-12 23:40:34.208908'),
('Horizon continúa su aventura épica',
 'La saga de Aloy evoluciona con nuevos horizontes',
 'Horizon sigue cautivando a los jugadores con su mezcla de acción, exploración y narrativa envolvente. Con impresionantes paisajes y máquinas robóticas que desafían la imaginación, la saga ofrece una experiencia inmersiva única. Cada entrega expande la historia de Aloy, introduciendo nuevos territorios, enemigos y desafíos, manteniendo la esencia de aventura y descubrimiento que convirtió a Horizon en un referente de los RPG de mundo abierto modernos.',
 '2026-02-10 00:00:00',
 '2026-02-12 22:49:55.064783'),
('Assassin’s Creed celebra su legado',
 'La franquicia que cambió los videojuegos de acción y aventuras',
 'La saga Assassin’s Creed, lanzada por primera vez en 2007, ha marcado un antes y un después en los videojuegos de mundo abierto. Con sus historias de conspiraciones históricas y exploración detallada de diferentes épocas, se ha ganado un lugar en el corazón de millones de jugadores alrededor del mundo. Cada entrega combina acción, sigilo y narrativa, manteniendo viva la esencia de la hermandad de asesinos a lo largo de los años.',
 '2026-02-12 17:24:59.223391',
 '2026-02-12 22:46:04.764426'),
('Oblivion regresa con HowardLegacy',
 'Una nueva versión que revitaliza el clásico RPG',
 'El remake Oblivion: HowardLegacy trae de vuelta la magia del clásico RPG de mundo abierto. Con gráficos actualizados y mejoras en la jugabilidad, los jugadores pueden explorar Tamriel con un nivel de detalle nunca antes visto. Esta versión conserva la narrativa rica y las misiones envolventes que hicieron famoso al título, ofreciendo tanto a fans antiguos como a nuevos jugadores la oportunidad de redescubrir la aventura épica en la tierra de los elfos, humanos y criaturas míticas.',
 '2026-02-12 21:25:00.774789',
 '2026-02-12 22:48:44.682428'),
('Hunter x Hunter sigue cautivando generaciones',
 'Aventuras, amistad, desafíos sin fin y el poder del NEN',
 'Hunter x Hunter es una saga que combina acción, estrategia y narrativa profunda, llevando a los espectadores a un mundo donde cazadores profesionales exploran territorios desconocidos y enfrentan desafíos únicos. Con personajes memorables, giros inesperados y una constante evolución de las habilidades de los protagonistas, la serie mantiene a los fans al borde del asiento. Cada arco amplía la historia, explorando la amistad, la ambición y los límites humanos, consolidando a Hunter x Hunter como un referente del anime moderno.',
 '2026-02-12 23:53:09.153767',
 '2026-02-12 23:54:01.869003');

INSERT INTO wm_news_gallery (alt, url, news_id)
VALUES
('Eivor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939914/news/uwe28f3sei5saumlfv7o.webp', 1),
('Valhalla', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939915/news/u4ygl2bb6nql1y5xtsru.jpg', 1),
('Eivor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770941204/news/wuvh9nrza7ok9r1wclli.jpg', 1),
('Valerie', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939716/news/jyhvpdp6qyfglg23dij0.webp', 2),
('Vincent', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939718/news/t91p3kpx2cy1ypnkft0o.jpg', 2),
('Cyberpunk 77', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939719/news/gcruoldoxvnvnoybmdlb.webp', 2),
('Aloy', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860243/news/ruatveggaye123paqwbv.webp', 3),
('Aloy', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939388/news/f8bxmp98ctc5lfzr5yif.webp', 3),
('Horizon', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939389/news/srveg87fsk5ybd8iiwz6.webp', 3),
('Kassandra', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770935727/news/v9oxvx7lu7owst444k4h.jpg', 4),
('Alexio', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939522/news/uozjmpr2yowenri4jfrs.webp', 4),
('Odessy', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939523/news/gujaxilkk854bws6vlon.jpg', 4),
('Oblivion', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770936527/news/lendveswlwbuyeivubbj.webp', 5),
('Hogwarts', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770936528/news/awlnzgejc6yhhmh6vxg5.webp', 5),
('Oblivion', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940063/news/rgrqye7kwl8lhdad9rfk.jpg', 5),
('Gen''ei Ryodan', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940393/news/yqoteucqnlwmdu3lt8dk.webp', 6),
('Gon', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940394/news/mfr18khtqxia0kica1co.webp', 6),
('Killua', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940395/news/qg93qwmsovk2nphxb6nc.webp', 6);

