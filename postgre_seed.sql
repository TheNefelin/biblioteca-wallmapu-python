
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
('Versión Resumida'),
('Cómic'),
('Tapa dura'),
('Tapa blanda'),
('Libro impreso con CD-ROM'),
('Rústica de bolsillo'),
('Rústica con solapas'),
('Tapa dura con sobrecubierta'),
('Libro electrónico');

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
('Manga'),
('Fantasía oscura'),
('Superhéroes'),
('Educación'),
  ('Espiritualidad'),
  ('Poesía'),
  ('Ensayo');

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
('Cuentos'),
('Cómic'),
('Sueños'),
('Mitología'),
('Horror'),
('DC Comics'),
('Batman'),
  ('Gotham City'),
  ('Flash'),
('Viajes en el tiempo'),
('Universos alternativos'),
('Álgebra'),
('Matemáticas'),
('Ejercicios'),
('Enseñanza media'),
('Francia del siglo XVIII'),
('Perfumería'),
('Obsesión'),
('Asesinato'),
('Identidad'),
('Metafísica cristiana'),
('Desarrollo personal'),
('Pensamiento positivo'),
('Espiritualidad'),
('Saint Germain'),
('Jesús de Nazaret'),
('Jerusalén'),
('Misterio'),
('Religión'),
('Hobbits'),
('Anillos de poder'),
('Viaje heroico'),
('Guerra'),
('Rohan'),
  ('Mordor'),
  ('Sauron'),
  ('Realismo mágico'),
  ('Saga familiar'),
  ('Destino'),
  ('América Latina'),
  ('Caballería andante'),
  ('Locura'),
  ('Idealismo'),
  ('Sátira'),
  ('Novela picaresca'),
  ('Honor'),
  ('Crimen'),
  ('Pueblo'),
  ('Honorabilidad'),
  ('Política'),
  ('Amor'),
  ('Chile'),
  ('Muerte'),
  ('Pueblo fantasma'),
  ('Voz'),
  ('Memoria'),
  ('Existencialismo'),
  ('Incomunicación'),
  ('Pintura'),
  ('Alienación'),
  ('Familia'),
  ('Absurdo'),
  ('Transformación'),
  ('Amistad'),
  ('Infancia'),
  ('Sabiduría'),
  ('Viaje'),
  ('Experimentalismo'),
  ('Jazz'),
  ('París'),
  ('Buenos Aires'),
  ('Juego narrativo'),
  ('Totalitarismo'),
  ('Vigilancia'),
  ('Control social'),
  ('Censura'),
  ('Libros'),
  ('Conformismo'),
  ('Rebeldía'),
  ('Sociedad'),
  ('Manipulación'),
  ('Felicidad artificial'),
  ('Tecnología'),
  ('Supervivencia'),
  ('Instinto'),
  ('Naturaleza humana'),
  ('Isla'),
  ('Civilización'),
  ('Escuela'),
  ('Brujería'),
  ('Espacio'),
  ('Ecología'),
  ('Imperio'),
  ('Especia'),
  ('Imperio galáctico'),
  ('Psicohistoria'),
  ('Conocimiento'),
  ('Poder'),
  ('Narnia'),
  ('Hadas'),
  ('Reinos'),
  ('Guerras'),
  ('Traición'),
  ('Futuros oscuros'),
  ('Televisión'),
  ('Rebelión'),
  ('Universos paralelos'),
  ('Daimonion'),
  ('Polo Norte'),
  ('Música'),
  ('Universidad'),
  ('Leyenda'),
  ('Realidad virtual'),
  ('Videojuegos'),
  ('Nostalgia'),
  ('Competencia'),
  ('Futuro distópico'),
  ('Hotel embrujado'),
  ('Alcoholismo'),
  ('Psicología'),
  ('Aislamiento'),
  ('Payaso siniestro'),
  ('Pueblo maldito'),
  ('Grupo de amigos'),
  ('Miedo ancestral'),
  ('Chocolate'),
  ('Fábrica'),
  ('Imaginación'),
  ('Genio precoz'),
  ('Lectura'),
  ('Poderes telequinéticos'),
  ('Justicia infantil'),
  ('Independencia'),
  ('Libertad'),
  ('Crítica social'),
  ('Moralidad'),
  ('Anarquismo'),
  ('Ninjas'),
  ('Superación'),
  ('Combate'),
  ('Piratas'),
  ('Tesoro'),
  ('Evolución'),
  ('Historia humana'),
  ('Cultura'),
  ('Antropología'),
  ('Pasión'),
  ('Erotismo'),
  ('Melancolía'),
  ('Naturaleza'),
  ('Estrategia'),
  ('Milicia'),
  ('Filosofía'),
  ('Liderazgo'),
  ('Conflicto');

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
('Julio Cortázar'),
('Neil Gaiman'),
('Sam Kieth'),
('Mike Dringenberg'),
('Frank Miller'),
('Klaus Janson'),
('Lynn Varley'),
('Geoff Johns'),
('Andy Kubert'),
('Sandra Hope'),
('Aurelio Baldor'),
('Patrick Süskind'),
('Conny Méndez'),
('J. J. Benítez'),
('Elio M. García Jr.'),
  ('Linda Antonsson'),
  ('Gabriel García Márquez'),
  ('Miguel de Cervantes Saavedra'),
  ('Isabel Allende'),
  ('Juan Rulfo'),
  ('Ernesto Sabato'),
  ('Franz Kafka'),
  ('Antoine de Saint-Exupéry'),
  ('George Orwell'),
  ('Ray Bradbury'),
  ('Aldous Huxley'),
  ('William Golding'),
  ('J. K. Rowling'),
  ('Frank Herbert'),
  ('Isaac Asimov'),
  ('C. S. Lewis'),
  ('Suzanne Collins'),
  ('Philip Pullman'),
  ('Patrick Rothfuss'),
  ('Ernest Cline'),
  ('Roald Dahl'),
  ('Astrid Lindgren'),
  ('Alan Moore'),
  ('Dave Gibbons'),
  ('David Lloyd'),
  ('Masashi Kishimoto'),
  ('Eiichiro Oda'),
  ('Yuval Noah Harari'),
  ('Pablo Neruda'),
  ('Sun Tzu');

