
TRUNCATE TABLE
  wm_copies,
  wm_edition_format,
  wm_book_author,
  wm_book_subject,
  wm_books,
  wm_subjects,
  wm_editions,
  wm_formats,
  wm_authors,
  wm_editorials,
  wm_genres,
  wm_news,
  wm_news_gallery,
  wm_user_role,
  wm_user_status,
  wm_loan_status,
  wm_reservation_status,
  wm_regions,
  wm_provinces,
  wm_communes
RESTART IDENTITY CASCADE;

SELECT
  (SELECT COUNT(*) FROM wm_news) AS count_news,
  (SELECT COUNT(*) FROM wm_news_gallery) AS count_news_gallery,
  (SELECT COUNT(*) FROM wm_books) AS count_books,
  (SELECT COUNT(*) FROM wm_book_author) AS count_books_author,
  (SELECT COUNT(*) FROM wm_book_subject) AS count_book_subject,
  (SELECT COUNT(*) FROM wm_authors) AS count_authors,
  (SELECT COUNT(*) FROM wm_subjects) AS count_subjects,
  (SELECT COUNT(*) FROM wm_genres) AS count_genres,
  (SELECT COUNT(*) FROM wm_editions) AS count_editions,
  (SELECT COUNT(*) FROM wm_edition_format) AS count_edition_format,
  (SELECT COUNT(*) FROM wm_formats) AS count_formats,
  (SELECT COUNT(*) FROM wm_copies) AS count_copies,
  (SELECT COUNT(*) FROM wm_editorials) AS count_editorials;

BEGIN;

-- === ESTADOS DE COPIA (necesarios para las copias) ===
INSERT INTO wm_copy_status (name) VALUES
('Disponible'),
('En reparación'),
('Extraviado'),
('Dado de baja')
ON CONFLICT (name) DO NOTHING;

-- === ROLES, ESTADOS Y GEOGRAFÍA CHILENA (catálogo desde DB.xlsx) ===
INSERT INTO wm_user_role (name) VALUES
('Super Admin'),
('Admin'),
('Lector');

INSERT INTO wm_user_status (name) VALUES
('Activo/a'),
('Deudor/a'),
('Bloqueado/a');

INSERT INTO wm_loan_status (name) VALUES
('En Préstamo'),
('Devuelto'),
('Vencido')
ON CONFLICT (name) DO NOTHING;

INSERT INTO wm_reservation_status (name) VALUES
('Pendiente de retiro'),
('Completada'),
('Cancelada'),
('Vencida')
ON CONFLICT (name) DO NOTHING;

-- === POLÍTICAS DE PRÉSTAMO (desde DB.xlsx) ===
-- id_policy es GENERATED ALWAYS (no acepta valor explícito) y name NO es
-- UNIQUE; por eso se usa WHERE NOT EXISTS para idempotencia.
INSERT INTO wm_loan_policies (name, max_books, max_days, reservation_days)
SELECT 'Lectores', 3, 14, 3
WHERE NOT EXISTS (SELECT 1 FROM wm_loan_policies WHERE name = 'Lectores');

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

-- === FORMATOS ===
INSERT INTO wm_formats (name) VALUES
('Sin Clasificar'),
('Accesible (tipografía grande)'),
('Adaptación infantil'),
('Adaptación juvenil'),
('Adaptación moderna'),
('Edición Ilustrada'),
('Idioma inglés'),
('Libro álbum'),
('Traducción / Bilingüe'),
('Versión Comentada'),
('Versión Original completa'),
('Versión Resumida');

-- === GÉNEROS ===
INSERT INTO wm_genres (name) VALUES
('Literatura infantil'),
('Novela'),
('Fantasía'),
('Terror'),
('Cuento'),
('Thriller'),
('Literatura clásica'),
('Literatura juvenil'),
('Ciencia ficción'),
('Manga');

-- === MATERIAS ===
INSERT INTO wm_subjects (name) VALUES
('Literatura infantil'),
('Literatura chilena'),
('Niños'),
('Vida cotidiana'),
('Novela latinoamericana'),
('Amazonía'),
('Soledad'),
('Fantasía épica'),
('Magia'),
('Reinos imaginarios'),
('Dragones'),
('Novela de terror'),
('Cementerios'),
('Horror cósmico'),
('Seres sobrenaturales'),
('Simbología religiosa'),
('Conspiraciones'),
('Epopeya griega'),
('Mitología griega'),
('Guerra de Troya'),
('Superhéroes'),
('Identidad secreta'),
('Thriller psicológico'),
('Asesinos seriales'),
('Ciencia ficción'),
('Vida extraterrestre'),
('Distopías'),
('Tierra Media'),
('Viajes fantásticos'),
('Criaturas míticas'),
('Manga'),
('Aventura'),
('Humor'),
('Cuentos');

-- === AUTORES ===
INSERT INTO wm_authors (name) VALUES
('Marcela Paz'),
('Luis Sepúlveda'),
('Morgan Rice'),
('George R. R. Martin'),
('Stephen King'),
('H. P. Lovecraft'),
('Dan Brown'),
('Homero'),
('Matt de la Peña'),
('Thomas Harris'),
('Arthur C. Clarke'),
('J. R. R. Tolkien'),
('Yoshihiro Togashi'),
('Manuel Rojas'),
('Julio Cortázar');

