-- Insert Sample Data for CineVision Movie Service
-- This migration adds initial test data for development

-- Insert Categories
INSERT INTO category (category_name) VALUES 
('Action'),
('Comedy'), 
('Drama'),
('Sci-Fi'),
('Horror'),
('Adventure'),
('Romance'),
('Thriller'),
('Animation'),
('Documentary') 
ON CONFLICT (category_name) DO NOTHING;

-- Insert Directors
INSERT INTO director (director_name, biography, birth_date) VALUES
('Anthony Russo', 'American film director known for directing Marvel films', '1970-02-03'),
('Joe Russo', 'American film director, part of Russo Brothers', '1971-07-18'),
('Jon Watts', 'American film director known for Spider-Man films', '1981-06-28'),
('Matt Reeves', 'American film director and screenwriter', '1966-04-27'),
('James Gunn', 'American filmmaker known for Guardians of the Galaxy', '1966-08-05'),
('Denis Villeneuve', 'Canadian film director', '1967-10-03'),
('Joseph Kosinski', 'American film director', '1974-05-03'),
('Shawn Levy', 'Canadian-American film director', '1968-07-23'),
('James Cameron', 'Canadian film director', '1954-08-16'),
('Christopher Nolan', 'British-American film director', '1970-07-30')
ON CONFLICT DO NOTHING;

-- Insert Cities
INSERT INTO city (city_name) VALUES
('Hà Nội'),
('Hồ Chí Minh'),
('Đà Nẵng'),
('Hải Phòng'),
('Cần Thơ'),
('Nha Trang'),
('Huế'),
('Vũng Tàu')
ON CONFLICT (city_name) DO NOTHING;

-- Insert Saloons
INSERT INTO saloon (saloon_name, city_id, address, seat_capacity) VALUES
('CGV Vincom Center', 1, 'Vincom Center Bà Triệu, Hà Nội', 150),
('Galaxy Cinema Nguyễn Du', 1, 'Nguyễn Du, Hai Bà Trưng, Hà Nội', 200),
('Lotte Cinema Keangnam', 1, 'Keangnam Landmark Tower, Hà Nội', 180),
('CGV Sư Vạn Hạnh', 2, 'Sư Vạn Hạnh Mall, TP.HCM', 160),
('Galaxy Cinema Tân Bình', 2, 'Tân Bình, TP.HCM', 190),
('BHD Star Cineplex', 2, 'Bitexco Financial Tower, TP.HCM', 170),
('Lotte Cinema Đà Nẵng', 3, 'Lotte Mart Đà Nẵng', 140),
('CGV Vincom Đà Nẵng', 3, 'Vincom Plaza Đà Nẵng', 130),
('Cinestar Hai Bà Trưng', 4, 'Hải Phòng Center, Hải Phòng', 120),
('Galaxy Cinema Cần Thơ', 5, 'Vincom Plaza Cần Thơ', 160)
ON CONFLICT DO NOTHING;