-- === EDITORIALES ===
INSERT INTO wm_editorials (name) VALUES
('Editorial Universitaria'),
('Tusquets Editores'),
('Lukeman Literary Management'),
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
('Alfaguara'),
('ECC Ediciones'),
('Planeta DeAgostini Cómics'),
('OVNI Press'),
('Grupo Editorial Patria'),
  ('Giluz'),
  ('Austral'),
  ('RM Verlag'),
  ('Salamandra'),
  ('Penguin Clásicos'),
  ('Plaza & Janés'),
  ('Molino'),
  ('Roca Bolsillo'),
  ('Nova'),
  ('Punto de Lectura'),
  ('Blackie Books'),
  ('Debate'),
  ('Planeta Cómic');

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
  VALUES (v_book_id, '9789561111851', 1995, 111, (SELECT id_editorial FROM wm_editorials WHERE name = 'Editorial Universitaria'), 'Edición de 1995', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1774721980/edition/g0laexbhrtzwkyzlhz03.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788472236554', 1993, 144, (SELECT id_editorial FROM wm_editorials WHERE name = 'Tusquets Editores'), 'Colección Andanzas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/aniuzgtkfw2yknukydix.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica con solapas'));
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
  VALUES (v_book_id, '9781632912824', 2015, 281, (SELECT id_editorial FROM wm_editorials WHERE name = 'Lukeman Literary Management'), 'Reyes y hechiceros, libro 1', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/g8aug3ov198rkumybpcf.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Libro electrónico'));
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
  VALUES (v_book_id, '9788416035847', 2017, 336, (SELECT id_editorial FROM wm_editorials WHERE name = 'Gigamesh'), 'Segunda edición en rústica', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773089263/edition/pt9kf9rqzva50pjsbrcj.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788497930994', 2004, 483, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Best Seller', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195682/edition/gaz9ueno8r0ja9nshprf.jpg')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
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
  v_title TEXT := 'La llamada de Cthulhu y otros cuentos';
  v_summary TEXT := 'Lovecraft explora en este relato, el terror a lo desconocido y el miedo por la existencia de creaturas míticas escondidas de la sociedad moderna. La llamada de Cthulhu es un relato en primera persona que provoca en el lector desconcierto e incertidumbre sobre la realidad en la que vive. ¿Pueden existir creaturas de las que sólo hay registro en los mitos? ¿Hasta dónde alcanza el conocimiento de nuestra realidad? De la mano con la ciencia y los descubrimientos de su tiempo Lovecraft crea un universo literario, donde cuestiona, los límites del conocimiento humano.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Cuento'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788420658537', 2004, 208, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alianza Editorial'), 'El libro de bolsillo — Bibliotecas temáticas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773182339/edition/qan097holp6dqnow2z0g.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788408176022', 2017, 624, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta'), 'Planeta Internacional, edición 2017', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195606/edition/mgetonnzlujkwplxghni.jpg')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica con solapas'));
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
  VALUES (v_book_id, '9788416540846', 2017, 200, (SELECT id_editorial FROM wm_editorials WHERE name = 'La Otra H'), 'Manga, primera edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195104/edition/sy07b8kgsfx6dx23swoz.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788490439210', 2019, 336, (SELECT id_editorial FROM wm_editorials WHERE name = 'Montena'), 'DC Icons, primera edición en español', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195135/edition/bcb10klmstviynx6iygi.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788497599368', 2003, 408, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Best Seller, bolsillo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773195005/edition/s8fd6qiku0ugqotftsgm.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
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
  VALUES (v_book_id, '9788445002698', 2015, 240, (SELECT id_editorial FROM wm_editorials WHERE name = 'Booket'), 'Edición de bolsillo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773194942/edition/dvikpgxy3xqiuqn1yecw.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9788445013588', 2023, 448, (SELECT id_editorial FROM wm_editorials WHERE name = 'Minotauro'), 'Edición revisada', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773194862/edition/quwflvgijtzwlvu48pju.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9789561231047', 2013, 320, (SELECT id_editorial FROM wm_editorials WHERE name = 'Zig-Zag'), 'Colección Viento Joven', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1776512269/edition/ojhg029an6eyyyodaifu.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  VALUES (v_book_id, '9789561223684', 2017, 232, (SELECT id_editorial FROM wm_editorials WHERE name = 'Zig-Zag'), 'Colección Narrativa', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780003694/edition/ggz5dm9d0bzqdhtthrkf.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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
  v_summary TEXT := 'Colección de cuentos, instrucciones y viñetas en la que Julio Cortázar contrapone a los imaginativos cronopios con los ordenados famas y las ambiguas esperanzas.';
BEGIN
  INSERT INTO wm_books (title, summary, genre_id)
  VALUES (v_title, v_summary, (SELECT id_genre FROM wm_genres WHERE name = 'Cuento'))
  RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image)
  VALUES (v_book_id, '9788420406794', 2010, 176, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alfaguara'), 'Edición de 2010', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1780177255/edition/zooigr4bprb1xrklu0ti.webp')
  RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
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

-- === LIBROS DE lista.txt ===
DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Sandman: Preludios y nocturnos', 'Morfeo, señor de los sueños, escapa tras décadas de cautiverio y busca los tres objetos que concentran su poder.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía oscura')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788418326592', 2020, 240, (SELECT id_editorial FROM wm_editorials WHERE name = 'ECC Ediciones'), 'Biblioteca Sandman vol. 01, segunda edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996800/edition/lbtrgwihqaoaxgov9vmx.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) SELECT v_edit_id, id_format FROM wm_formats WHERE name IN ('Cómic', 'Tapa dura');
  INSERT INTO wm_book_author (id_book, id_author) SELECT v_book_id, id_author FROM wm_authors WHERE name IN ('Neil Gaiman', 'Sam Kieth', 'Mike Dringenberg');
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Cómic', 'Sueños', 'Mitología', 'Horror', 'DC Comics');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Batman: El regreso del caballero oscuro', 'Un Bruce Wayne envejecido vuelve del retiro para enfrentar la violencia de Gotham y un orden político que cuestiona su papel como Batman.', (SELECT id_genre FROM wm_genres WHERE name = 'Superhéroes')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788467433197', 2008, 192, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta DeAgostini Cómics'), 'Absolute, primera edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996474/edition/dva49z1qfnqvazmrk4mw.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) SELECT v_edit_id, id_format FROM wm_formats WHERE name IN ('Cómic', 'Tapa dura');
  INSERT INTO wm_book_author (id_book, id_author) SELECT v_book_id, id_author FROM wm_authors WHERE name IN ('Frank Miller', 'Klaus Janson', 'Lynn Varley');
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Batman', 'Gotham City', 'Superhéroes', 'Distopías', 'Cómic');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Flashpoint', 'Barry Allen despierta en una línea temporal alterada y debe restaurar la realidad original.', (SELECT id_genre FROM wm_genres WHERE name = 'Superhéroes')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9789878191676', 2023, 240, (SELECT id_editorial FROM wm_editorials WHERE name = 'OVNI Press'), 'Primera edición argentina', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996625/edition/nto4wkvxlpatid2ofgap.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) SELECT v_edit_id, id_format FROM wm_formats WHERE name IN ('Cómic', 'Tapa blanda');
  INSERT INTO wm_book_author (id_book, id_author) SELECT v_book_id, id_author FROM wm_authors WHERE name IN ('Geoff Johns', 'Andy Kubert', 'Sandra Hope');
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Flash', 'Viajes en el tiempo', 'Universos alternativos', 'Superhéroes', 'DC Comics');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Álgebra', 'Manual de álgebra elemental con teoría, ejemplos, ejercicios y problemas resueltos.', (SELECT id_genre FROM wm_genres WHERE name = 'Educación')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9789708170000', 2007, 576, (SELECT id_editorial FROM wm_editorials WHERE name = 'Grupo Editorial Patria'), 'Segunda edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998070/edition/jhe4f2hwtey3tqouosyd.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Libro impreso con CD-ROM'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Aurelio Baldor'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Álgebra', 'Matemáticas', 'Ejercicios', 'Enseñanza media');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El perfume: historia de un asesino', 'Jean-Baptiste Grenouille persigue la esencia perfecta hasta convertir su obsesión en una serie de asesinatos.', (SELECT id_genre FROM wm_genres WHERE name = 'Thriller')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788432251146', 2011, 320, (SELECT id_editorial FROM wm_editorials WHERE name = 'Booket'), 'Colección Bestseller', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996578/edition/dr4o0cagiu3vgk4ypss8.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Patrick Süskind'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Francia del siglo XVIII', 'Perfumería', 'Obsesión', 'Asesinato', 'Identidad');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Metafísica 4 en 1, volumen I', 'Reúne cuatro textos de divulgación metafísica orientados a presentar principios espirituales y prácticas de transformación personal.', (SELECT id_genre FROM wm_genres WHERE name = 'Espiritualidad')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9789806329478', 2021, 331, (SELECT id_editorial FROM wm_editorials WHERE name = 'Giluz'), 'Volumen I', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998194/edition/bj1riz7fxqpgr1ymbhfl.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Conny Méndez'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Metafísica cristiana', 'Desarrollo personal', 'Pensamiento positivo', 'Espiritualidad', 'Saint Germain');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Caballo de Troya 1: Jerusalén', 'Un proyecto secreto permite a un militar viajar a la Palestina del siglo I para observar los últimos días de Jesús de Nazaret.', (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9789875806993', 2014, 736, (SELECT id_editorial FROM wm_editorials WHERE name = 'Booket'), 'Edición especial 30 aniversario', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996537/edition/fzychwcxs3lafexgs1kt.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica con solapas'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. J. Benítez'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Viajes en el tiempo', 'Jesús de Nazaret', 'Jerusalén', 'Misterio', 'Religión');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El Señor de los Anillos: La Comunidad del Anillo', 'Frodo recibe el Anillo Único y parte de la Comarca para impedir que Sauron recupere su poder.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788445009598', 2022, 488, (SELECT id_editorial FROM wm_editorials WHERE name = 'Minotauro'), 'Nueva edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996757/edition/mmnfrv7rwg1ttz7jelas.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura con sobrecubierta'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. R. R. Tolkien'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Tierra Media', 'Hobbits', 'Anillos de poder', 'Viaje heroico', 'Magia');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El Señor de los Anillos: Las Dos Torres', 'Frodo y Sam siguen hacia Mordor mientras sus aliados enfrentan la guerra que amenaza la Tierra Media.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788445009604', 2022, 408, (SELECT id_editorial FROM wm_editorials WHERE name = 'Minotauro'), 'Nueva edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996721/edition/qhghwipp2qwvrdlkfuic.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura con sobrecubierta'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. R. R. Tolkien'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Tierra Media', 'Guerra', 'Rohan', 'Hobbits', 'Anillos de poder');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El Señor de los Anillos: El Retorno del Rey', 'Mientras los pueblos libres se enfrentan a Sauron, Frodo y Sam se internan en Mordor para destruir el Anillo Único.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788445009611', 2022, 520, (SELECT id_editorial FROM wm_editorials WHERE name = 'Minotauro'), 'Nueva edición', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996689/edition/aoaenddnn0dtfbbndgtr.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura con sobrecubierta'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. R. R. Tolkien'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Tierra Media', 'Mordor', 'Sauron', 'Guerra', 'Anillos de poder');
END $$;

