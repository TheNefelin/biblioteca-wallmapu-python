SELECT * FROM wm_authors;
SELECT * FROM wm_book_author;
SELECT * FROM wm_book_subject;
SELECT * FROM wm_books;
SELECT * FROM wm_communes;
SELECT * FROM wm_copies;
SELECT * FROM wm_copy_status;
SELECT * FROM wm_edition_format;
SELECT * FROM wm_editions;
SELECT * FROM wm_editorials;
SELECT * FROM wm_formats;
SELECT * FROM wm_genres;
SELECT * FROM wm_loan_policies;
SELECT * FROM wm_loan_status;
SELECT * FROM wm_loans;
SELECT * FROM wm_news;
SELECT * FROM wm_news_gallery;
SELECT * FROM wm_notifications;
SELECT * FROM wm_provinces;
SELECT * FROM wm_regions;
SELECT * FROM wm_reservation_status;
SELECT * FROM wm_reservations;
SELECT * FROM wm_subjects;
SELECT * FROM wm_user_role;
SELECT * FROM wm_user_status;
SELECT * FROM wm_users;



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