-- === EDITORIALES ===
INSERT INTO wm_editorials (name) VALUES
('Editorial Universitaria'),
('Tusquets Editores'),
('Autor-editor (ebook)'),
('Gigamesh'),
('Debolsillo'),
('Alianza Editorial'),
('Planeta'),
('La Otra H'),
('Montena'),
('Booket'),
('Minotauro'),
('Panini'),
('Zig-Zag'),
('Alfaguara');

-- === SEED DEMO: 16 LIBROS ENRIQUECIDOS ===
DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Papelucho';
  v_summary TEXT := 'Papelucho tiene un terrible secreto, tan terrible que no puede contárselo a nadie. Por eso decide escribirlo en un diario...
Asi comienza la exitosa serie de diarios de Papelucho, personaje que con su ingenio logra transformar la vida cotidiana en un escenario chispeante, donde las travesuras son las protagonistas';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Literatura infantil'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9789561111851', 1995, 125, (SELECT id_editorial FROM wm_editorials WHERE name = 'Editorial Universitaria'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1774721980/edition/g0laexbhrtzwkyzlhz03.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Marcela Paz'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Literatura infantil'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Literatura chilena'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Niños'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Vida cotidiana'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Un viejo que leía novelas de amor';
  v_summary TEXT := 'Antonio José Bolívar Proaño vive en El Idilio, un pueblo remoto en la región amazónica de los indios shuar (mal llamados jíbaros), y con ellos aprendió a conocer la Selva y sus leyes, a respetar a los animales y los indígenas que la pueblan, pero también a cazar el temible tigrillo como ningún blanco jamás pudo hacerlo. Un buen día decidió leer con pasión las novelas de amor -«del verdadero, del que hace sufrir»- que dos veces al año le lleva el dentista Rubicundo Loachamín para distraer las solitarias noches ecuatoriales de su incipiente vejez. En ellas intenta alejarse un poco de la fanfarrona estupidez de esos codiciosos forasteros que creen dominar la Selva porque van armados hasta los dientes pero que no saben cómo enfrentarse a una fiera enloquecida porque le han matado las crías. Descritas en un lenguaje cristalino, escueto y preciso, las aventuras y las emociones del viejo Bolívar Proaño difícilmente abandonarán nuestra memoria.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Novela'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788472236554', 1993, 144, (SELECT id_editorial FROM wm_editorials WHERE name = 'Tusquets Editores'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/aniuzgtkfw2yknukydix.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Luis Sepúlveda'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Novela latinoamericana'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Amazonía'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Soledad'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El despertar de los dragones';
  v_summary TEXT := 'Si pensaste que ya no había razón para vivir después de terminar de leer la serie El anillo del hechicero, te equivocaste. En EL DESPERTAR DE LOS DRAGONES Morgan Rice nos presenta lo que promete ser otra brillante serie, sumergiéndonos en una fantasía de troles y dragones, de valor, honor, intrepidez, magia y fe en tu destino. Morgan ha logrado producir otro fuerte conjunto de personajes que nos hacen animarlos en cada página.…Recomendado para la biblioteca permanente de todos los lectores que aman la fantasía bien escrita';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9781632912824', 2015, 0, (SELECT id_editorial FROM wm_editorials WHERE name = 'Autor-editor (ebook)'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/g8aug3ov198rkumybpcf.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Morgan Rice'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Fantasía épica'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Magia'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Reinos imaginarios'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Dragones'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El mundo de Hielo y Fuego';
  v_summary TEXT := 'Si el pasado es prólogo, la obra maestra de George R.R. Martin -Juego de Tronos, la saga fantástica más innovadora y trepidante de nuestra época- se merecía una introducción excepcional. Por fin, con El mundo de hielo y fuego, la tenemos. Con más de 170 imágenes originales a todo color. Este libro magníficamente ilustrado es una historia completa de los Siete Reinos, animada por vibrantes descripciones de las épicas batallas, enconadas rivalidades y audaces rebeliones que desembocan en la trama de Canción de hielo y fuego y de la serie de HBO Game of thrones. En una colaboración preparada desde hace años, George R.R. Martin ha formado equipo con Elio M. García Jr. y Linda Antonsson, fundadores del prestigioso fan site Westeros.org, quizá las únicas personas que conocen casi tan bien el mundo de la saga como su visionario creador. Se reúne aquí todo el saber acumulado, todas las teorías eruditas y todo el acervo de relatos populares de maestres, septones, magos y bardos, en una crónica que empieza por la Era del Amanecer y sigue por la Edad de los Héroes, la aparición de los primeros hombres, la llegada de Aegon el Conquistador, el establecimiento del Trono de Hierro por Aegon, la Rebelión de Robert y la caída del Rey Loco, Aerys II Targaryen, causantes de las peripecias "actuales" de los Stark, los Lannister, los Baratheon y los Targaryen. Complemento definitivo del universo que tan deslumbrantemente ha ideado George R.R. Martin, El mundo de hielo y fuego es sin duda la demostración de que es más poderosa la pluma que una tormenta de espadas.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788416035847', 2017, 336, (SELECT id_editorial FROM wm_editorials WHERE name = 'Gigamesh'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/pt9kf9rqzva50pjsbrcj.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'George R. R. Martin'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Fantasía épica'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Reinos imaginarios'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Cementerio de animales';
  v_summary TEXT := 'Cementerio de animales Church estaba allí otra vez, como Louis Creed temía y deseaba. Porque su hijita Ellie le había encomendado que cuidara del gato, y Church había muerto atropellado. Louis lo había comprobado: el gato estaba muerto, incluso lo había enterrado más allá del cementerio de animales. Sin embargo, Church había regresado, y sus ojos eran más crueles y perversos que antes. Pero volvía a estar allí y Ellie no lo lamentaría. Louis Creed sí lo lamentaría. Porque más allá del cementerio de animales, más allá de la valla de troncos que nadie se atrevía a trasponer, más allá de los cuarenta y cinco escalones, el maligno poder del antiguo cementerio indio le reclamaba con macabra avidez...';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Terror'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788497930994', 2004, 488, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195682/edition/gaz9ueno8r0ja9nshprf.jpg')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Stephen King'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Novela de terror'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Cementerios'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El llamado de Cthulhu';
  v_summary TEXT := 'Lovecraft explora en este relato, el terror a lo desconocido y el miedo por la existencia de creaturas míticas escondidas de la sociedad moderna. El llamado de Cthulhu es un relato en primera persona que provoca en el lector desconcierto e incertidumbre sobre la realidad en la que vive. ¿Pueden existir creaturas de las que sólo hay registro en los mitos? ¿Hasta dónde alcanza el conocimiento de nuestra realidad? De la mano con la ciencia y los descubrimientos de su tiempo Lovecraft crea un universo literario, donde cuestiona, los límites del conocimiento humano.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Cuento'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788420658537', 2004, 208, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alianza Editorial'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773182339/edition/qan097holp6dqnow2z0g.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'H. P. Lovecraft'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Horror cósmico'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Seres sobrenaturales'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El Código Da Vinci';
  v_summary TEXT := '¿Qué misterio se oculta tras la sonrisa de Mona Lisa? Durante siglos, la Iglesia ha conseguido mantener oculta la verdad… hasta ahora.

Antes de morir asesinado, Jacques Saunière, el último Gran Maestre de una sociedad secreta que se remonta a la fundación de los templarios, transmite a su nieta Sofía una misteriosa clave. Saunière y sus predecesores, entre los que se encontraban hombres como Isaac Newton o Leonardo da Vinci, han conservado durante siglos un conocimiento que puede cambiar completamente la historia de la humanidad.

Ahora Sofía, con la ayuda del experto en simbología Robert Langdon, comienza la búsqueda de ese secreto, en una trepidante carrera que los lleva de una clave a otra, descifrando mensajes ocultos en los más famosos cuadros del genial pintor y en las paredes de antiguas catedrales. Un rompecabezas que deberán resolver pronto, ya que no están solos en el juego: una poderosa e influyente organización católica está dispuesta a emplear todos los medios para evitar que el secreto salga a la luz.

Un apasionante juego de claves escondidas, sorprendentes revelaciones, acertijos ingeniosos, verdades, mentiras, realidades históricas, mitos, símbolos, ritos, misterios y suposiciones en una trama llena de giros inesperados, narrada con un ritmo imparable que conduce al lector hasta el secreto más celosamente guardado del inicio de nuestra era.

Intriga y amenaza se mezclan en una de las mejores novelas de suspense que he leído jamás. Un sorprendente relato donde los enigmas se suceden a los secretos y estos a las adivinanzas.
Clive Cussler.

Un inteligente thriller lleno de enigmas y códigos que, sin duda, puede recomendarse con rotundo entusiasmo.
The New York Times.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Thriller'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788408176022', 2017, 624, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195606/edition/mgetonnzlujkwplxghni.jpg')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Dan Brown'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Simbología religiosa'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Conspiraciones'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'La Ilíada y la Odisea';
  v_summary TEXT := 'La Ilíada y la Odisea, obras cumbre de la literatura, son dos de los textos fundacionales de la cultura occidental. He aquí la versión manga de estos poemas épicos queEncuadernación: Rústica con solapas narran las aventuras de los héroes griegos: la lucha de Aquiles en la guerra de Troya y el viaje posterior de regreso a Ítaca emprendido por Odiseo. Homero (siglo VIII a.C.) es el cantor épico de la antigua Grecia a quien se atribuyen la Ilíada y la Odisea. Sobre su figura, rodeada de misterio, se han vertido ríos de tinta. Desde la época helenística se ha debatido no solo si fue autor o compilador, sino también su existencia histórica.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Literatura clásica'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788416540846', 2017, 200, (SELECT id_editorial FROM wm_editorials WHERE name = 'La Otra H'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195104/edition/sy07b8kgsfx6dx23swoz.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Homero'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Epopeya griega'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Mitología griega'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Guerra de Troya'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Superman Dawnbreaker';
  v_summary TEXT := 'Su poder va más allá de la imaginación.
Clark Kent siempre ha sido más rápido, más fuerte y mejor que la gente que lo rodea. Pero no fue educado para demostrarlo, y llamar la atención podría ser peligroso. Sin embargo, sus poderes son cada vez más fuertes y pronto se vuelve difícil mantenerlos en secreto.
Pero todo poder tiene un precio.
Cuando Clark conoce a Gloria Álvarez descubre que un oscuro secreto se esconde en Smallville. Parece que él no es el único que oculta algo. ¿Qué peligros se ciernen sobre esa pequeña ciudad? Junto con su mejor amiga, Lana Lang, busca resolver el misterio, pero para conseguirlo tendrá que pagar un alto precio: afrontar la verdad sobre su pasado.
Antes de salvar el mundo,
debe salvar Smallville.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Literatura juvenil'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788490439210', 2019, 336, (SELECT id_editorial FROM wm_editorials WHERE name = 'Montena'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195135/edition/bcb10klmstviynx6iygi.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Matt de la Peña'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Superhéroes'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Identidad secreta'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El silencio de los corderos';
  v_summary TEXT := 'En este potente thriller psicológico, Clarice, cautivada por Hannibal, se enfrenta con su ayuda a un despiadado asesino. A Clarice Starling, joven y ambiciosa estudiante de la academia del FBI, le encomiendan que entreviste a Hannibal Lecter, brillante psiquiatra y despiadado asesino, para conseguir su colaboración en la resolución de un caso de asesinatos en serie. El asombroso conocimiento de Lecter del comportamiento humano y su poderosa personalidad cautivarán de inmediato a Clarice, quien, incapaz de dominarse, establecerá con él una ambigua, inquietante y peligrosa relación. El silencio de los corderos fue llevada al cine en 1991, y ganó los Premios Oscar a las categorías mejor película, mejor dirección (Jonathan Demme), mejor actriz (Jodie Foster), mejor actor (Anthony Hopkins) y mejor guion adaptado. Los lectores opinan:«Excelente libro de un excelente autor.» «Hannibal Lecter, uno de los mejores antihéroes que ha dado la literatura. [...] Lectura más que obligada para los amantes de las buenas historias de suspense.»';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Thriller'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788497599368', 2003, 408, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195005/edition/s8fd6qiku0ugqotftsgm.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Thomas Harris'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Thriller psicológico'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Asesinos seriales'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El fin de la infancia';
  v_summary TEXT := 'Recuperamos este clásico escrito por una de las figuras más influyentes de la ciencia ficción del siglo XX.

Perteneciente a la tradicional y ya casi extinta «literatura de ideas», El fin de la infancia tiene como tema la futura evolución del hombre. Una raza extraña llega a la Tierra y trae consigo paz, prosperidad..., y la inesperada tragedia de la perfección. ¿Qué seguirá a la extinción de la raza humana?';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788445002698', 2015, 240, (SELECT id_editorial FROM wm_editorials WHERE name = 'Booket'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773194942/edition/dvikpgxy3xqiuqn1yecw.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Arthur C. Clarke'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Ciencia ficción'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Vida extraterrestre'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Distopías'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'El Hobbit';
  v_summary TEXT := 'Un gran clásico moderno y el preludio a las vastas y poderosas mitologías de El Señor de Los Anillos. Cuando alrededor de 1930, J.R.R. Tolkien comenzó a escribir El Hobbit, hacía ya diez años que trabajaba en el vasto panorama mitológico de El Libro de los Relatos, que más tarde se llamaría El Silmarillion. Así como esas crónicas tempranas narraban los mitos inmemoriales de la Primera y Segunda Edad, Tolkien pronto advirtió que El Hobbit iba ordenándose de algún modo como un relato de la Tercera Edad (Gandalf habla del Nigromante en las primeras páginas), aunque las inesperadas aventuras de un pacífico hombre del campo no parecieran tener mucha relación con las vastas y oscuras mitologías de la Tierra Media. El estilo directo y lineal, con alusiones (que el autor deploró más tarde) a un público infantil, no impide la poderosa irrupción unas pocas veces en términos de comedia de los grandes temas tolkienianos (el poder, la codicia, la guerra, la muerte) que reaparecerían en una dimensión a menudo obviamente épica en El Señor de los Anillos.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788445013588', 2023, 448, (SELECT id_editorial FROM wm_editorials WHERE name = 'Minotauro'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773194862/edition/quwflvgijtzwlvu48pju.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. R. R. Tolkien'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Fantasía épica'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Tierra Media'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Viajes fantásticos'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Criaturas míticas'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Hunter × Hunter';
  v_summary TEXT := 'La historia sigue a Gon Freecss, un joven que descubre que su padre, a quien creía muerto, es en realidad un legendario Hunter. Decidido a encontrarlo, Gon abandona su hogar y se presenta al peligroso Examen Hunter, donde conoce a nuevos aliados como Killua, Kurapika y Leorio. A lo largo de la aventura, los protagonistas enfrentan enemigos mortales, organizaciones criminales y desafíos que ponen a prueba su inteligencia, fuerza y determinación mientras exploran un mundo lleno de misterios, criaturas peligrosas y tesoros ocultos.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Manga'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788490242070', 2012, 192, (SELECT id_editorial FROM wm_editorials WHERE name = 'Panini'), 'Tomo 1', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1775055228/edition/jklsmj90ybgi91scubqu.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Adaptación juvenil'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Yoshihiro Togashi'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Manga'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Aventura'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Hijo de Ladrón';
  v_summary TEXT := 'En su novela Hijo de ladrón, presentada al concurso realizado en 1950 por la Sociedad de Escritores de Chile con el título Tiempo irremediable, Manuel Rojas introdujo el monólogo interior (o corriente de la conciencia), específicamente en el fragmento conocido como "La herida". Es la primera vez que en la narrativa chilena aparecen en forma consciente los procedimientos utilizados en la novela anglosajona, sobre todo por James Joyce y William Faulkner.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Novela'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9789561231047', 2013, 312, (SELECT id_editorial FROM wm_editorials WHERE name = 'Zig-Zag'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1776512269/edition/ojhg029an6eyyyodaifu.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Manuel Rojas'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Literatura chilena'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Novela latinoamericana'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'Sombras contra el Muro';
  v_summary TEXT := '"Sombras contra el muro" es la tercera novela que Rojas publicó de la tetralogía Tiempo irremediable, aunque desde la cronología vital de Aniceto Hevia, álter ego del autor y protagonista del ciclo narrativo, es la segunda. En Sombras contra el muro Rojas continúa las experiencias del Aniceto Hevia de Hijo de Ladrón para sumergirnos en el tiempo de su formación intelectual y política, enmarcada en el heteróclito medio anarquista del Santiago de los años veinte.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Novela'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9789561223684', 2017, 232, (SELECT id_editorial FROM wm_editorials WHERE name = 'Zig-Zag'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780003694/edition/ggz5dm9d0bzqdhtthrkf.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Sin Clasificar'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Manuel Rojas'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Literatura chilena'))
  ON CONFLICT DO NOTHING;
END $$;

DO $$
DECLARE
  v_book_id INTEGER;
  v_edit_id INTEGER;
  v_title TEXT := 'De cronopios y de famas';
  v_summary TEXT := 'historia de cronopios y de famas';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Cuento'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788420406794', 2010, 144, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alfaguara'), '1ra edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780177255/edition/zooigr4bprb1xrklu0ti.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Edición Ilustrada'));
  INSERT INTO wm_book_author (id_book, id_author)
  VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Julio Cortázar'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Humor'))
  ON CONFLICT DO NOTHING;
  INSERT INTO wm_book_subject (id_book, id_subject)
  VALUES (v_book_id, (SELECT id_subject FROM wm_subjects WHERE name = 'Cuentos'))
  ON CONFLICT DO NOTHING;
