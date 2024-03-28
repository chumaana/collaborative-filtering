-- Book data
delete from filtering_book;
insert into filtering_book (id, name, author) values (1, 'GhostWatcher', 'Liza Hallgath');
insert into filtering_book (id, name, author) values (2, 'Percy Jackson: Sea of Monsters', 'Farris Egalton');
insert into filtering_book (id, name, author) values (3, 'Winnie the Pooh and the Blustery Day', 'Sasha Fattorini');
insert into filtering_book (id, name, author) values (4, 'Civil Action, A', 'Tessie Stratford');
insert into filtering_book (id, name, author) values (5, 'Ride Lonesome', 'Clo Swigger');
insert into filtering_book (id, name, author) values (6, 'Spontaneous Combustion', 'Nerta Faiers');
insert into filtering_book (id, name, author) values (7, 'Rango', 'Curtice Trunkfield');
insert into filtering_book (id, name, author) values (8, 'Hungarian Fairy Tale, A (Hol volt, hol nem volt)', 'Bealle Parradice');
insert into filtering_book (id, name, author) values (9, 'Party Girl', 'Horton Harty');
insert into filtering_book (id, name, author) values (10, '27 Missing Kisses', 'Miguel Ouldred');

-- User data

-- Review data
delete from filtering_review;
insert into filtering_review (id, book_id, user_id, rate) values (1, 6, 4, 1);
insert into filtering_review (id, book_id, user_id, rate) values (2, 3, 3, 2);
insert into filtering_review (id, book_id, user_id, rate) values (3, 7, 3, 3);
insert into filtering_review (id, book_id, user_id, rate) values (4, 5, 5, 5);
insert into filtering_review (id, book_id, user_id, rate) values (5, 7, 6, 5);
insert into filtering_review (id, book_id, user_id, rate) values (6, 2, 6, 4);
insert into filtering_review (id, book_id, user_id, rate) values (7, 9, 3, 2);
insert into filtering_review (id, book_id, user_id, rate) values (8, 6, 3, 1);
insert into filtering_review (id, book_id, user_id, rate) values (9, 4, 4, 4);
insert into filtering_review (id, book_id, user_id, rate) values (10, 2, 4, 3);
insert into filtering_review (id, book_id, user_id, rate) values (11, 2, 3, 3);
insert into filtering_review (id, book_id, user_id, rate) values (12, 2, 5, 4);
insert into filtering_review (id, book_id, user_id, rate) values (13, 7, 4, 3);
insert into filtering_review (id, book_id, user_id, rate) values (14, 7, 5, 5);
insert into filtering_review (id, book_id, user_id, rate) values (15, 6, 6, 1);