-- === LOTE 3: 34 LIBROS AGREGADOS ===
DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Cien años de soledad', 'La historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo, donde los destinos individuales se entrelazan con la historia de Colombia en una narrativa cíclica de realismo mágico.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788497592208', 2003, 496, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998297/edition/ulevcmdy5pk5zr5957ld.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Gabriel García Márquez'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Realismo mágico', 'Saga familiar', 'Soledad', 'Destino', 'América Latina');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Don Quijote de la Mancha', 'Un hidalgo manchego enloquece de tanto leer libros de caballería y, convertido en Don Quijote, recorre los caminos acompañado de su escudero Sancho Panza en busca de aventuras y justicia.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura clásica')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788423355235', 2019, 1040, (SELECT id_editorial FROM wm_editorials WHERE name = 'Austral'), 'Puesto en castellano actual por Andrés Trapiello', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998382/edition/vg4ctywqgw0l0ihk5fle.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Miguel de Cervantes Saavedra'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Caballería andante', 'Locura', 'Idealismo', 'Sátira', 'Novela picaresca');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Crónica de una muerte anunciada', 'Un cronista reconstruye los hechos que llevaron al asesinato de Santiago Nasar por los gemelos Vicario, explorando la paradoja de que nadie impidió una muerte que todo el pueblo sabía que iba a ocurrir.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788497592437', 2003, 144, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998447/edition/qymyf81wmozrdpknftew.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Gabriel García Márquez'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Honor', 'Crimen', 'Destino', 'Pueblo', 'Honorabilidad');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('La casa de los espíritus', 'La saga de la familia Trueba a lo largo de cuatro generaciones en un país latinoamericano, donde el despotismo del patriarca Esteban Trueba choca con las fuerzas del cambio social y la resistencia espiritual de las mujeres del linaje.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788483462034', 2006, 464, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998521/edition/ifnizopqbf0izxx5wns6.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Isabel Allende'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Realismo mágico', 'Saga familiar', 'Política', 'Amor', 'Chile');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Pedro Páramo', 'Juan Preciado viaja a Comala en cumplimiento de la promesa hecha a su madre moribunda de encontrar a su padre, Pedro Páramo, y descubre un pueblo poblado por murmullos y almas en pena que le revelan la historia del caudillo.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788493442606', 2016, 136, (SELECT id_editorial FROM wm_editorials WHERE name = 'RM Verlag'), 'Edición corregida por la Fundación Juan Rulfo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998635/edition/rz0lelw4ujhckxnhcref.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Juan Rulfo'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Realismo mágico', 'Muerte', 'Pueblo fantasma', 'Voz', 'Memoria');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El túnel', 'El pintor Juan Pablo Castel narra desde la cárcel su obsesión por María Iribarne, la única persona que comprendió una de sus obras, hasta el crimen que consuma su aislamiento definitivo del mundo.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788432248368', 2011, 160, (SELECT id_editorial FROM wm_editorials WHERE name = 'Austral'), 'Narrativa Austral', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998712/edition/qwsbhoirjgzwnssxejzv.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Ernesto Sabato'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Existencialismo', 'Obsesión', 'Incomunicación', 'Pintura', 'Crimen');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('La metamorfosis', 'Gregorio Samsa despierta convertido en un enorme insecto y, mientras su familia enfrenta la repulsión y el rechazo, sufre una progresiva degradación física y emocional.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466367813', 2023, 144, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Ediciones Conmemorativas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998854/edition/yyyaktiy2x2vzuu0ii45.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Franz Kafka'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Alienación', 'Familia', 'Identidad', 'Absurdo', 'Transformación');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El Principito', 'Un piloto varado en el desierto del Sahara conoce a un pequeño príncipe que viaja por distintos mundos y le enseña que lo esencial es invisible a los ojos.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura infantil')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788498381498', 2015, 96, (SELECT id_editorial FROM wm_editorials WHERE name = 'Salamandra'), 'Edición oficial con acuarelas originales', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788998940/edition/vty6gz9hc6mwqcsertjn.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Antoine de Saint-Exupéry'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Amistad', 'Amor', 'Infancia', 'Sabiduría', 'Viaje');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Rayuela', 'Una novela que puede leerse de muchas formas sigue a Horacio Oliveira entre París y Buenos Aires en su búsqueda del sentido de la existencia y del amor de La Maga, planteada como un vasto collage de reflexiones filosóficas y literarias.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466331906', 2016, 736, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999010/edition/y0uxuku9nrjlttuxxhlf.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Julio Cortázar'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Experimentalismo', 'Jazz', 'París', 'Buenos Aires', 'Juego narrativo');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('1984', 'En un Londres distópico vigilado por el Gran Hermano, Winston Smith trabaja reescribiendo la historia para el Partido y, al cuestionar el sistema, se enfrenta a la represión del régimen totalitario.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788499890944', 2013, 352, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Edición definitiva avalada por The Orwell Estate', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999106/edition/psajcpvflxc4xqv1c42e.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'George Orwell'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Distopías', 'Totalitarismo', 'Vigilancia', 'Control social', 'Política');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Fahrenheit 451', 'Guy Montag es un bombero en un futuro que quema libros en lugar de apagar incendios; tras cuestionar su labor, se une a un grupo clandestino dedicado a preservar el conocimiento literario.', (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788491058151', 2026, 192, (SELECT id_editorial FROM wm_editorials WHERE name = 'Penguin Clásicos'), 'Ediciones Icónicas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999367/edition/y2shrmmatiovuji2xnva.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Ray Bradbury'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Distopías', 'Censura', 'Libros', 'Conformismo', 'Rebeldía');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Un mundo feliz', 'En un futuro donde los seres humanos son creados en laboratorio y mantenidos dóciles mediante drogas y entretenimiento constante, uno de ellos cuestiona la perfecta estabilidad del sistema.', (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466350945', 2020, 256, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Colección Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999429/edition/ls4vmtauwjej1soov4ah.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura con sobrecubierta'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Aldous Huxley'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Distopías', 'Sociedad', 'Manipulación', 'Felicidad artificial', 'Tecnología');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El señor de las moscas', 'Un grupo de niños queda varado en una isla desierta y organiza su propia sociedad, pero el orden se desmorona cuando afloran los instintos más primitivos y violentos.', (SELECT id_genre FROM wm_genres WHERE name = 'Novela')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788420674179', 2010, 288, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alianza Editorial'), 'El libro de bolsillo — Bibliotecas de autor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999505/edition/x5wqywqxexcwdsbo2qnz.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'William Golding'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Supervivencia', 'Instinto', 'Naturaleza humana', 'Isla', 'Civilización');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Harry Potter y la piedra filosofal', 'Harry Potter descubre en su undécimo cumpleaños que es un mago y es aceptado en el Colegio Hogwarts de Magia y Hechicería, donde vivirá increíbles aventuras.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788498382662', 2010, 256, (SELECT id_editorial FROM wm_editorials WHERE name = 'Salamandra'), 'Edición clásica con portada ilustrada', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999614/edition/wdzfz2x0ahe1jgnoifjg.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'J. K. Rowling'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Magia', 'Escuela', 'Aventura', 'Amistad', 'Brujería');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Dune', 'En el planeta desértico Arrakis, Paul Atreides se ve envuelto en una lucha por el control de la melange, la especia más valiosa del universo que decide el destino de imperios enteros.', (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466353779', 2021, 784, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Las crónicas de Dune, traducción corregida', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999690/edition/suprncn0dl60xc0aa6xn.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Frank Herbert'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Espacio', 'Ecología', 'Política', 'Imperio', 'Especia');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Fundación', 'El psicohistoriador Hari Seldon prevé la caída del Imperio Galáctico y funda una colonia en el planeta Terminus para preservar el conocimiento y acortar el período de barbarie.' ,(SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788497599245', 2003, 264, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Ciclo de la Fundación', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999748/edition/sntstt9dztpwbt2wrgj4.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Isaac Asimov'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Imperio galáctico', 'Psicohistoria', 'Conocimiento', 'Civilización', 'Poder');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El león, la bruja y el armario', 'Cuatro hermanos descubren un armario que los transporta a Narnia, un reino mágico sumido en un invierno eterno por la malvada Bruja Blanca y del que solo el león Aslan podrá liberarlo.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788420445649', 2000, 168, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alfaguara'), 'Las Crónicas de Narnia', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788999880/edition/usjweporxstdqgcht4wb.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'C. S. Lewis'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Magia', 'Aventura', 'Narnia', 'Hadas', 'Infancia');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Juego de tronos', 'En los continentes de Poniente y Essos, las grandes familias nobles libran guerras por el control del Trono de Hierro mientras en el extremo norte una amenaza milenaria despierta.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788401032424', 2023, 800, (SELECT id_editorial FROM wm_editorials WHERE name = 'Plaza & Janés'), 'Los libros que inspiraron la serie de HBO', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000034/edition/fbs8lfyr1anaswtdmym6.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura con sobrecubierta'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'George R. R. Martin'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Reinos', 'Dragones', 'Guerras', 'Traición', 'Poder');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Los juegos del hambre', 'En una nación distópica, doce chicos y doce chicas son obligados a participar en un reality show donde solo hay una regla: matar o morir. Cuando Katniss Everdeen se ofrece como voluntaria, su instinto de supervivencia la convertirá en un símbolo de esperanza.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788427202122', 2012, 400, (SELECT id_editorial FROM wm_editorials WHERE name = 'Molino'), 'Colección Juegos del Hambre', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000126/edition/iskmpmxnzlyvpxtpmmj1.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Suzanne Collins'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Distopías', 'Supervivencia', 'Futuros oscuros', 'Televisión', 'Rebelión');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('La brújula dorada', 'Lyra, una niña de once años en un mundo donde los humanos tienen daimonion, viaja al Polo Norte para rescatar a los niños secuestrados y descubrir los secretos de la Autoridad.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788416859320', 2019, 400, (SELECT id_editorial FROM wm_editorials WHERE name = 'Roca Bolsillo'), 'La Materia Oscura', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000203/edition/qoxxaeigdily2yhjpr4l.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Philip Pullman'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Aventura', 'Universos paralelos', 'Daimonion', 'Infancia', 'Polo Norte');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El nombre del viento', 'En una posada apartada, un hombre llamado Kvothe accede a contar la auténtica historia de su vida: su infancia como músico itinerante, su paso por una gran ciudad y su llegada a una universidad donde buscaba todas las respuestas.', (SELECT id_genre FROM wm_genres WHERE name = 'Fantasía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788401337208', 2009, 880, (SELECT id_editorial FROM wm_editorials WHERE name = 'Plaza & Janés'), 'Crónica del asesino de reyes, primer día', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000263/edition/ptbftpp1tn3lfgksis6d.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Patrick Rothfuss'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Magia', 'Aventura', 'Música', 'Universidad', 'Leyenda');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Ready Player One', 'En 2044, Wade Watts prefiere el universo virtual de OASIS al sombrío mundo real. Cuando el creador de OASIS muere y deja una fortuna tras una serie de acertijos de los años ochenta, Wade descifra la primera pista y debe competir contra miles de rivales.', (SELECT id_genre FROM wm_genres WHERE name = 'Ciencia ficción')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466663069', 2018, 476, (SELECT id_editorial FROM wm_editorials WHERE name = 'Nova'), 'Colección Nova 231', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000329/edition/jjukq5ernujtx5ddy8p3.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica con solapas'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Ernest Cline'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Realidad virtual', 'Videojuegos', 'Nostalgia', 'Competencia', 'Futuro distópico');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El resplandor', 'Jack Torrance acepta el cargo de cuidador invernal del aislado Hotel Overlook junto a su esposa y su hijo Danny, que posee el don sobrenatural llamado "el resplandor". Poco a poco, las fuerzas malignas del hotel se apoderan de él.', (SELECT id_genre FROM wm_genres WHERE name = 'Terror')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466357319', 2021, 656, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Best Seller Debolsillo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000423/edition/sc1egrtkjnm5b1de7gmm.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Stephen King'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Hotel embrujado', 'Alcoholismo', 'Familia', 'Psicología', 'Aislamiento');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('It (Eso)', 'En el pueblo de Derry, siete niños son aterrados por una entidad que adopta la forma de un payaso siniestro; veintisiete años después, una antigua promesa los hace regresar para enfrentarse a la amenaza que los marcó.', (SELECT id_genre FROM wm_genres WHERE name = 'Terror')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788466345347', 2017, 1030, (SELECT id_editorial FROM wm_editorials WHERE name = 'Punto de Lectura'), 'Colección Bestseller 26200', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1789000528/edition/qgw41hopwaybgwc9fuhc.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Stephen King'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Payaso siniestro', 'Infancia', 'Pueblo maldito', 'Grupo de amigos', 'Miedo ancestral');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Charlie y la fábrica de chocolate', 'Charlie Bucket, un niño de familia pobre, encuentra uno de los cinco billetes de oro escondidos en las chocolatinas de Willy Wonka y gana una visita a su misteriosa fábrica de chocolate.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura infantil')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788491221166', 2016, 240, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alfaguara'), 'Colección Alfaguara Clásicos', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997944/edition/nqgq3n066mxwtdeubcyz.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Roald Dahl'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Chocolate', 'Fábrica', 'Aventura', 'Imaginación', 'Niños');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Matilda', 'Matilda es una niña de cinco años extraordinariamente inteligente, despreciada por sus padres mediocres, que descubre poseer poderes telequinéticos y los emplea contra su abominable directora para cambiar su historia.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura infantil')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788491221364', 2016, 288, (SELECT id_editorial FROM wm_editorials WHERE name = 'Alfaguara'), 'Colección Alfaguara Clásicos', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997858/edition/nikmndfr7uo8wiasnvdd.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Roald Dahl'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Genio precoz', 'Lectura', 'Poderes telequinéticos', 'Escuela', 'Justicia infantil');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Pippi Calzaslargas', 'Pippi Calzaslargas es una niña de nueve años que vive sola en Villa Villekulla con un mono y un caballo; posee una fuerza sobrehumana y un espíritu indomable con el que vive aventuras junto a sus amigos Tommy y Annika.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura infantil')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788416290543', 2015, 285, (SELECT id_editorial FROM wm_editorials WHERE name = 'Blackie Books'), 'Todas las historias', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997757/edition/ye01iupx7cmcf19h0dhx.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa dura'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Astrid Lindgren'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Infancia', 'Aventura', 'Imaginación', 'Independencia', 'Libertad');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Watchmen', 'En un mundo donde los superhéroes han sido prohibidos, un asesinato desencadena una conspiración global; Rorschach, Búho Nocturno, Espectro de Seda, Dr. Manhattan y Ozymandias investigan una trama que cuestiona la naturaleza del poder.', (SELECT id_genre FROM wm_genres WHERE name = 'Superhéroes')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788490946299', 2018, 416, (SELECT id_editorial FROM wm_editorials WHERE name = 'ECC Ediciones'), 'Novela gráfica', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997544/edition/jskmavepxec7mcfvx91g.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) SELECT v_edit_id, id_format FROM wm_formats WHERE name IN ('Cómic', 'Tapa dura con sobrecubierta');
  INSERT INTO wm_book_author (id_book, id_author) SELECT v_book_id, id_author FROM wm_authors WHERE name IN ('Alan Moore', 'Dave Gibbons');
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Superhéroes', 'Distopías', 'Crítica social', 'Poder', 'Moralidad');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('V de Vendetta', 'En una Inglaterra futura gobernada por un régimen fascista, un misterioso enmascarado llamado V desafía al Estado con actos de terrorismo simbólico; la joven Evey Hammond será testigo y cómplice de su guerra por la libertad.', (SELECT id_genre FROM wm_genres WHERE name = 'Superhéroes')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788467420920', 2006, 296, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta DeAgostini Cómics'), 'Novela gráfica', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997449/edition/e8abx57zxs6hq8ttmjhz.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) SELECT v_edit_id, id_format FROM wm_formats WHERE name IN ('Cómic', 'Tapa blanda');
  INSERT INTO wm_book_author (id_book, id_author) SELECT v_book_id, id_author FROM wm_authors WHERE name IN ('Alan Moore', 'David Lloyd');
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Distopías', 'Anarquismo', 'Totalitarismo', 'Libertad', 'Identidad');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Naruto, vol. 1', 'Naruto Uzumaki es un ninja problemático que sueña con convertirse en Hokage, el líder de su aldea; el poder de un zorro de nueve colas está sellado dentro de él, lo que lo convierte en un paria que anhela ser reconocido.', (SELECT id_genre FROM wm_genres WHERE name = 'Manga')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788484492757', 2002, 192, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta Cómic'), 'Manga Shonen', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997325/edition/x8cyum6vay7lypzaxsf2.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Masashi Kishimoto'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Ninjas', 'Amistad', 'Superación', 'Aventura', 'Combate');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('One Piece, vol. 1', 'Monkey D. Luffy, un chico que se comió la Fruta del Diablo y puede estirarse como goma, zarpa al mar buscando el legendario tesoro "One Piece" para convertirse en el Rey de los Piratas.', (SELECT id_genre FROM wm_genres WHERE name = 'Manga')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788468471525', 2011, 192, (SELECT id_editorial FROM wm_editorials WHERE name = 'Planeta DeAgostini Cómics'), 'Manga', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997235/edition/hqeaq957brysdxkgzdgg.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Eiichiro Oda'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Piratas', 'Aventura', 'Tesoro', 'Amistad', 'Sueños');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Sapiens. De animales a dioses', 'Yuval Noah Harari traza la historia de la humanidad desde el Homo sapiens hasta la era del capitalismo, analizando las revoluciones cognitiva, agrícola y científica, y cuestiona si hemos ganado en felicidad.', (SELECT id_genre FROM wm_genres WHERE name = 'Ensayo')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788499926223', 2016, 496, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debate'), 'Ensayo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997156/edition/ceseyydzb4szpkh53glx.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Yuval Noah Harari'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Evolución', 'Historia humana', 'Cultura', 'Civilización', 'Antropología');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('Veinte poemas de amor y una canción desesperada', 'Publicado en 1924 cuando Neruda tenía diecinueve años, este poemario revolucionó la poesía amorosa con versos de intenso erotismo que exploran el amor, el deseo y la pérdida.', (SELECT id_genre FROM wm_genres WHERE name = 'Poesía')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788497933056', 2004, 96, (SELECT id_editorial FROM wm_editorials WHERE name = 'Debolsillo'), 'Contemporánea', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788997087/edition/pj9i3y7cg7nhhip4pizx.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Rústica de bolsillo'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Pablo Neruda'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Amor', 'Pasión', 'Erotismo', 'Melancolía', 'Naturaleza');
END $$;

