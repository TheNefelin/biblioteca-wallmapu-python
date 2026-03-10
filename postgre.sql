DROP TABLE wm_news_gallery;
DROP TABLE wm_news;

DROP TABLE wm_users;

DROP TABLE wm_user_role;
DROP TABLE wm_user_status;

DROP TABLE wm_communes;
DROP TABLE wm_provinces;
DROP TABLE wm_regions;

DROP TABLE wm_book_author
DROP TABLE wm_book_subject
DROP TABLE wm_books
DROP TABLE wm_subjects
DROP TABLE wm_authors
DROP TABLE wm_editorials


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
  commune VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  province_id INTEGER,
  CONSTRAINT communes_provinces_fk FOREIGN KEY (province_id) REFERENCES wm_provinces(id_province)
);

CREATE TABLE IF NOT EXISTS wm_user_status (
  id_user_status INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  status VARCHAR(45),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE IF NOT EXISTS wm_user_role (
  id_user_role INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  role VARCHAR(45) NOT NULL,
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
  news_id INTEGER,
  CONSTRAINT news_gallery_fk FOREIGN KEY (news_id) REFERENCES wm_news(id_news)
);

CREATE TABLE IF NOT EXISTS wm_authors (
  id_author INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_editorials (
  id_editorial INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_subjects (
  id_subject INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_genres (
  id_genre INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wm_copy_status (
  id_status SMALLINT PRIMARY KEY,
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
  isbn VARCHAR(20) UNIQUE NOT NULL,
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

CREATE TABLE IF NOT EXISTS wm_copies (
  id_copy INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  barcode VARCHAR(100) UNIQUE NOT NULL,
  signature_topography VARCHAR(100) NOT NULL,
  copy_number VARCHAR(20) NOT NULL,
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

CREATE TABLE IF NOT EXISTS wm_loans (
  id_loan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
  due_date DATE NOT NULL,
  return_date DATE,
  status VARCHAR(30) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  copy_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,

  CONSTRAINT loans_copies_fk FOREIGN KEY (copy_id) REFERENCES wm_book_copies(id_copy),
  CONSTRAINT loans_users_fk FOREIGN KEY (user_id) REFERENCES wm_users(id_user)
);


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


INSERT INTO wm_communes (commune, province_id) VALUES
('Arica', 1),
('Camarones', 2),
('Putre', 2),
('General Lagos', 2),
('Iquique', 3),
('Alto Hospicio', 3),
('Pozo Almonte', 4),
('Camiña', 4),
('Colchane', 4),
('Huara', 4),
('Pica', 4),
('Antofagasta', 5),
('Mejillones', 5),
('Sierra Gorda', 5),
('Taltal', 5),
('Calama', 6),
('Ollagüe', 6),
('San Pedro de Atacama', 6),
('Tocopilla', 7),
('María Elena', 7),
('Chañaral', 8),
('Diego de Almagro', 8),
('Copiapó', 9),
('Caldera', 9),
('Tierra Amarilla', 9),
('Vallenar', 10),
('Alto del Carmen', 10),
('Freirina', 10),
('Huasco', 10),
('La Serena', 11),
('Coquimbo', 11),
('Andacollo', 11),
('Vicuña', 11),
('Illapel', 12),
('Canela', 12),
('Los Vilos', 13),
('Salamanca', 13),
('Valparaíso', 14),
('Viña del Mar', 14),
('Isla de Pascua', 15),
('Los Andes', 16),
('San Esteban', 16),
('Petorca', 17),
('La Ligua', 17),
('San Antonio', 18),
('Cartagena', 18),
('San Felipe', 19),
('Putaendo', 19),
('Quillota', 20),
('La Calera', 20),
('Villa Alemana', 21),
('Limache', 21),
('Santiago', 22),
('Providencia', 22),
('Ñuñoa', 22),
('Puente Alto', 23),
('Pirque', 23),
('Colina', 24),
('Lampa', 24),
('San Bernardo', 25),
('Buin', 25),
('Melipilla', 26),
('Alhué', 26),
('Talagante', 27),
('Peñaflor', 27),
('Rancagua', 28),
('Machalí', 28),
('San Fernando', 30),
('Santa Cruz', 30),
('Pichilemu', 29),
('La Estrella', 29),
('Talca', 31),
('Maule', 31),
('Curicó', 32),
('Hualañé', 32),
('Linares', 33),
('San Javier', 33),
('Cauquenes', 34),
('Chanco', 34),
('Chillán', 35),
('Chillán Viejo', 35),
('Quirihue', 36),
('Cobquecura', 36),
('Pinto', 37),
('Concepción', 38),
('Talcahuano', 38),
('Hualpén', 38),
('Los Ángeles', 39),
('Mulchén', 39),
('Lebu', 40),
('Cañete', 40),
('Arauco', 40),
('Temuco', 41),
('Villarrica', 41),
('Loncoche', 41),
('Angol', 42),
('Renaico', 42),
('Collipulli', 42),
('Valdivia', 43),
('Corral', 43),
('La Unión', 44),
('Río Bueno', 44),
('Puerto Montt', 45),
('Puerto Varas', 45),
('Castro', 46),
('Ancud', 46),
('Osorno', 47),
('Purranque', 47),
('Chaitén', 48),
('Futaleufú', 48),
('Coyhaique', 49),
('Lago Verde', 49),
('Aysén', 50),
('Cisnes', 50),
('Chile Chico', 51),
('Río Ibáñez', 51),
('Tortel', 52),
('Punta Arenas', 53),
('Puerto Natales', 54),
('Porvenir', 55),
('Cabo de Hornos', 55),
('Antártica', 56);


INSERT INTO wm_user_status (status)
VALUES 
('Activo/a'),
('Deudor/a'),
('Bloqueado/a');


INSERT INTO wm_user_role (role)
VALUES 
('Super Admin'),
('Admin'),
('Lector');


INSERT INTO wm_news (title, subtitle, body) VALUES
('Assassin’s Creed Valhalla, aventura vikinga',
 'Explora Inglaterra como un vikingo',
 'Assassin’s Creed Valhalla transporta a los jugadores al siglo IX, donde encarnan a Eivor, un guerrero vikingo. Con un mundo abierto lleno de exploración, combates y decisiones que afectan la historia, el juego busca combinar acción y narrativa histórica para los fanáticos de la saga.'),

('Cyberpunk 2077 sigue evolucionando',
 'Night City recibe mejoras y nuevas historias',
 'Cyberpunk 2077 ha logrado reinventarse tras su lanzamiento inicial, ofreciendo una experiencia más pulida y profunda en la icónica Night City. Con gráficos mejorados, misiones ampliadas y correcciones de bugs, los jugadores pueden sumergirse en un mundo futurista lleno de intrigas, tecnología avanzada y decisiones que afectan la historia. Cada actualización refuerza la narrativa y la libertad de exploración, manteniendo a Cyberpunk como un referente del RPG de mundo abierto en un entorno distópico y vibrante.'),

('Horizon continúa su aventura épica',
 'La saga de Aloy evoluciona con nuevos horizontes',
 'Horizon sigue cautivando a los jugadores con su mezcla de acción, exploración y narrativa envolvente. Con impresionantes paisajes y máquinas robóticas que desafían la imaginación, la saga ofrece una experiencia inmersiva única. Cada entrega expande la historia de Aloy, introduciendo nuevos territorios, enemigos y desafíos, manteniendo la esencia de aventura y descubrimiento que convirtió a Horizon en un referente de los RPG de mundo abierto modernos.'),

('Assassin’s Creed celebra su legado',
 'La franquicia que cambió los videojuegos de acción y aventuras',
 'La saga Assassin’s Creed, lanzada por primera vez en 2007, ha marcado un antes y un después en los videojuegos de mundo abierto. Con sus historias de conspiraciones históricas y exploración detallada de diferentes épocas, se ha ganado un lugar en el corazón de millones de jugadores alrededor del mundo. Cada entrega combina acción, sigilo y narrativa, manteniendo viva la esencia de la hermandad de asesinos a lo largo de los años.'),

('Oblivion regresa con Howard Legacy',
 'Una nueva versión que revitaliza el clásico RPG',
 'El remake Oblivion: HowardLegacy trae de vuelta la magia del clásico RPG de mundo abierto. Con gráficos actualizados y mejoras en la jugabilidad, los jugadores pueden explorar Tamriel con un nivel de detalle nunca antes visto. Esta versión conserva la narrativa rica y las misiones envolventes que hicieron famoso al título, ofreciendo tanto a fans antiguos como a nuevos jugadores la oportunidad de redescubrir la aventura épica en la tierra de los elfos, humanos y criaturas míticas.'),

('Hunter x Hunter sigue cautivando generaciones',
 'Aventuras, amistad, desafíos sin fin y el poder del NEN',
 'Hunter x Hunter es una saga que combina acción, estrategia y narrativa profunda, llevando a los espectadores a un mundo donde cazadores profesionales exploran territorios desconocidos y enfrentan desafíos únicos. Con personajes memorables, giros inesperados y una constante evolución de las habilidades de los protagonistas, la serie mantiene a los fans al borde del asiento. Cada arco amplía la historia, explorando la amistad, la ambición y los límites humanos, consolidando a Hunter x Hunter como un referente del anime moderno.'),

('Final Fantasy VII Remake: La épica historia regresa.',
 'La primera parte del remake revive el clásico de 1997 con gráficos impresionantes y un enfoque narrativo renovado.',
 'Square Enix ha vuelto a capturar la magia del icónico Final Fantasy VII con su remake, ofreciendo a los jugadores una experiencia completamente renovada mientras mantienen la esencia que hizo del original un clásico. La primera parte del remake se centra en la ciudad de Midgar, expandiendo la historia y los personajes con detalles y profundidad inéditos.

Los fans se maravillan con los gráficos modernos, el sistema de combate híbrido que mezcla acción y estrategia por turnos, y la banda sonora remasterizada que trae nostalgia y emoción. Aunque solo cubre la primera sección del juego original, los desarrolladores prometen que las siguientes partes continuarán con la misma fidelidad y expansión narrativa, manteniendo a los jugadores ansiosos por la próxima entrega.

Con un enfoque en la historia, los personajes y la jugabilidad, Final Fantasy VII Remake no solo rinde homenaje al título original, sino que también introduce el mundo a una nueva generación de jugadores, consolidándose como una de las experiencias RPG más destacadas de los últimos años.'),

('Elden Ring anuncia expansión sorpresa con nuevas regiones y jefes colosales.',
 'FromSoftware revela contenido inédito para Elden Ring que ampliará el mapa, incorporará desafiantes mazmorras y profundizará en el misterio de las Tierras Intermedias con nuevas líneas argumentales.',
 'Elden Ring vuelve a acaparar titulares tras el anuncio de una expansión sorpresa que promete ampliar significativamente la experiencia original. El estudio japonés FromSoftware confirmó que el nuevo contenido incluirá regiones completamente inéditas, enemigos nunca antes vistos y jefes de escala monumental que pondrán a prueba incluso a los jugadores más veteranos.

Según los primeros detalles, la expansión profundizará en el trasfondo de las Tierras Intermedias, explorando historias paralelas vinculadas al legado de los semidioses y a los fragmentos restantes del Círculo de Elden. También se introducirán nuevas armas, hechizos y mecánicas de combate que ampliarán las posibilidades de personalización.

Desde su lanzamiento en 2022, el título se consolidó como uno de los RPG de acción más influyentes de la década, gracias a su mundo abierto desafiante y su narrativa fragmentada. Con esta nueva expansión, el estudio busca revitalizar la comunidad y ofrecer retos aún más exigentes para quienes ya dominaron sus secretos.

La fecha de lanzamiento y el nombre oficial del contenido adicional se anunciarán próximamente, pero la expectativa entre los seguidores ya es enorme.'),

('Helldivers 2 recibe nueva ofensiva.',
 'Un parche masivo añade enemigos, armas y un bioma extremo para veteranos',
 'La guerra galáctica se intensifica. Helldivers 2 ha lanzado una actualización de gran magnitud que introduce una nueva ofensiva enemiga, poniendo a prueba incluso a los escuadrones más experimentados. El parche incluye una facción invasora con habilidades adaptativas que obligarán a los jugadores a replantear sus estrategias en el campo de batalla.

Entre las novedades destacan tres armas inéditas: un rifle de pulsos con daño en cadena, una escopeta incendiaria de corto alcance y un lanzador táctico capaz de desplegar cobertura portátil. Además, se han añadido estratagemas defensivas mejoradas, permitiendo solicitar drones de apoyo que patrullan zonas específicas durante tiempo limitado.

El nuevo bioma, un planeta volcánico azotado por tormentas electromagnéticas, añade peligros ambientales dinámicos. Erupciones repentinas, visibilidad reducida y fallos temporales en el equipamiento elevan la tensión en cada misión. La coordinación y la comunicación vuelven a ser claves para sobrevivir.

La comunidad ha reaccionado con entusiasmo ante el aumento de dificultad y la variedad de desafíos. Los desarrolladores han confirmado que este contenido forma parte de un plan de soporte continuo, con más eventos dinámicos y recompensas exclusivas programadas para las próximas semanas.

La Super Tierra necesita refuerzos. Y esta vez, la batalla será más brutal que nunca.'),

('La saga nórdica de God of War brilla',
 'Kratos y Atreus redefinen la acción en PS4 y PS5',
 'La saga nórdica de God of War y su secuela God of War Ragnarök marcó un antes y un después para la franquicia en PlayStation. Tras años centrada en la mitología griega, la serie reinventó su fórmula con una narrativa más madura, un combate renovado y un enfoque más íntimo en la relación entre Kratos y su hijo Atreus.

Lanzado originalmente en PS4, God of War (2018) sorprendió con su cámara en plano secuencia, su sistema de progresión RPG ligero y una exploración más abierta ambientada en los reinos de la mitología nórdica. El Leviatán, el hacha icónica de Kratos, se convirtió en símbolo de esta nueva etapa, combinando brutalidad y precisión táctica.

Por su parte, God of War Ragnarök elevó la apuesta en PS4 y especialmente en PS5, aprovechando la potencia de la nueva generación para ofrecer tiempos de carga casi inexistentes, combates más fluidos y una dirección artística aún más ambiciosa. La historia profundiza en el destino profetizado de Atreus y el inminente Ragnarök, enfrentando a los protagonistas a dioses como Thor y Odín.

La crítica y los jugadores coincidieron en destacar la evolución emocional de Kratos, ahora más humano y reflexivo, sin perder la intensidad que caracteriza a la saga. La etapa nórdica no solo revitalizó la franquicia, sino que consolidó a God of War como uno de los pilares narrativos y técnicos de PlayStation en la última década.'),

('Jedi Survivor expande la Fuerza.',
 'Cal Kestis regresa con combate más profundo y nuevos mundos.',
 'La galaxia vuelve a arder en Star Wars Jedi: Survivor, la esperada secuela de Star Wars Jedi: Fallen Order desarrollada por Respawn Entertainment. Ambientado cinco años después de los eventos anteriores, el título muestra a un Cal Kestis más experimentado, pero también más perseguido por el Imperio.

El nuevo capítulo amplía considerablemente los escenarios, ofreciendo planetas más abiertos, rutas opcionales y secretos que recompensan la exploración. El sistema de combate evoluciona con cinco posturas de sable de luz intercambiables, permitiendo adaptar el estilo de lucha a cada enfrentamiento, desde duelos rápidos hasta combates más pesados y estratégicos.

En PS5 y consolas de nueva generación, el juego destaca por su carga casi instantánea, mejoras gráficas y uso del control háptico para transmitir la intensidad de los choques de sable. Además, la narrativa profundiza en el conflicto interno de Cal, explorando temas como la resistencia, el sacrificio y el peso del legado Jedi.

Con una historia más oscura y ambiciosa, Jedi: Survivor consolida la saga como una de las adaptaciones más sólidas del universo Star Wars en videojuegos, combinando acción cinematográfica con exploración y desarrollo de personaje al más puro estilo Jedi.'),

('GTA V sigue dominando el mercado.',
 'El clásico de Rockstar mantiene su éxito en nueva generación.',
 'Más de una década después de su lanzamiento original, Grand Theft Auto V continúa siendo uno de los títulos más influyentes y vendidos de la industria. Desarrollado por Rockstar Games, el juego ha logrado mantenerse vigente gracias a constantes actualizaciones y su exitosa vertiente online.

En PS4 y PS5, GTA V ofrece mejoras visuales, mayor fluidez y tiempos de carga reducidos, especialmente en la versión optimizada para nueva generación. Los jugadores pueden elegir entre distintos modos gráficos que priorizan rendimiento o calidad visual, elevando la experiencia en la ciudad de Los Santos.

Por su parte, Grand Theft Auto Online sigue expandiéndose con nuevos golpes, vehículos, negocios y eventos semanales que mantienen activa a una comunidad masiva. Esta fórmula de contenido constante ha sido clave para que el juego continúe generando cifras récord año tras año.

Mientras la expectativa crece por el futuro de la franquicia, GTA V demuestra que su combinación de mundo abierto, narrativa criminal y libertad total sigue siendo una referencia dentro del género.');


INSERT INTO wm_news_gallery (alt, url, news_id) VALUES
('Eivor','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939914/news/uwe28f3sei5saumlfv7o.webp',1),
('Valhalla','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939915/news/u4ygl2bb6nql1y5xtsru.jpg',1),
('Eivor','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770941204/news/wuvh9nrza7ok9r1wclli.jpg',1),
('Valerie','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939716/news/jyhvpdp6qyfglg23dij0.webp',2),
('Vincent','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939718/news/t91p3kpx2cy1ypnkft0o.jpg',2),
('Cyberpunk 77','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939719/news/gcruoldoxvnvnoybmdlb.webp',2),
('Aloy','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770860243/news/ruatveggaye123paqwbv.webp',3),
('Aloy','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939388/news/f8bxmp98ctc5lfzr5yif.webp',3),
('Horizon','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939389/news/srveg87fsk5ybd8iiwz6.webp',3),
('Kassandra','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770935727/news/v9oxvx7lu7owst444k4h.jpg',4),
('Alexio','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939522/news/uozjmpr2yowenri4jfrs.webp',4),
('Odessy','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770939523/news/gujaxilkk854bws6vlon.jpg',4),
('Oblivion','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770936527/news/lendveswlwbuyeivubbj.webp',5),
('Hogwarts','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770936528/news/awlnzgejc6yhhmh6vxg5.webp',5),
('Oblivion','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940063/news/rgrqye7kwl8lhdad9rfk.jpg',5),
('Gen''ei Ryodan','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940393/news/yqoteucqnlwmdu3lt8dk.webp',6),
('Gon','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940394/news/mfr18khtqxia0kica1co.webp',6),
('Killua','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940395/news/qg93qwmsovk2nphxb6nc.webp',6),
('Cloud Strife','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257298/news/pgxw8jpjgiselqsuw4di.webp',7),
('Tifa Lockhart','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257299/news/fg9pfhzxk287wvkok6c6.webp',7),
('Sephiroth','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257300/news/pzkqszs9ysasdmysjayl.webp',7),
('Elden Ring','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823372/news/nbsnfynpbawekafceblx.webp',8),
('Elden Ring','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823372/news/driwxm2zqnpousc2rytc.webp',8),
('Elden Ring','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823373/news/re10mxytego7w8bm0yzy.webp',8),
('Helldivers 2','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885339/news/aa7ceeyz5v6bkbcqjowt.webp',9),
('Helldivers 2','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885341/news/i9co1om3cc7tcn09abrc.webp',9),
('Helldivers 2','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885342/news/pxvfuhf6webhyidlgigm.webp',9),
('Kratos','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771887680/news/gf83vsctlnzuupdsyrkt.webp',10),
('Ragnarok','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771887682/news/odoxyx9zpwkmaa66m7nk.webp',10),
('God Of War','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771951578/news/cijm92qqwa79xqqouwn9.webp',10),
('Jedi Survivor','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888048/news/kpjxbetb7rze9j0jyu9m.webp',11),
('Jedi Survivor','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888049/news/mgulzfkp4xvefmtysrn1.webp',11),
('Cal Kestis','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888050/news/fuvvnesjs0jx8bdhw7zn.webp',11),
('GTA 5','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888405/news/bmillgcolenf9kfwc7kv.webp',12),
('GTA 5','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888406/news/bvzm5cwazjbyvdfriawq.webp',12),
('GTA 5','https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888407/news/lhjoz9ethysntixpm373.webp',12);


INSERT INTO wm_editorials (editorial) VALUES 
('Academia Chilena de la Lengua'),
('Alfaguara'),
('Ediciones Desidia'),
('Ediciones Occidente'),
('Ediciones Prosa'),
('Ediciones SM'),
('Edisur'),
('Editorial Andrés Bello'),
('Editorial Atlantida'),
('Editorial Bruño'),
('Editorial Don Bosco'),
('Editorial Ercilla'),
('Editorial Everest'),
('Editorial Grijalbo'),
('Editorial Maeva ediciones'),
('Editorial Planeta'),
('Editorial Planeta Chile'),
('Editorial Ramón Sopena'),
('Editorial Universitaria'),
('Editorial Vincens Vives'),
('Editorial Zig-Zag'),
('Grupo Editorial Planeta'),
('Javier Vergara Editor'),
('LOM Edición'),
('La Nación'),
('Maeva Ediciones'),
('Maeva Ediciones/Editorial Oceáno'),
('Penguin Random House'),
('Plaza Janés'),
('Publicaciones Lo Castillo'),
('Publicaciones y Ediciones Salamanca');


INSERT INTO wm_authors (name) VALUES
('Marcela Paz'),
('Luis Sepúlveda'),
('Christopher Paolini'),
('George R. R. Martin'),
('Stephen King'),
('H. P. Lovecraft'),
('Dan Brown'),
('Homero'),
('Peter J. Tomasi'),
('Thomas Harris'),
('Arthur C. Clarke'),
('J. R. R. Tolkien');


INSERT INTO wm_editorials (name) VALUES
('Editorial Universitaria'),
('Tusquets Editores'),
('Alfaguara'),
('Plaza & Janés'),
('Doubleday'),
('Arkham House'),
('Planeta'),
('Penguin Random House'),
('DC Comics'),
('St. Martin''s Press'),
('Debolsillo'),
('Minotauro');


INSERT INTO wm_subjects (name) VALUES
('Literatura infantil'),
('Literatura chilena'),
('Niños'),
('Vida cotidiana'),
('Novela latinoamericana'),
('Amazonía'),
('Soledad'),
('Fantasía épica'),
('Dragones'),
('Magia'),
('Reinos imaginarios'),
('Novela de terror'),
('Cementerios'),
('Horror cósmico'),
('Seres sobrenaturales'),
('Thriller psicológico'),
('Asesinos seriales'),
('Simbología religiosa'),
('Conspiraciones'),
('Epopeya griega'),
('Mitología griega'),
('Guerra de Troya'),
('Ciencia ficción'),
('Vida extraterrestre'),
('Distopías'),
('Superhéroes'),
('Identidad secreta'),
('Tierra Media'),
('Viajes fantásticos'),
('Criaturas míticas');


INSERT INTO wm_genres (name) VALUES
('Novela'),
('Cuento'),
('Poesía'),
('Ensayo'),
('Teatro'),
('Ciencia ficción'),
('Fantasía'),
('Terror'),
('Misterio'),
('Thriller'),
('Romance'),
('Aventura'),
('Drama'),
('Literatura infantil'),
('Literatura juvenil'),
('Biografía'),
('Autobiografía'),
('Historia'),
('Filosofía'),
('Psicología'),
('Autoayuda'),
('Divulgación científica'),
('Crónica'),
('Humor'),
('Distopía'),
('Realismo mágico'),
('Novela histórica'),
('Novela negra'),
('Literatura clásica');

INSERT INTO wm_copy_status (id_status, name) VALUES
(1,'Disponible'),
(2,'Prestado'),
(3,'En reparación'),
(4,'Extraviado');


INSERT INTO wm_books (title, summary, genre_id) VALUES
('Papelucho',
 'Papelucho tiene un terrible secreto, tan terrible que no puede contárselo a nadie. Por eso decide escribirlo en un diario...
Asi comienza la exitosa serie de diarios de Papelucho, personaje que con su ingenio logra transformar la vida cotidiana en un escenario chispeante, donde las travesuras son las protagonistas',
 14),
('Un viejo que leía novelas de amor',
 'Antonio José Bolívar Proaño vive en El Idilio, un pueblo remoto en la región amazónica de los indios shuar (mal llamados jíbaros), y con ellos aprendió a conocer la Selva y sus leyes, a respetar a los animales y los indígenas que la pueblan, pero también a cazar el temible tigrillo como ningún blanco jamás pudo hacerlo. Un buen día decidió leer con pasión las novelas de amor -«del verdadero, del que hace sufrir»- que dos veces al año le lleva el dentista Rubicundo Loachamín para distraer las solitarias noches ecuatoriales de su incipiente vejez. En ellas intenta alejarse un poco de la fanfarrona estupidez de esos codiciosos forasteros que creen dominar la Selva porque van armados hasta los dientes pero que no saben cómo enfrentarse a una fiera enloquecida porque le han matado las crías. Descritas en un lenguaje cristalino, escueto y preciso, las aventuras y las emociones del viejo Bolívar Proaño difícilmente abandonarán nuestra memoria.',
 1),
('El despertar de los dragones',
 'Si pensaste que ya no había razón para vivir después de terminar de leer la serie El anillo del hechicero, te equivocaste. En EL DESPERTAR DE LOS DRAGONES Morgan Rice nos presenta lo que promete ser otra brillante serie, sumergiéndonos en una fantasía de troles y dragones, de valor, honor, intrepidez, magia y fe en tu destino. Morgan ha logrado producir otro fuerte conjunto de personajes que nos hacen animarlos en cada página.…Recomendado para la biblioteca permanente de todos los lectores que aman la fantasía bien escrita',
 7),
('El mundo de Hielo y Fuego',
 'Si el pasado es prólogo, la obra maestra de George R.R. Martin -Juego de Tronos, la saga fantástica más innovadora y trepidante de nuestra época- se merecía una introducción excepcional. Por fin, con El mundo de hielo y fuego, la tenemos. Con más de 170 imágenes originales a todo color. Este libro magníficamente ilustrado es una historia completa de los Siete Reinos, animada por vibrantes descripciones de las épicas batallas, enconadas rivalidades y audaces rebeliones que desembocan en la trama de Canción de hielo y fuego y de la serie de HBO Game of thrones. En una colaboración preparada desde hace años, George R.R. Martin ha formado equipo con Elio M. García Jr. y Linda Antonsson, fundadores del prestigioso fan site Westeros.org, quizá las únicas personas que conocen casi tan bien el mundo de la saga como su visionario creador. Se reúne aquí todo el saber acumulado, todas las teorías eruditas y todo el acervo de relatos populares de maestres, septones, magos y bardos, en una crónica que empieza por la Era del Amanecer y sigue por la Edad de los Héroes, la aparición de los primeros hombres, la llegada de Aegon el Conquistador, el establecimiento del Trono de Hierro por Aegon, la Rebelión de Robert y la caída del Rey Loco, Aerys II Targaryen, causantes de las peripecias "actuales" de los Stark, los Lannister, los Baratheon y los Targaryen. Complemento definitivo del universo que tan deslumbrantemente ha ideado George R.R. Martin, El mundo de hielo y fuego es sin duda la demostración de que es más poderosa la pluma que una tormenta de espadas.',
 18),
('Cementerio de animales',
 'Cementerio de animales Church estaba allí otra vez, como Louis Creed temía y deseaba. Porque su hijita Ellie le había encomendado que cuidara del gato, y Church había muerto atropellado. Louis lo había comprobado: el gato estaba muerto, incluso lo había enterrado más allá del cementerio de animales. Sin embargo, Church había regresado, y sus ojos eran más crueles y perversos que antes. Pero volvía a estar allí y Ellie no lo lamentaría. Louis Creed sí lo lamentaría. Porque más allá del cementerio de animales, más allá de la valla de troncos que nadie se atrevía a trasponer, más allá de los cuarenta y cinco escalones, el maligno poder del antiguo cementerio indio le reclamaba con macabra avidez...',
 8),
('El llamado de Cthulhu',
 'Lovecraft explora en este relato, el terror a lo desconocido y el miedo por la existencia de creaturas míticas escondidas de la sociedad moderna. El llamado de Cthulhu es un relato en primera persona que provoca en el lector desconcierto e incertidumbre sobre la realidad en la que vive. ¿Pueden existir creaturas de las que sólo hay registro en los mitos? ¿Hasta dónde alcanza el conocimiento de nuestra realidad? De la mano con la ciencia y los descubrimientos de su tiempo Lovecraft crea un universo literario, donde cuestiona, los límites del conocimiento humano.',
 2),
('El Código Da Vinci',
 '¿Qué misterio se oculta tras la sonrisa de Mona Lisa? Durante siglos, la Iglesia ha conseguido mantener oculta la verdad… hasta ahora.

Antes de morir asesinado, Jacques Saunière, el último Gran Maestre de una sociedad secreta que se remonta a la fundación de los templarios, transmite a su nieta Sofía una misteriosa clave. Saunière y sus predecesores, entre los que se encontraban hombres como Isaac Newton o Leonardo da Vinci, han conservado durante siglos un conocimiento que puede cambiar completamente la historia de la humanidad.

Ahora Sofía, con la ayuda del experto en simbología Robert Langdon, comienza la búsqueda de ese secreto, en una trepidante carrera que los lleva de una clave a otra, descifrando mensajes ocultos en los más famosos cuadros del genial pintor y en las paredes de antiguas catedrales. Un rompecabezas que deberán resolver pronto, ya que no están solos en el juego: una poderosa e influyente organización católica está dispuesta a emplear todos los medios para evitar que el secreto salga a la luz.

Un apasionante juego de claves escondidas, sorprendentes revelaciones, acertijos ingeniosos, verdades, mentiras, realidades históricas, mitos, símbolos, ritos, misterios y suposiciones en una trama llena de giros inesperados, narrada con un ritmo imparable que conduce al lector hasta el secreto más celosamente guardado del inicio de nuestra era.

Intriga y amenaza se mezclan en una de las mejores novelas de suspense que he leído jamás. Un sorprendente relato donde los enigmas se suceden a los secretos y estos a las adivinanzas.
Clive Cussler.

Un inteligente thriller lleno de enigmas y códigos que, sin duda, puede recomendarse con rotundo entusiasmo.
The New York Times.',
 10),
('La Ilíada y la Odisea',
 'La Ilíada y la Odisea, obras cumbre de la literatura, son dos de los textos fundacionales de la cultura occidental. He aquí la versión manga de estos poemas épicos queEncuadernación: Rústica con solapas narran las aventuras de los héroes griegos: la lucha de Aquiles en la guerra de Troya y el viaje posterior de regreso a Ítaca emprendido por Odiseo. Homero (siglo VIII a.C.) es el cantor épico de la antigua Grecia a quien se atribuyen la Ilíada y la Odisea. Sobre su figura, rodeada de misterio, se han vertido ríos de tinta. Desde la época helenística se ha debatido no solo si fue autor o compilador, sino también su existencia histórica.',
 29),
('Superman Dawnbreaker',
 'Su poder va más allá de la imaginación.
Clark Kent siempre ha sido más rápido, más fuerte y mejor que la gente que lo rodea. Pero no fue educado para demostrarlo, y llamar la atención podría ser peligroso. Sin embargo, sus poderes son cada vez más fuertes y pronto se vuelve difícil mantenerlos en secreto.
Pero todo poder tiene un precio.
Cuando Clark conoce a Gloria Álvarez descubre que un oscuro secreto se esconde en Smallville. Parece que él no es el único que oculta algo. ¿Qué peligros se ciernen sobre esa pequeña ciudad? Junto con su mejor amiga, Lana Lang, busca resolver el misterio, pero para conseguirlo tendrá que pagar un alto precio: afrontar la verdad sobre su pasado.
Antes de salvar el mundo,
debe salvar Smallville.',
 15),
('El silencio de los corderos',
 'En este potente thriller psicológico, Clarice, cautivada por Hannibal, se enfrenta con su ayuda a un despiadado asesino. A Clarice Starling, joven y ambiciosa estudiante de la academia del FBI, le encomiendan que entreviste a Hannibal Lecter, brillante psiquiatra y despiadado asesino, para conseguir su colaboración en la resolución de un caso de asesinatos en serie. El asombroso conocimiento de Lecter del comportamiento humano y su poderosa personalidad cautivarán de inmediato a Clarice, quien, incapaz de dominarse, establecerá con él una ambigua, inquietante y peligrosa relación. El silencio de los corderos fue llevada al cine en 1991, y ganó los Premios Oscar a las categorías mejor película, mejor dirección (Jonathan Demme), mejor actriz (Jodie Foster), mejor actor (Anthony Hopkins) y mejor guion adaptado. Los lectores opinan:«Excelente libro de un excelente autor.» «Hannibal Lecter, uno de los mejores antihéroes que ha dado la literatura. [...] Lectura más que obligada para los amantes de las buenas historias de suspense.»',
 10),
('El fin de la infancia',
 'Recuperamos este clásico escrito por una de las figuras más influyentes de la ciencia ficción del siglo XX.

Perteneciente a la tradicional y ya casi extinta «literatura de ideas», El fin de la infancia tiene como tema la futura evolución del hombre. Una raza extraña llega a la Tierra y trae consigo paz, prosperidad..., y la inesperada tragedia de la perfección. ¿Qué seguirá a la extinción de la raza humana?',
 6),
('El Hobbit',
 'Un gran clásico moderno y el preludio a las vastas y poderosas mitologías de El Señor de Los Anillos. Cuando alrededor de 1930, J.R.R. Tolkien comenzó a escribir El Hobbit, hacía ya diez años que trabajaba en el vasto panorama mitológico de El Libro de los Relatos, que más tarde se llamaría El Silmarillion. Así como esas crónicas tempranas narraban los mitos inmemoriales de la Primera y Segunda Edad, Tolkien pronto advirtió que El Hobbit iba ordenándose de algún modo como un relato de la Tercera Edad (Gandalf habla del Nigromante en las primeras páginas), aunque las inesperadas aventuras de un pacífico hombre del campo no parecieran tener mucha relación con las vastas y oscuras mitologías de la Tierra Media. El estilo directo y lineal, con alusiones (que el autor deploró más tarde) a un público infantil, no impide la poderosa irrupción unas pocas veces en términos de comedia de los grandes temas tolkienianos (el poder, la codicia, la guerra, la muerte) que reaparecerían en una dimensión a menudo obviamente épica en El Señor de los Anillos.',
 7);


INSERT INTO wm_editions
(edition, isbn, publication_year, pages, cover_image, book_id, editorial_id)
VALUES
('1ra edición','9789561111851',1947,200,'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/d0y1qsplzftnalveumcl.webp',1,1),
('1ra edición','9788483835302',1989,250,'images/test/02.jpg',2,2),
('1ra edición','9780375826680',2003,500,'images/test/03.jpg',3,3),
('1ra edición','9788416035342',1996,700,'images/test/04.jpg',4,4),
('1ra edición','9780385182443',1983,350,'images/test/05.jpg',5,5),
('1ra edición','9780486294380',1928,150,'images/test/06.jpg',6,6),
('1ra edición','9788408175728',2003,450,'images/test/07.jpg',7,7),
('1ra edición','9788433906489',-800,600,'images/test/08.jpg',8,8),
('1ra edición','9781401278919',2018,120,'images/test/09.jpg',9,9),
('1ra edición','9780312927226',1988,350,'images/test/10.jpg',10,10),
('1ra edición','9788445077009',1985,280,'images/test/11.webp',11,11),
('1ra edición','9786070797217',1937,310,'images/test/12.webp',12,12);


INSERT INTO wm_copies
(barcode, signature_topography, copy_number, edition_id, status_id)
VALUES
('BC001','863 P348','1',1,1),
('BC002','863 S479','1',2,1),
('BC003','813.6 P195','1',3,1),
('BC004','813.54 M379','1',4,1),
('BC005','813.54 K54','1',5,1),
('BC006','813.52 L897','1',6,1),
('BC007','813.54 B877','1',7,1),
('BC008','883 H767','1',8,1),
('BC009','741.5 T655','1',9,1),
('BC010','813.54 H316','1',10,1),
('BC011','823.914 C592','1',11,1),
('BC012','823.912 T649','1',12,1);


INSERT INTO wm_book_author (id_book, id_author) VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10),
(11,11),
(12,12);


INSERT INTO wm_book_subject (id_book, id_subject) VALUES
(1,1),(1,2),(1,3),(1,4),
(2,5),(2,6),(2,7),
(3,8),(3,9),(3,10),(3,11),
(4,8),(4,11),
(5,12),(5,13),(5,15),
(6,14),(6,15),
(7,16),(7,18),(7,19),
(8,20),(8,21),(8,22),
(9,26),(9,27),
(10,16),(10,17),
(11,23),(11,24),(11,25),
(12,8),(12,9),(12,28),(12,30);

