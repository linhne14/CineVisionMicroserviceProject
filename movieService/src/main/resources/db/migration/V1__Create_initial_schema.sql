-- CineVision Movie Service Initial Database Schema
-- Created for PostgreSQL database

-- Create Category table
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Director table
CREATE TABLE IF NOT EXISTS director (
    director_id SERIAL PRIMARY KEY,
    director_name VARCHAR(200) NOT NULL,
    biography TEXT,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Movie table
CREATE TABLE IF NOT EXISTS movie (
    movie_id SERIAL PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL,
    description TEXT,
    duration INTEGER NOT NULL CHECK (duration > 0),
    release_date DATE NOT NULL,
    is_display BOOLEAN DEFAULT true,
    movie_trailer_url VARCHAR(500),
    rating DECIMAL(3,1) DEFAULT 0.0 CHECK (rating >= 0.0 AND rating <= 10.0),
    category_id INTEGER REFERENCES category(category_id) ON DELETE SET NULL,
    director_id INTEGER REFERENCES director(director_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Movie Image table
CREATE TABLE IF NOT EXISTS movie_image (
    image_id SERIAL PRIMARY KEY,
    image_url VARCHAR(500) NOT NULL,
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(movie_id) -- One image per movie
);

-- Create City table
CREATE TABLE IF NOT EXISTS city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Saloon table
CREATE TABLE IF NOT EXISTS saloon (
    saloon_id SERIAL PRIMARY KEY,
    saloon_name VARCHAR(200) NOT NULL,
    city_id INTEGER NOT NULL REFERENCES city(city_id) ON DELETE CASCADE,
    address TEXT,
    seat_capacity INTEGER DEFAULT 100 CHECK (seat_capacity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Movie City junction table (Many-to-Many)
CREATE TABLE IF NOT EXISTS movie_city (
    movie_id INTEGER REFERENCES movie(movie_id) ON DELETE CASCADE,
    city_id INTEGER REFERENCES city(city_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, city_id)
);

-- Create Saloon Time table
CREATE TABLE IF NOT EXISTS saloon_time (
    saloon_time_id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    saloon_id INTEGER NOT NULL REFERENCES saloon(saloon_id) ON DELETE CASCADE,
    movie_date DATE NOT NULL,
    movie_begin_time TIME NOT NULL,
    available_seats INTEGER DEFAULT 100 CHECK (available_seats >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(movie_id, saloon_id, movie_date, movie_begin_time)
);

-- Create Actor table
CREATE TABLE IF NOT EXISTS actor (
    actor_id SERIAL PRIMARY KEY,
    actor_name VARCHAR(200) NOT NULL,
    biography TEXT,
    birth_date DATE,
    movie_id INTEGER REFERENCES movie(movie_id) ON DELETE CASCADE,
    character_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Comment table
CREATE TABLE IF NOT EXISTS comment (
    comment_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id VARCHAR(100) NOT NULL, -- Reference to MongoDB user
    user_name VARCHAR(200) NOT NULL,
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_movie_category ON movie(category_id);
CREATE INDEX IF NOT EXISTS idx_movie_director ON movie(director_id);
CREATE INDEX IF NOT EXISTS idx_movie_release_date ON movie(release_date);
CREATE INDEX IF NOT EXISTS idx_movie_is_display ON movie(is_display);
CREATE INDEX IF NOT EXISTS idx_saloon_time_movie ON saloon_time(movie_id);
CREATE INDEX IF NOT EXISTS idx_saloon_time_date ON saloon_time(movie_date);
CREATE INDEX IF NOT EXISTS idx_comment_movie ON comment(movie_id);
CREATE INDEX IF NOT EXISTS idx_comment_user ON comment(user_id);
CREATE INDEX IF NOT EXISTS idx_actor_movie ON actor(movie_id);

-- Add triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_category_updated_at BEFORE UPDATE ON category FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_director_updated_at BEFORE UPDATE ON director FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_movie_updated_at BEFORE UPDATE ON movie FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_comment_updated_at BEFORE UPDATE ON comment FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();