-- Insert Movies (with correct category_id and director_id references)
INSERT INTO movie (movie_name, description, duration, release_date, is_display, movie_trailer_url, rating, category_id, director_id) VALUES
('Avengers: Endgame', 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos'' actions and restore balance to the universe.', 181, '2019-04-26', true, 'https://www.youtube.com/embed/TcMBFSGVi1c?autoplay=0', 8.4, 1, 1),
('Spider-Man: No Way Home', 'With Spider-Man''s identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.', 148, '2021-12-17', true, 'https://www.youtube.com/embed/JfVOs4VSpmA?autoplay=0', 8.2, 1, 3),
('The Batman', 'When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city''s hidden corruption and question his family''s involvement.', 176, '2022-03-04', true, 'https://www.youtube.com/embed/mqqft2x_Aa4?autoplay=0', 7.8, 1, 4),
('Guardians of the Galaxy Vol. 3', 'Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own.', 150, '2023-05-05', false, 'https://www.youtube.com/embed/JqcncLPi9zw?autoplay=0', 8.0, 1, 5),
('Dune: Part Two', 'Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.', 166, '2024-03-01', true, 'https://www.youtube.com/embed/Way9Dexny3w?autoplay=0', 8.5, 4, 6),
('Top Gun: Maverick', 'After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN''s elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it.', 130, '2022-05-27', true, 'https://www.youtube.com/embed/qSqVVswa420?autoplay=0', 8.3, 1, 7),
('Deadpool 3', 'Wade Wilson''s world is about to change. Marvel Studios presents Deadpool & Wolverine - an epic team-up featuring everyone''s favorite regenerating degenerate.', 128, '2026-07-26', false, 'https://www.youtube.com/embed/73_1biulkYk?autoplay=0', 8.1, 2, 8),
('Avatar 3', 'The third installment in James Cameron''s Avatar saga continues the story of Jake Sully and his family on Pandora.', 180, '2026-12-20', false, 'https://www.youtube.com/embed/d9MyW72ELq0?autoplay=0', 8.2, 4, 9)
ON CONFLICT DO NOTHING;

-- Insert Movie Images
INSERT INTO movie_image (image_url, movie_id) VALUES
('https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', 1),
('https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg', 2),
('https://image.tmdb.org/t/p/w500/b0PlSFdDwbyK0cf5RxwDpaOJQvQ.jpg', 3),
('https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg', 4),
('https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg', 5),
('https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg', 6),
('https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg', 7),
('https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg', 8)
ON CONFLICT DO NOTHING;

-- Insert Movie-City relationships
INSERT INTO movie_city (movie_id, city_id) VALUES
(1, 1), (1, 2), (1, 3), -- Avengers: Endgame available in Hà Nội, TP.HCM, Đà Nẵng
(2, 1), (2, 2), (2, 4), -- Spider-Man: No Way Home
(3, 1), (3, 2), (3, 3), (3, 5), -- The Batman
(4, 2), (4, 3), (4, 5), -- Guardians of the Galaxy Vol. 3
(5, 1), (5, 2), (5, 3), (5, 4), -- Dune: Part Two
(6, 1), (6, 2), (6, 3), -- Top Gun: Maverick
(7, 2), (7, 3), -- Deadpool 3
(8, 1), (8, 2), (8, 4) -- Avatar 3
ON CONFLICT DO NOTHING;

-- Insert Saloon Times (Showtimes)
INSERT INTO saloon_time (movie_id, saloon_id, movie_date, movie_begin_time, available_seats) VALUES
-- Today and upcoming dates for currently displaying movies
(1, 1, CURRENT_DATE, '10:00:00', 145),
(1, 1, CURRENT_DATE, '14:00:00', 130),
(1, 1, CURRENT_DATE, '18:00:00', 120),
(1, 2, CURRENT_DATE, '11:30:00', 180),
(1, 2, CURRENT_DATE, '16:30:00', 170),
(1, 2, CURRENT_DATE, '20:30:00', 160),
(2, 4, CURRENT_DATE, '13:00:00', 140),
(2, 4, CURRENT_DATE, '17:00:00', 135),
(2, 4, CURRENT_DATE, '21:00:00', 130),
(3, 1, CURRENT_DATE + INTERVAL '1 day', '12:00:00', 160),
(3, 2, CURRENT_DATE + INTERVAL '1 day', '15:30:00', 150),
(5, 1, CURRENT_DATE + INTERVAL '2 days', '19:00:00', 140),
(5, 4, CURRENT_DATE + INTERVAL '2 days', '14:30:00', 155),
(6, 2, CURRENT_DATE + INTERVAL '3 days', '16:00:00', 175)
ON CONFLICT DO NOTHING;

-- Insert Actors
INSERT INTO actor (actor_name, biography, birth_date, movie_id, character_name) VALUES
('Robert Downey Jr.', 'American actor and producer', '1965-04-04', 1, 'Tony Stark / Iron Man'),
('Chris Evans', 'American actor', '1981-06-13', 1, 'Steve Rogers / Captain America'),
('Scarlett Johansson', 'American actress', '1984-11-22', 1, 'Natasha Romanoff / Black Widow'),
('Tom Holland', 'British actor', '1996-06-01', 2, 'Peter Parker / Spider-Man'),
('Zendaya', 'American actress and singer', '1996-09-01', 2, 'MJ'),
('Willem Dafoe', 'American actor', '1955-07-22', 2, 'Norman Osborn / Green Goblin'),
('Robert Pattinson', 'British actor', '1986-05-13', 3, 'Bruce Wayne / Batman'),
('Zoë Kravitz', 'American actress', '1988-12-01', 3, 'Selina Kyle / Catwoman'),
('Paul Dano', 'American actor', '1984-06-19', 3, 'Edward Nashton / The Riddler'),
('Chris Pratt', 'American actor', '1979-06-21', 4, 'Peter Quill / Star-Lord'),
('Timothée Chalamet', 'American-French actor', '1995-12-27', 5, 'Paul Atreides'),
('Tom Cruise', 'American actor', '1962-07-03', 6, 'Pete "Maverick" Mitchell')
ON CONFLICT DO NOTHING;

-- Insert Sample Comments (using mock user IDs)
INSERT INTO comment (content, user_id, user_name, movie_id) VALUES
('Phim tuyệt vời! Rất khuyến khích xem.', 'user_001', 'Nguyễn Văn An', 1),
('Hiệu ứng hình ảnh và cốt truyện tuyệt vời.', 'user_002', 'Trần Thị Bình', 1),
('Phim hay, diễn viên diễn xuất rất tốt!', 'user_003', 'Lê Minh Châu', 2),
('Cảnh hành động kịch tính, đáng xem.', 'user_004', 'Phạm Thu Dung', 2),
('Spider-Man xuất sắc trong phần này!', 'user_005', 'Hoàng Minh Tuấn', 2),
('Batman phiên bản mới rất ấn tượng.', 'user_006', 'Đinh Thị Lan', 3),
('Phim khoa học viễn tưởng hay nhất năm.', 'user_007', 'Vũ Đức Minh', 5),
('Top Gun: Maverick không thể tuyệt vời hơn!', 'user_008', 'Bùi Thị Hương', 6)
ON CONFLICT DO NOTHING;