DO $$
DECLARE v_book_id INTEGER; v_edit_id INTEGER;
BEGIN
  INSERT INTO wm_books (title, summary, genre_id) VALUES
  ('El arte de la guerra', 'Tratado de estrategia militar atribuido al general chino Sun Tzu, compuesto por trece capítulos sobre planificación, engaño, terreno y espionaje, con alcance de filosofía del liderazgo.', (SELECT id_genre FROM wm_genres WHERE name = 'Literatura clásica')) RETURNING id_book INTO v_book_id;
  INSERT INTO wm_editions (book_id, isbn, publication_year, pages, editorial_id, edition, cover_image) VALUES
  (v_book_id, '9788491056652', 2026, 472, (SELECT id_editorial FROM wm_editorials WHERE name = 'Penguin Clásicos'), 'Bilingüe chino-español', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1788996951/edition/ixgw38d7xis0cwznbvu0.webp') RETURNING id_edition INTO v_edit_id;
  INSERT INTO wm_edition_format (id_edition, id_format) VALUES (v_edit_id, (SELECT id_format FROM wm_formats WHERE name = 'Tapa blanda'));
  INSERT INTO wm_book_author (id_book, id_author) VALUES (v_book_id, (SELECT id_author FROM wm_authors WHERE name = 'Sun Tzu'));
  INSERT INTO wm_book_subject (id_book, id_subject) SELECT v_book_id, id_subject FROM wm_subjects WHERE name IN ('Estrategia', 'Milicia', 'Filosofía', 'Liderazgo', 'Conflicto');
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
VALUES ('ROJsom', 'ROJsom', 1, 15, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CORcro-c1', 'CORcro-c1', 2, 16, 1)
ON CONFLICT (barcode) DO NOTHING;
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id)
VALUES ('CORcro', 'CORcro', 1, 16, 3)
ON CONFLICT (barcode) DO NOTHING;

-- === COPIAS DE lista.txt ===
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id) VALUES
('GAIpre', 'GAIpre', 1, 17, 1),
('MILreg', 'MILreg', 1, 18, 1),
('JOHfla', 'JOHfla', 1, 19, 1),
('BALalg', 'BALalg', 1, 20, 1),
('SUSper', 'SUSper', 1, 21, 1),
('MENmet', 'MENmet', 1, 22, 1),
('BENcab', 'BENcab', 1, 23, 1),
('TOLcom', 'TOLcom', 1, 24, 1),
('TOLtor', 'TOLtor', 1, 25, 1),
('TOLret', 'TOLret', 1, 26, 1)
ON CONFLICT (barcode) DO NOTHING;