END $$;

-- === COPIAS (ejemplares conservados del xlsx) ===
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('PAZpapher-c2', 'PAZpapher-c2', 3, 1, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('PAZpapher', 'PAZpapher', 1, 1, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('PAZpapher-c1', 'PAZpapher-c1', 2, 1, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('SEPvie', 'SEPvie', 1, 2, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('SEPvie-c1', 'SEPvie-c1', 1, 2, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('SEPvie-c2', 'SEPvie-c2', 3, 2, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CLAdes', 'CLAdes', 1, 3, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CLAdes-c1', 'CLAdes-c1', 2, 3, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('MARmun', 'MARmun', 1, 4, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('BC005', '813.54 K54', 1, 5, 2)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('LOVlla', 'LOVlla', 1, 6, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('BC007', '813.54 B877', 1, 7, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('HOMili-c1', 'HOMili-c1', 2, 8, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('HOMili', 'HOMili', 1, 8, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('TOMsup-c3', 'TOMsup-c3', 4, 9, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('TOMsup-c1', 'TOMsup-c1', 2, 9, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('TOMsup', 'TOMsup', 1, 9, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('TOMsup-c2', 'TOMsup-c2', 3, 9, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('HARsil', 'HARsil', 1, 10, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('HARsil-c1', 'HARsil-c1', 2, 10, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CLAfin', 'CLAfin', 1, 11, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CLAfin-c1', 'CLAfin-c1', 2, 11, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('BC012', '823.912 T649', 1, 12, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('NEThxh-2026', 'NEThxh-2026', 1, 13, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('NEThxh-c1-2026', 'NEThxh-c1-2026', 1, 13, 2)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('NEThxh-c2-2026', 'NEThxh-c2-2026', 2, 13, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('SEPhij-c1-1960', 'SEPhij-c1-1960', 1, 14, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CORcro-c1', 'CORcro-c1', 2, 16, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CORcro', 'CORcro', 1, 16, 3)
ON CONFLICT (barcode) DO NOTHING;

-- === NOTICIAS ====
INSERT INTO wm_news (title, subtitle, body, created_at) VALUES
('Assassin’s Creed Valhalla, aventura vikinga', 'Explora Inglaterra como un vikingo', 'Assassin’s Creed Valhalla transporta a los jugadores al siglo IX, donde encarnan a Eivor, un guerrero vikingo. Con un mundo abierto lleno de exploración, combates y decisiones que afectan la historia, el juego busca combinar acción y narrativa histórica para los fanáticos de la saga.', '2026-02-08'),
('Cyberpunk 2077 sigue evolucionando', 'Night City recibe mejoras y nuevas historias', 'Cyberpunk 2077 ha logrado reinventarse tras su lanzamiento inicial, ofreciendo una experiencia más pulida y profunda en la icónica Night City. Con gráficos mejorados, misiones ampliadas y correcciones de bugs, los jugadores pueden sumergirse en un mundo futurista lleno de intrigas, tecnología avanzada y decisiones que afectan la historia. Cada actualización refuerza la narrativa y la libertad de exploración, manteniendo a Cyberpunk como un referente del RPG de mundo abierto en un entorno distópico y vibrante.', '2026-02-09'),
('Horizon continúa su aventura épica', 'La saga de Aloy evoluciona con nuevos horizontes', 'Horizon sigue cautivando a los jugadores con su mezcla de acción, exploración y narrativa envolvente. Con impresionantes paisajes y máquinas robóticas que desafían la imaginación, la saga ofrece una experiencia inmersiva única. Cada entrega expande la historia de Aloy, introduciendo nuevos territorios, enemigos y desafíos, manteniendo la esencia de aventura y descubrimiento que convirtió a Horizon en un referente de los RPG de mundo abierto modernos.', '2026-02-10'),
('Assassin’s Creed celebra su legado', 'La franquicia que cambió los videojuegos de acción y aventuras', 'La saga Assassin’s Creed, lanzada por primera vez en 2007, ha marcado un antes y un después en los videojuegos de mundo abierto. Con sus historias de conspiraciones históricas y exploración detallada de diferentes épocas, se ha ganado un lugar en el corazón de millones de jugadores alrededor del mundo. Cada entrega combina acción, sigilo y narrativa, manteniendo viva la esencia de la hermandad de asesinos a lo largo de los años.', '2026-02-12'),
('Oblivion regresa con Howard Legacy', 'Una nueva versión que revitaliza el clásico RPG', 'El remake Oblivion: HowardLegacy trae de vuelta la magia del clásico RPG de mundo abierto. Con gráficos actualizados y mejoras en la jugabilidad, los jugadores pueden explorar Tamriel con un nivel de detalle nunca antes visto. Esta versión conserva la narrativa rica y las misiones envolventes que hicieron famoso al título, ofreciendo tanto a fans antiguos como a nuevos jugadores la oportunidad de redescubrir la aventura épica en la tierra de los elfos, humanos y criaturas míticas.', '2026-02-12'),
('Hunter x Hunter sigue cautivando generaciones', 'Aventuras, amistad, desafíos sin fin y el poder del NEN', 'Hunter x Hunter es una saga que combina acción, estrategia y narrativa profunda, llevando a los espectadores a un mundo donde cazadores profesionales exploran territorios desconocidos y enfrentan desafíos únicos. Con personajes memorables, giros inesperados y una constante evolución de las habilidades de los protagonistas, la serie mantiene a los fans al borde del asiento. Cada arco amplía la historia, explorando la amistad, la ambición y los límites humanos, consolidando a Hunter x Hunter como un referente del anime moderno.', '2026-02-12'),
('Final Fantasy VII Remake: La épica historia regresa.', 'La primera parte del remake revive el clásico de 1997 con gráficos impresionantes y un enfoque narrativo renovado.', 'Square Enix ha vuelto a capturar la magia del icónico Final Fantasy VII con su remake, ofreciendo a los jugadores una experiencia completamente renovada mientras mantienen la esencia que hizo del original un clásico. La primera parte del remake se centra en la ciudad de Midgar, expandiendo la historia y los personajes con detalles y profundidad inéditos.

Los fans se maravillan con los gráficos modernos, el sistema de combate híbrido que mezcla acción y estrategia por turnos, y la banda sonora remasterizada que trae nostalgia y emoción. Aunque solo cubre la primera sección del juego original, los desarrolladores prometen que las siguientes partes continuarán con la misma fidelidad y expansión narrativa, manteniendo a los jugadores ansiosos por la próxima entrega.

Con un enfoque en la historia, los personajes y la jugabilidad, Final Fantasy VII Remake no solo rinde homenaje al título original, sino que también introduce el mundo a una nueva generación de jugadores, consolidándose como una de las experiencias RPG más destacadas de los últimos años.', '2026-02-16'),
('Elden Ring anuncia expansión sorpresa con nuevas regiones y jefes colosales.', 'FromSoftware revela contenido inédito para Elden Ring que ampliará el mapa, incorporará desafiantes mazmorras y profundizará en el misterio de las Tierras Intermedias con nuevas líneas argumentales.', 'Elden Ring vuelve a acaparar titulares tras el anuncio de una expansión sorpresa que promete ampliar significativamente la experiencia original. El estudio japonés FromSoftware confirmó que el nuevo contenido incluirá regiones completamente inéditas, enemigos nunca antes vistos y jefes de escala monumental que pondrán a prueba incluso a los jugadores más veteranos.

Según los primeros detalles, la expansión profundizará en el trasfondo de las Tierras Intermedias, explorando historias paralelas vinculadas al legado de los semidioses y a los fragmentos restantes del Círculo de Elden. También se introducirán nuevas armas, hechizos y mecánicas de combate que ampliarán las posibilidades de personalización.

Desde su lanzamiento en 2022, el título se consolidó como uno de los RPG de acción más influyentes de la década, gracias a su mundo abierto desafiante y su narrativa fragmentada. Con esta nueva expansión, el estudio busca revitalizar la comunidad y ofrecer retos aún más exigentes para quienes ya dominaron sus secretos.

La fecha de lanzamiento y el nombre oficial del contenido adicional se anunciarán próximamente, pero la expectativa entre los seguidores ya es enorme.', '2026-02-23'),
('Helldivers 2 recibe nueva ofensiva.', 'Un parche masivo añade enemigos, armas y un bioma extremo para veteranos', 'La guerra galáctica se intensifica. Helldivers 2 ha lanzado una actualización de gran magnitud que introduce una nueva ofensiva enemiga, poniendo a prueba incluso a los escuadrones más experimentados. El parche incluye una facción invasora con habilidades adaptativas que obligarán a los jugadores a replantear sus estrategias en el campo de batalla.

Entre las novedades destacan tres armas inéditas: un rifle de pulsos con daño en cadena, una escopeta incendiaria de corto alcance y un lanzador táctico capaz de desplegar cobertura portátil. Además, se han añadido estratagemas defensivas mejoradas, permitiendo solicitar drones de apoyo que patrullan zonas específicas durante tiempo limitado.

El nuevo bioma, un planeta volcánico azotado por tormentas electromagnéticas, añade peligros ambientales dinámicos. Erupciones repentinas, visibilidad reducida y fallos temporales en el equipamiento elevan la tensión en cada misión. La coordinación y la comunicación vuelven a ser claves para sobrevivir.

La comunidad ha reaccionado con entusiasmo ante el aumento de dificultad y la variedad de desafíos. Los desarrolladores han confirmado que este contenido forma parte de un plan de soporte continuo, con más eventos dinámicos y recompensas exclusivas programadas para las próximas semanas.

La Super Tierra necesita refuerzos. Y esta vez, la batalla será más brutal que nunca.', '2026-02-23'),
('La saga nórdica de God of War brilla', 'Kratos y Atreus redefinen la acción en PS4 y PS5', 'La saga nórdica de God of War y su secuela God of War Ragnarök marcó un antes y un después para la franquicia en PlayStation. Tras años centrada en la mitología griega, la serie reinventó su fórmula con una narrativa más madura, un combate renovado y un enfoque más íntimo en la relación entre Kratos y su hijo Atreus.

Lanzado originalmente en PS4, God of War (2018) sorprendió con su cámara en plano secuencia, su sistema de progresión RPG ligero y una exploración más abierta ambientada en los reinos de la mitología nórdica. El Leviatán, el hacha icónica de Kratos, se convirtió en símbolo de esta nueva etapa, combinando brutalidad y precisión táctica.

Por su parte, God of War Ragnarök elevó la apuesta en PS4 y especialmente en PS5, aprovechando la potencia de la nueva generación para ofrecer tiempos de carga casi inexistentes, combates más fluidos y una dirección artística aún más ambiciosa. La historia profundiza en el destino profetizado de Atreus y el inminente Ragnarök, enfrentando a los protagonistas a dioses como Thor y Odín.

La crítica y los jugadores coincidieron en destacar la evolución emocional de Kratos, ahora más humano y reflexivo, sin perder la intensidad que caracteriza a la saga. La etapa nórdica no solo revitalizó la franquicia, sino que consolidó a God of War como uno de los pilares narrativos y técnicos de PlayStation en la última década.', '2026-02-23'),
('Jedi Survivor expande la Fuerza.', 'Cal Kestis regresa con combate más profundo y nuevos mundos.', 'La galaxia vuelve a arder en Star Wars Jedi: Survivor, la esperada secuela de Star Wars Jedi: Fallen Order desarrollada por Respawn Entertainment. Ambientado cinco años después de los eventos anteriores, el título muestra a un Cal Kestis más experimentado, pero también más perseguido por el Imperio.

El nuevo capítulo amplía considerablemente los escenarios, ofreciendo planetas más abiertos, rutas opcionales y secretos que recompensan la exploración. El sistema de combate evoluciona con cinco posturas de sable de luz intercambiables, permitiendo adaptar el estilo de lucha a cada enfrentamiento, desde duelos rápidos hasta combates más pesados y estratégicos.

En PS5 y consolas de nueva generación, el juego destaca por su carga casi instantánea, mejoras gráficas y uso del control háptico para transmitir la intensidad de los choques de sable. Además, la narrativa profundiza en el conflicto interno de Cal, explorando temas como la resistencia, el sacrificio y el peso del legado Jedi.

Con una historia más oscura y ambiciosa, Jedi: Survivor consolida la saga como una de las adaptaciones más sólidas del universo Star Wars en videojuegos, combinando acción cinematográfica con exploración y desarrollo de personaje al más puro estilo Jedi.', '2026-02-23'),
('GTA V sigue dominando el mercado.', 'El clásico de Rockstar mantiene su éxito en nueva generación.', 'Más de una década después de su lanzamiento original, Grand Theft Auto V continúa siendo uno de los títulos más influyentes y vendidos de la industria. Desarrollado por Rockstar Games, el juego ha logrado mantenerse vigente gracias a constantes actualizaciones y su exitosa vertiente online.

En PS4 y PS5, GTA V ofrece mejoras visuales, mayor fluidez y tiempos de carga reducidos, especialmente en la versión optimizada para nueva generación. Los jugadores pueden elegir entre distintos modos gráficos que priorizan rendimiento o calidad visual, elevando la experiencia en la ciudad de Los Santos.

Por su parte, Grand Theft Auto Online sigue expandiéndose con nuevos golpes, vehículos, negocios y eventos semanales que mantienen activa a una comunidad masiva. Esta fórmula de contenido constante ha sido clave para que el juego continúe generando cifras récord año tras año.

Mientras la expectativa crece por el futuro de la franquicia, GTA V demuestra que su combinación de mundo abierto, narrativa criminal y libertad total sigue siendo una referencia dentro del género.', '2026-02-23'),
('Monster Hunter Rise sigue vivo', 'La comunidad de cazadores mantiene activo el juego de Capcom', 'A pesar de haber sido lanzado en 2021, Monster Hunter Rise continúa siendo uno de los títulos más jugados de la franquicia. En 2026, miles de jugadores siguen regresando al juego gracias a su expansión Sunbreak, las misiones cooperativas y la constante actividad de la comunidad en línea.

Muchos fanáticos destacan que el juego sigue siendo una excelente opción tanto para nuevos jugadores como para veteranos de la saga. Además, el éxito reciente de Monster Hunter Wilds ha provocado que más personas vuelvan a probar Rise mientras esperan futuras actualizaciones de la franquicia.
', '2026-05-27'),
('Último capítulo de Arcane', 'Rompe récords y desata teorías entre los fans', 'La serie animada Arcane, inspirada en el universo de League of Legends, volvió a convertirse en tendencia mundial tras el estreno de su más reciente episodio, el cual dejó a miles de espectadores debatiendo teorías en redes sociales durante toda la madrugada.
La producción de Riot Games y Fortiche recibió elogios por su calidad de animación, banda sonora y el desarrollo emocional de personajes como Jinx, Vi y Caitlyn. Muchos fans destacaron especialmente una escena final “impactante”, que ya está siendo considerada una de las más memorables de la serie.
En plataformas como X y Reddit, las discusiones se centraron en posibles alianzas inesperadas, el destino de Piltover y Zaun, y la aparición de referencias ocultas al lore original del videojuego.
Críticos especializados también señalaron que Arcane continúa elevando el estándar de las adaptaciones de videojuegos, demostrando que una narrativa sólida puede atraer incluso a personas que nunca jugaron League of Legends.
Mientras tanto, Riot Games evitó comentar sobre las teorías más populares, aunque adelantó que “lo peor todavía está por venir”.', '2026-05-28');

-- === GALERÍAS DE NOTICIAS ===
INSERT INTO wm_news_gallery(alt, url, news_id) VALUES
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
('Killua', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1770940395/news/qg93qwmsovk2nphxb6nc.webp', 6),
('Cloud Strife', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257298/news/pgxw8jpjgiselqsuw4di.webp', 7),
('Tifa Lockhart', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257299/news/fg9pfhzxk287wvkok6c6.webp', 7),
('Sephiroth', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771257300/news/pzkqszs9ysasdmysjayl.webp', 7),
('Elden Ring', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823372/news/nbsnfynpbawekafceblx.webp', 8),
('Elden Ring', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823372/news/driwxm2zqnpousc2rytc.webp', 8),
('Elden Ring', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771823373/news/re10mxytego7w8bm0yzy.webp', 8),
('Helldivers 2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885339/news/aa7ceeyz5v6bkbcqjowt.webp', 9),
('Helldivers 2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885341/news/i9co1om3cc7tcn09abrc.webp', 9),
('Helldivers 2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771885342/news/pxvfuhf6webhyidlgigm.webp', 9),
('Kratos', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771887680/news/i0zza4ye75cxpbmv8lad.webp', 10),
('Ragnarok', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771887682/news/odoxyx9zpwkmaa66m7nk.webp', 10),
('God Of War', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771951578/news/cijm92qqwa79xqqouwn9.webp', 10),
('Jedi Survivor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888048/news/kpjxbetb7rze9j0jyu9m.webp', 11),
('Jedi Survivor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888049/news/mgulzfkp4xvefmtysrn1.webp', 11),
('Cal Kestis', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888050/news/fuvvnesjs0jx8bdhw7zn.webp', 11),
('GTA 5', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888405/news/bmillgcolenf9kfwc7kv.webp', 12),
('GTA 5', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888406/news/bvzm5cwazjbyvdfriawq.webp', 12),
('GTA 5', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1771888407/news/lhjoz9ethysntixpm373.webp', 12),
('Monster Hunter Rise', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1779916409/news/s9jnplwprhzm5bzny5nr.webp', 13),
('Valstrax', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1779916410/news/rpiqekgucqv1yra1oxhy.webp', 13),
('MH Rise', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1779916411/news/rkupvxqgq33rlibdtkcp.webp', 13),
('Arcane', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780011277/news/jrzbqhzvunqpw5315osg.webp', 14),
('Arcane', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780011278/news/lbqquyucttwurgbvznby.webp', 14),
('Arcane', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780011279/news/x0ik8ouoiwbquszawtgp.webp', 14);

COMMIT;
