#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock Backend Server for CineVision Frontend
Runs on port 8080 to serve mock movie data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
import time

# Mock data
MOCK_MOVIES = [
    {
        "id": 1,
        "movieId": 1,
        "movieName": "Avengers: Endgame",
        "moviePoster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "description": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "movieDescription": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "movieTrailerUrl": "https://www.youtube.com/embed/TcMBFSGVi1c?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/TcMBFSGVi1c?autoplay=0",
        "directorName": "Anthony Russo, Joe Russo",
        "movieDirector": "Anthony Russo, Joe Russo",
        "releaseDate": "2019-04-26",
        "movieReleaseDate": "2019-04-26",
        "duration": 181,
        "movieDuration": 181,
        "categoryName": "Action, Adventure, Sci-Fi",
        "movieCategory": "Action, Adventure, Sci-Fi",
        "rating": 8.4
    },
    {
        "id": 2,
        "movieId": 2,
        "movieName": "Spider-Man: No Way Home",
        "moviePoster": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "description": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
        "movieDescription": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
        "movieTrailerUrl": "https://www.youtube.com/embed/JfVOs4VSpmA?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/JfVOs4VSpmA?autoplay=0",
        "directorName": "Jon Watts",
        "movieDirector": "Jon Watts",
        "releaseDate": "2021-12-17",
        "movieReleaseDate": "2021-12-17",
        "duration": 148,
        "movieDuration": 148,
        "categoryName": "Action, Adventure, Sci-Fi",
        "movieCategory": "Action, Adventure, Sci-Fi",
        "rating": 8.2
    },
    {
        "id": 3,
        "movieId": 3,
        "movieName": "The Batman",
        "moviePoster": "https://image.tmdb.org/t/p/w500/b0PlSFdDwbyK0cf5RxwDpaOJQvQ.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/b0PlSFdDwbyK0cf5RxwDpaOJQvQ.jpg",
        "description": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement.",
        "movieDescription": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement.",
        "movieTrailerUrl": "https://www.youtube.com/embed/mqqft2x_Aa4?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/mqqft2x_Aa4?autoplay=0",
        "directorName": "Matt Reeves",
        "movieDirector": "Matt Reeves",
        "releaseDate": "2022-03-04",
        "movieReleaseDate": "2022-03-04",
        "duration": 176,
        "movieDuration": 176,
        "categoryName": "Action, Crime, Drama",
        "movieCategory": "Action, Crime, Drama",
        "rating": 7.8
    },
    {
        "id": 4,
        "movieId": 4,
        "movieName": "Guardians of the Galaxy Vol. 3",
        "moviePoster": "https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
        "description": "Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own.",
        "movieDescription": "Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own.",
        "movieTrailerUrl": "https://www.youtube.com/embed/JqcncLPi9zw?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/JqcncLPi9zw?autoplay=0",
        "directorName": "James Gunn",
        "movieDirector": "James Gunn",
        "releaseDate": "2023-05-05",
        "movieReleaseDate": "2023-05-05",
        "duration": 150,
        "movieDuration": 150,
        "categoryName": "Action, Adventure, Comedy",
        "movieCategory": "Action, Adventure, Comedy",
        "rating": 8.0
    },
    {
        "id": 5,
        "movieId": 5,
        "movieName": "Dune: Part Two",
        "moviePoster": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
        "description": "Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.",
        "movieDescription": "Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.",
        "movieTrailerUrl": "https://www.youtube.com/embed/Way9Dexny3w?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/Way9Dexny3w?autoplay=0",
        "directorName": "Denis Villeneuve",
        "movieDirector": "Denis Villeneuve",
        "releaseDate": "2024-03-01",
        "movieReleaseDate": "2024-03-01",
        "duration": 166,
        "movieDuration": 166,
        "categoryName": "Action, Adventure, Sci-Fi",
        "movieCategory": "Action, Adventure, Sci-Fi",
        "rating": 8.5
    },
    {
        "id": 6,
        "movieId": 6,
        "movieName": "Top Gun: Maverick",
        "moviePoster": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg",
        "description": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it.",
        "movieDescription": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it.",
        "movieTrailerUrl": "https://www.youtube.com/embed/qSqVVswa420?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/qSqVVswa420?autoplay=0",
        "directorName": "Joseph Kosinski",
        "movieDirector": "Joseph Kosinski",
        "releaseDate": "2022-05-27",
        "movieReleaseDate": "2022-05-27",
        "duration": 130,
        "movieDuration": 130,
        "categoryName": "Action, Drama",
        "movieCategory": "Action, Drama",
        "rating": 8.3
    },
    {
        "id": 7,
        "movieId": 7,
        "movieName": "Deadpool 3",
        "moviePoster": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "description": "Wade Wilson's world is about to change. Marvel Studios presents Deadpool & Wolverine - an epic team-up featuring everyone's favorite regenerating degenerate.",
        "movieDescription": "Wade Wilson's world is about to change. Marvel Studios presents Deadpool & Wolverine - an epic team-up featuring everyone's favorite regenerating degenerate.",
        "movieTrailerUrl": "https://www.youtube.com/embed/73_1biulkYk?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/73_1biulkYk?autoplay=0",
        "directorName": "Shawn Levy",
        "movieDirector": "Shawn Levy",
        "releaseDate": "2026-07-26",
        "movieReleaseDate": "2026-07-26",
        "duration": 128,
        "movieDuration": 128,
        "categoryName": "Action, Comedy, Superhero",
        "movieCategory": "Action, Comedy, Superhero",
        "rating": 8.1
    },
    {
        "id": 8,
        "movieId": 8,
        "movieName": "Avatar 3",
        "moviePoster": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
        "description": "The third installment in James Cameron's Avatar saga continues the story of Jake Sully and his family on Pandora.",
        "movieDescription": "The third installment in James Cameron's Avatar saga continues the story of Jake Sully and his family on Pandora.",
        "movieTrailerUrl": "https://www.youtube.com/embed/d9MyW72ELq0?autoplay=0",
        "movieTrailer": "https://www.youtube.com/embed/d9MyW72ELq0?autoplay=0",
        "directorName": "James Cameron",
        "movieDirector": "James Cameron",
        "releaseDate": "2026-12-20",
        "movieReleaseDate": "2026-12-20",
        "duration": 180,
        "movieDuration": 180,
        "categoryName": "Action, Adventure, Sci-Fi",
        "movieCategory": "Action, Adventure, Sci-Fi",
        "rating": 8.2
    }
]

class MockBackendHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Suppress default request logging"""
        return

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
        except (ConnectionAbortedError, BrokenPipeError):
            print("🔌 Client disconnected during OPTIONS")
            return

    def do_GET(self):
        """Handle GET requests"""
        try:
            path = self.path
            print(f"📥 GET request to: {path}")
            
            if path == '/api/movie/movies/displayingMovies':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(MOCK_MOVIES)
                self.wfile.write(response.encode())
                print("✅ Served displaying movies")
                
            elif path == '/api/movie/movies/comingSoonMovies':
                # Coming soon movies - with complete movie data for detail pages
                coming_soon = [
                    {
                        "id": 4,
                        "movieId": 4,
                        "movieName": "Guardians of the Galaxy Vol. 3",
                        "moviePoster": "https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
                        "movieImageUrl": "https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
                        "description": "Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own.",
                        "movieDescription": "Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own.",
                        "movieTrailerUrl": "https://www.youtube.com/embed/JqcncLPi9zw?autoplay=0",
                        "movieTrailer": "https://www.youtube.com/embed/JqcncLPi9zw?autoplay=0",
                        "directorName": "James Gunn",
                        "movieDirector": "James Gunn",
                        "releaseDate": "2026-05-05",
                        "movieReleaseDate": "2026-05-05",
                        "duration": 150,
                        "movieDuration": 150,
                        "categoryName": "Action, Adventure, Comedy",
                        "movieCategory": "Action, Adventure, Comedy",
                        "rating": 8.0
                    },
                    {
                        "id": 7,
                        "movieId": 7,
                        "movieName": "Deadpool 3",
                        "moviePoster": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
                        "movieImageUrl": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
                        "description": "Wade Wilson's world is about to change. Marvel Studios presents Deadpool & Wolverine - an epic team-up featuring everyone's favorite regenerating degenerate.",
                        "movieDescription": "Wade Wilson's world is about to change. Marvel Studios presents Deadpool & Wolverine - an epic team-up featuring everyone's favorite regenerating degenerate.",
                        "movieTrailerUrl": "https://www.youtube.com/embed/73_1biulkYk?autoplay=0",
                        "movieTrailer": "https://www.youtube.com/embed/73_1biulkYk?autoplay=0",
                        "directorName": "Shawn Levy",
                        "movieDirector": "Shawn Levy",
                        "releaseDate": "2026-07-26",
                        "movieReleaseDate": "2026-07-26",
                        "duration": 128,
                        "movieDuration": 128,
                        "categoryName": "Action, Comedy, Superhero",
                        "movieCategory": "Action, Comedy, Superhero",
                        "rating": 8.1
                    },
                    {
                        "id": 8,
                        "movieId": 8,
                        "movieName": "Avatar 3",
                        "moviePoster": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
                        "movieImageUrl": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
                        "description": "The third installment in James Cameron's Avatar saga continues the story of Jake Sully and his family on Pandora.",
                        "movieDescription": "The third installment in James Cameron's Avatar saga continues the story of Jake Sully and his family on Pandora.",
                        "movieTrailerUrl": "https://www.youtube.com/embed/d9MyW72ELq0?autoplay=0",
                        "movieTrailer": "https://www.youtube.com/embed/d9MyW72ELq0?autoplay=0",
                        "directorName": "James Cameron",
                        "movieDirector": "James Cameron",
                        "releaseDate": "2026-12-20",
                        "movieReleaseDate": "2026-12-20",
                        "duration": 180,
                        "movieDuration": 180,
                        "categoryName": "Action, Adventure, Sci-Fi",
                        "movieCategory": "Action, Adventure, Sci-Fi",
                        "rating": 8.2
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(coming_soon)
                self.wfile.write(response.encode())
                print("✅ Served coming soon movies")
                
            elif path.startswith('/api/movie/movies/') and path.split('/')[-1].isdigit():
                # Get specific movie by ID
                movie_id = int(path.split('/')[-1])
                movie = next((m for m in MOCK_MOVIES if m['id'] == movie_id), None)
                
                if movie:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(movie)
                    self.wfile.write(response.encode())
                    print(f"✅ Served movie {movie_id}")
                else:
                    self.send_response(404)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"error": "Movie not found"}')
                    print(f"❌ Movie {movie_id} not found")
            
            elif path.startswith('/api/movie/saloons/getByCityId/') or path.startswith('/api/movie/saloons/getSaloonsByCityId/'):
                # Get saloons by city ID (support both endpoint formats)
                city_id = None
                if '/getByCityId/' in path:
                    city_id = path.split('/getByCityId/')[-1]
                elif '/getSaloonsByCityId/' in path:
                    city_id = path.split('/getSaloonsByCityId/')[-1]
                
                # Mock saloons based on city ID
                all_saloons = [
                    {"saloonId": 1, "saloonName": "CGV Vincom Center", "cityId": 1},
                    {"saloonId": 2, "saloonName": "Galaxy Cinema", "cityId": 1}, 
                    {"saloonId": 3, "saloonName": "Lotte Cinema", "cityId": 2},
                    {"saloonId": 4, "saloonName": "BHD Star Cineplex", "cityId": 2},
                    {"saloonId": 5, "saloonName": "Cinestar Cinema", "cityId": 3}
                ]
                
                # Filter by city ID if provided
                if city_id and city_id.isdigit():
                    city_id = int(city_id)
                    filtered_saloons = [s for s in all_saloons if s['cityId'] == city_id]
                    mock_saloons = filtered_saloons if filtered_saloons else all_saloons[:2]  # Fallback
                else:
                    mock_saloons = all_saloons[:3]  # Default saloons
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloons)
                self.wfile.write(response.encode())
                print(f"✅ Served saloons for city {city_id}")
            
            elif path == '/api/movie/saloons/getall':
                # Get all saloons
                mock_saloons = [
                    {"saloonId": 1, "saloonName": "CGV Vincom Center", "cityId": 1},
                    {"saloonId": 2, "saloonName": "Galaxy Cinema", "cityId": 1},
                    {"saloonId": 3, "saloonName": "Lotte Cinema", "cityId": 2}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloons)
                self.wfile.write(response.encode())
                print("✅ Served all saloons")
                
            elif path == '/api/movie/cities/getall':
                # Get all cities
                mock_cities = [
                    {"cityId": 1, "cityName": "Hà Nội"},
                    {"cityId": 2, "cityName": "Hồ Chí Minh"},
                    {"cityId": 3, "cityName": "Đà Nẵng"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_cities)
                self.wfile.write(response.encode())
                print("✅ Served all cities")
                
            elif path.startswith('/api/movie/comments/getCountOfComments/'):
                # Get comment count - mock data
                mock_count = {"count": 5}
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_count)
                self.wfile.write(response.encode())
                print("✅ Served comment count")
                
            elif '/api/movie/comments/getCommentsByMovieId/' in path:
                # Get comments by movie ID - mock comments
                mock_comments = [
                    {
                        "id": 1,
                        "content": "Phim tuyệt vời! Rất khuyến khích xem.",
                        "user": {"name": "Nguyễn Văn An"},
                        "createdAt": "2023-10-01"
                    },
                    {
                        "id": 2,
                        "content": "Hiệu ứng hình ảnh và cốt truyện tuyệt vời.",
                        "user": {"name": "Trần Thị Bình"},
                        "createdAt": "2023-10-02"
                    },
                    {
                        "id": 3,
                        "content": "Phim hay, diễn viên diễn xuất rất tốt!",
                        "user": {"name": "Lê Minh Châu"},
                        "createdAt": "2023-10-03"
                    },
                    {
                        "id": 4,
                        "content": "Cảnh hành động kịch tính, đáng xem.",
                        "user": {"name": "Phạm Thu Dung"},
                        "createdAt": "2023-10-04"
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_comments)
                self.wfile.write(response.encode())
                print("✅ Served comments")
            
            elif path.startswith('/api/movie/saloonTimes/getSaloonTimesByMovieId/'):
                # Get saloon times by movie ID - mock showtime data
                mock_saloon_times = [
                    {
                        "id": 1,
                        "movieBeginTime": "14:00",
                        "movieDate": "2025-10-30",
                        "movieId": 1,
                        "saloonId": 1,
                        "saloon": {"saloonName": "CGV Vincom Center"}
                    },
                    {
                        "id": 2,
                        "movieBeginTime": "16:30",
                        "movieDate": "2025-10-30",
                        "movieId": 1,
                        "saloonId": 1,
                        "saloon": {"saloonName": "CGV Vincom Center"}
                    },
                    {
                        "id": 3,
                        "movieBeginTime": "19:00",
                        "movieDate": "2025-10-30",
                        "movieId": 1,
                        "saloonId": 2,
                        "saloon": {"saloonName": "Galaxy Cinema"}
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloon_times)
                self.wfile.write(response.encode())
                print("✅ Served saloon times")
                
            elif path.startswith('/api/movie/actors/getActorsByMovieId/'):
                # Get actors by movie ID - mock actors data
                mock_actors = [
                    {"id": 1, "name": "Robert Downey Jr.", "character": "Tony Stark / Iron Man"},
                    {"id": 2, "name": "Chris Evans", "character": "Steve Rogers / Captain America"},
                    {"id": 3, "name": "Scarlett Johansson", "character": "Natasha Romanoff / Black Widow"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_actors)
                self.wfile.write(response.encode())
                print("✅ Served actors")
                
            elif path.startswith('/api/movie/cities/getCitiesByMovieId/'):
                # Get cities by movie ID - mock cities for movie
                mock_movie_cities = [
                    {"cityId": 1, "cityName": "Hà Nội"},
                    {"cityId": 2, "cityName": "Hồ Chí Minh"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_movie_cities)
                self.wfile.write(response.encode())
                print("✅ Served cities for movie")
                
            elif path == '/health':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"status": "OK", "message": "Mock Backend đang hoạt động"})
                self.wfile.write(response.encode())
                print("✅ Health check")
                
            elif path.startswith('/api/movie/saloonTimes/getMovieSaloonTimeSaloonAndMovieId/'):
                # Get movie saloon times by saloonId and movieId
                # Extract saloonId and movieId from path
                path_parts = path.split('/')
                if len(path_parts) >= 6:
                    saloon_id = path_parts[-2]
                    movie_id = path_parts[-1]
                    
                    mock_saloon_times = [
                        {"movieBeginTime": "10:00", "saloonId": int(saloon_id), "movieId": int(movie_id)},
                        {"movieBeginTime": "13:00", "saloonId": int(saloon_id), "movieId": int(movie_id)},
                        {"movieBeginTime": "16:00", "saloonId": int(saloon_id), "movieId": int(movie_id)},
                        {"movieBeginTime": "19:00", "saloonId": int(saloon_id), "movieId": int(movie_id)},
                        {"movieBeginTime": "22:00", "saloonId": int(saloon_id), "movieId": int(movie_id)}
                    ]
                else:
                    mock_saloon_times = []
                    
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloon_times)
                self.wfile.write(response.encode())
                print(f"✅ Served saloon times for saloon {saloon_id} movie {movie_id}")
                
            # Admin endpoints
            elif path == '/api/movie/actors/getall':
                mock_actors = [
                    {"id": 1, "name": "Robert Downey Jr.", "actorName": "Robert Downey Jr."},
                    {"id": 2, "name": "Chris Evans", "actorName": "Chris Evans"},
                    {"id": 3, "name": "Scarlett Johansson", "actorName": "Scarlett Johansson"},
                    {"id": 4, "name": "Tom Holland", "actorName": "Tom Holland"},
                    {"id": 5, "name": "Robert Pattinson", "actorName": "Robert Pattinson"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"success": True, "data": mock_actors})
                self.wfile.write(response.encode())
                print("✅ Served all actors")
                
            elif path == '/api/movie/categories/getall':
                mock_categories = [
                    {"id": 1, "name": "Action", "categoryName": "Action"},
                    {"id": 2, "name": "Comedy", "categoryName": "Comedy"},
                    {"id": 3, "name": "Drama", "categoryName": "Drama"},
                    {"id": 4, "name": "Sci-Fi", "categoryName": "Sci-Fi"},
                    {"id": 5, "name": "Horror", "categoryName": "Horror"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"success": True, "data": mock_categories})
                self.wfile.write(response.encode())
                print("✅ Served all categories")
                
            elif path == '/api/movie/directors/getall':
                mock_directors = [
                    {"id": 1, "name": "Anthony Russo", "directorName": "Anthony Russo"},
                    {"id": 2, "name": "Joe Russo", "directorName": "Joe Russo"},
                    {"id": 3, "name": "Jon Watts", "directorName": "Jon Watts"},
                    {"id": 4, "name": "Matt Reeves", "directorName": "Matt Reeves"},
                    {"id": 5, "name": "Christopher Nolan", "directorName": "Christopher Nolan"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"success": True, "data": mock_directors})
                self.wfile.write(response.encode())
                print("✅ Served all directors")
                
            else:
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Endpoint not found"}')
                print(f"❌ Unknown endpoint: {path}")
                
        except ConnectionAbortedError:
            print("🔌 Client disconnected")
            return
        except BrokenPipeError:
            print("🔧 Broken pipe")
            return
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({"error": str(e)})
                self.wfile.write(error_response.encode())
                print(f"💥 Error: {e}")
            except (ConnectionAbortedError, BrokenPipeError):
                print("🔌 Client disconnected during error response")
                return

    def do_POST(self):
        """Handle POST requests"""
        try:
            path = self.path
            print(f"📥 POST request to: {path}")
            
            if path == '/api/movie/payments/sendTicketDetail':
                # Get the content length and read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse the JSON data
                    ticket_data = json.loads(post_data.decode('utf-8'))
                    print(f"🎫 Received ticket data: {ticket_data}")
                    
                    # Mock successful payment response
                    payment_response = {
                        "success": True,
                        "message": "Đặt vé thành công!",
                        "ticketId": "TK" + str(int(time.time())),
                        "bookingDetails": {
                            "movieTitle": ticket_data.get("movieTitle", "Unknown Movie"),
                            "seats": ticket_data.get("chairNumbers", []),
                            "totalPrice": ticket_data.get("totalPrice", 0),
                            "bookingTime": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(payment_response)
                    self.wfile.write(response.encode())
                    print("✅ Payment processed successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in payment request")
                    
            elif path == '/api/user/users/add':
                # User registration endpoint
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse the JSON data
                    user_data = json.loads(post_data.decode('utf-8'))
                    print(f"👤 Received user registration: {user_data}")
                    
                    # Mock successful registration response
                    registration_response = {
                        "success": True,
                        "message": "Đăng ký người dùng thành công!",
                        "userId": "USER" + str(int(time.time())),
                        "userDetails": {
                            "email": user_data.get("email", ""),
                            "name": user_data.get("name", ""),
                            "registeredAt": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(registration_response)
                    self.wfile.write(response.encode())
                    print("✅ User registered successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in registration request")
                    
            elif path == '/api/user/auth/login':
                # User login endpoint
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse the JSON data
                    login_data = json.loads(post_data.decode('utf-8'))
                    print(f"🔐 Received login attempt: {login_data}")
                    
                    # Mock successful login response with admin check
                    user_email = login_data.get("email", "")
                    user_password = login_data.get("password", "")
                    user_id = "USER_" + str(int(time.time()))
                    user_name = user_email.split('@')[0] if '@' in user_email else "Demo User"
                    
                    # Check for admin credentials
                    if user_email == "admin@cinevision.com" and user_password == "admin123":
                        user_roles = ["ADMIN"]
                        user_name = "Administrator"
                        user_id = "ADMIN_001"
                    else:
                        user_roles = ["User"]
                    
                    login_response = {
                        "success": True,
                        "message": "Đăng nhập thành công!",
                        "token": "mock_jwt_token_" + str(int(time.time())),
                        "userId": user_id,
                        "email": user_email,
                        "fullName": user_name,
                        "name": user_name,
                        "roles": user_roles,
                        "user": {
                            "email": user_email,
                            "name": user_name,
                            "role": user_roles[0].lower(),
                            "userId": user_id,
                            "loginTime": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(login_response)
                    self.wfile.write(response.encode())
                    print("✅ User logged in successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in login request")
                    
            elif path == '/api/movie/comments/add':
                # Add comment endpoint
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse the JSON data
                    comment_data = json.loads(post_data.decode('utf-8'))
                    print(f"💬 Received comment: {comment_data}")
                    
                    # Mock new comment response
                    new_comment = {
                        "commentId": "COMMENT" + str(int(time.time())),
                        "commentText": comment_data.get("commentText", ""),
                        "commentBy": comment_data.get("commentBy", "Khách ẩn danh"),
                        "commentByUserId": comment_data.get("commentByUserId", ""),
                        "movieId": comment_data.get("movieId", ""),
                        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(new_comment)
                    self.wfile.write(response.encode())
                    print("✅ Comment added successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in comment request")
                    
            elif path == '/api/movie/comments/delete':
                # Delete comment endpoint
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse the JSON data
                    delete_data = json.loads(post_data.decode('utf-8'))
                    print(f"🗑️ Deleting comment: {delete_data}")
                    
                    # Mock successful deletion response
                    delete_response = {
                        "success": True,
                        "message": "Xóa bình luận thành công!",
                        "deletedCommentId": delete_data.get("commentId", "")
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(delete_response)
                    self.wfile.write(response.encode())
                    print("✅ Comment deleted successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in delete comment request")
                    
            elif path == '/api/movie/movies/add':
                # Handle movie addition by admin
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    movie_data = json.loads(post_data.decode('utf-8'))
                    print(f"🎬 Received movie addition: {movie_data}")
                    
                    # Mock successful movie addition response
                    new_movie_id = len(MOCK_MOVIES) + 1
                    add_response = {
                        "success": True,
                        "message": "Thêm phim thành công!",
                        "movieId": new_movie_id,
                        "data": {
                            "id": new_movie_id,
                            "movieId": new_movie_id,
                            "movieName": movie_data.get("movieName", "New Movie"),
                            "addedAt": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(add_response)
                    self.wfile.write(response.encode())
                    print("✅ Movie added successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in movie addition request")
                    
            elif path == '/api/movie/directors/add':
                # Handle director addition by admin
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    director_data = json.loads(post_data.decode('utf-8'))
                    print(f"🎭 Received director addition: {director_data}")
                    
                    # Mock successful director addition response
                    new_director_id = 100 + int(time.time() % 1000)
                    add_response = {
                        "success": True,
                        "message": "Thêm đạo diễn thành công!",
                        "data": {
                            "directorId": new_director_id,
                            "id": new_director_id,
                            "directorName": director_data.get("directorName", "New Director"),
                            "addedAt": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(add_response)
                    self.wfile.write(response.encode())
                    print("✅ Director added successfully")
                    
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON data"})
                    self.wfile.write(error_response.encode())
                    print("❌ Invalid JSON in director addition request")
                    
            else:
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({"error": "POST endpoint not found"})
                self.wfile.write(error_response.encode())
                print(f"❌ Unknown POST endpoint: {path}")
                
        except (ConnectionAbortedError, BrokenPipeError):
            print("🔌 Client disconnected during POST")
            return
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({"error": str(e)})
                self.wfile.write(error_response.encode())
                print(f"💥 POST Error: {e}")
            except (ConnectionAbortedError, BrokenPipeError):
                print("🔌 Client disconnected during error response")
                return

def run_server():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MockBackendHandler)
    
    print("🚀 Mock Backend Server starting...")
    print(f"📍 Server running at http://localhost:8080")
    print("📺 Available endpoints:")
    print("   GET http://localhost:8080/api/movie/movies/displayingMovies")
    print("   GET http://localhost:8080/api/movie/movies/comingSoonMovies") 
    print("   GET http://localhost:8080/api/movie/movies/{id}")
    print("   GET http://localhost:8080/api/movie/actors/getActorsByMovieId/{id}")
    print("   GET http://localhost:8080/api/movie/cities/getCitiesByMovieId/{id}")
    print("   GET http://localhost:8080/api/movie/saloons/getSaloonsByCityId/{id}")
    print("   GET http://localhost:8080/api/movie/saloonTimes/getMovieSaloonTimeSaloonAndMovieId/{saloonId}/{movieId}")
    print("   GET http://localhost:8080/api/movie/comments/getCommentsByMovieId/{id}/{page}/{size}")
    print("   GET http://localhost:8080/api/movie/comments/getCountOfComments/{id}")
    print("   POST http://localhost:8080/api/movie/comments/add")
    print("   POST http://localhost:8080/api/movie/comments/delete")
    print("   POST http://localhost:8080/api/movie/payments/sendTicketDetail")
    print("   POST http://localhost:8080/api/user/users/add")
    print("   POST http://localhost:8080/api/user/auth/login")
    print("   GET http://localhost:8080/health")
    print("🎬 Frontend should now work at http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopping...")
        httpd.server_close()
        print("✅ Server stopped")

if __name__ == '__main__':
    run_server()