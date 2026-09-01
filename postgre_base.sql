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
BEGIN;

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

COMMIT;
-- ---------------------------------------------------------------------------------