-- === COPIAS LOTE 3 (34 libros agregados) ===
INSERT INTO wm_copies (barcode, signature_topography, copy_number, edition_id, status_id) VALUES
('GARcie', 'GARcie', 1, 27, 1),
('CERqui', 'CERqui', 1, 28, 1),
('GARcro', 'GARcro', 1, 29, 1),
('ALLcas', 'ALLcas', 1, 30, 1),
('RULped', 'RULped', 1, 31, 1),
('SABtun', 'SABtun', 1, 32, 1),
('KAFmet', 'KAFmet', 1, 33, 1),
('SAIpri', 'SAIpri', 1, 34, 1),
('CORray', 'CORray', 1, 35, 1),
('ORW198', 'ORW198', 1, 36, 1),
('BRAfah', 'BRAfah', 1, 37, 1),
('HUXmun', 'HUXmun', 1, 38, 1),
('GOLsen', 'GOLsen', 1, 39, 1),
('ROWhar', 'ROWhar', 1, 40, 1),
('HERdun', 'HERdun', 1, 41, 1),
('ASIfun', 'ASIfun', 1, 42, 1),
('LEWleo', 'LEWleo', 1, 43, 1),
('MARjue', 'MARjue', 1, 44, 1),
('COLjue', 'COLjue', 1, 45, 1),
('PULbru', 'PULbru', 1, 46, 1),
('ROTnom', 'ROTnom', 1, 47, 1),
('CLIrea', 'CLIrea', 1, 48, 1),
('KINres', 'KINres', 1, 49, 1),
('KINeso', 'KINeso', 1, 50, 1),
('DAHcha', 'DAHcha', 1, 51, 1),
('DAHmat', 'DAHmat', 1, 52, 1),
('LINpip', 'LINpip', 1, 53, 1),
('MOOwat', 'MOOwat', 1, 54, 1),
('MOOvde', 'MOOvde', 1, 55, 1),
('KISnar', 'KISnar', 1, 56, 1),
('ODAone', 'ODAone', 1, 57, 1),
('HARsap', 'HARsap', 1, 58, 1),
('NERvei', 'NERvei', 1, 59, 1),
('SUNart', 'SUNart', 1, 60, 1)
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
