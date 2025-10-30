#!/usr/bin/env python3
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
        "movieId": 1,
        "movieName": "Avengers: Endgame",
        "description": "The epic conclusion to the Infinity Saga that changed the Marvel Cinematic Universe forever.",
        "releaseDate": "2019-04-26",
        "duration": 181,
        "categoryName": "Action",
        "directorName": "Anthony Russo",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "movieTrailerUrl": "https://www.youtube.com/watch?v=TcMBFSGVi1c"
    },
    {
        "movieId": 2,
        "movieName": "Spider-Man: No Way Home", 
        "description": "Spider-Man's identity is revealed and he asks Doctor Strange for help.",
        "releaseDate": "2021-12-17",
        "duration": 148,
        "categoryName": "Action",
        "directorName": "Jon Watts",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "movieTrailerUrl": "https://www.youtube.com/watch?v=JfVOs4VSpmA"
    },
    {
        "movieId": 3,
        "movieName": "The Batman",
        "description": "Batman ventures into Gotham City's underworld when a sadistic killer leaves behind a trail of cryptic clues.",
        "releaseDate": "2022-03-04",
        "duration": 176,
        "categoryName": "Action",
        "directorName": "Matt Reeves",
        "movieImageUrl": "https://image.tmdb.org/t/p/w500/b0PlSFdDwbyK0cf5RxwDpaOJQvQ.jpg",
        "movieTrailerUrl": "https://www.youtube.com/watch?v=mqqft2x_Aa4"
    }
]

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse URL
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/movie/movies/displayingMovies':
                try:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(MOCK_MOVIES)
                    self.wfile.write(response.encode())
                    print("✅ Served displaying movies")
                except (ConnectionAbortedError, BrokenPipeError):
                    print("🔌 Client disconnected during response")
                    return
                
            elif path == '/api/movie/movies/comingSoonMovies':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                # Return only first movie for coming soon
                response = json.dumps(MOCK_MOVIES[:1])
                self.wfile.write(response.encode())
                print("✅ Served coming soon movies")
                
            elif path.startswith('/api/movie/movies/'):
                # Get specific movie by ID
                movie_id_str = path.split('/')[-1]
                
                # Handle undefined case
                if movie_id_str == 'undefined' or not movie_id_str.isdigit():
                    # Return first movie as default
                    movie = MOCK_MOVIES[0] if MOCK_MOVIES else None
                    movie_id = movie['movieId'] if movie else 1
                else:
                    movie_id = int(movie_id_str)
                    movie = next((m for m in MOCK_MOVIES if m['movieId'] == movie_id), None)
                
                if movie:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps(movie)
                    self.wfile.write(response.encode())
                    print(f"✅ Served movie ID: {movie_id} (requested: {movie_id_str})")
                else:
                    self.send_response(404)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"error": "Movie not found"}')
                    print(f"❌ Movie not found: {movie_id} (requested: {movie_id_str})")
                    
            elif path.startswith('/api/movie/actors/getActorsByMovieId/'):
                # Get actors by movie ID - mock actors data
                movie_id_str = path.split('/')[-1]
                mock_actors = [
                    {"firstName": "Robert", "lastName": "Downey Jr."},
                    {"firstName": "Chris", "lastName": "Evans"},
                    {"firstName": "Scarlett", "lastName": "Johansson"}
                ]
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_actors)
                self.wfile.write(response.encode())
                print(f"✅ Served actors for movie: {movie_id_str}")
                
            elif path.startswith('/api/movie/cities/getCitiesByMovieId/'):
                # Get cities by movie ID - mock cities data
                mock_cities = [
                    {"cityId": 1, "cityName": "Ho Chi Minh City"},
                    {"cityId": 2, "cityName": "Ha Noi"},
                    {"cityId": 3, "cityName": "Da Nang"}
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_cities)
                self.wfile.write(response.encode())
                print("✅ Served cities")
                
            elif path.startswith('/api/movie/saloons/getSaloonsByCityId/'):
                # Get saloons by city ID - mock saloons data
                mock_saloons = [
                    {
                        "saloonId": 1,
                        "saloonName": "CGV Vincom Center",
                        "cityId": 1
                    },
                    {
                        "saloonId": 2, 
                        "saloonName": "Galaxy Cinema",
                        "cityId": 1
                    },
                    {
                        "saloonId": 3,
                        "saloonName": "Lotte Cinema",
                        "cityId": 1
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloons)
                self.wfile.write(response.encode())
                print("✅ Served saloons")
            
            elif path == '/api/movie/saloons/getall':
                # Get all saloons
                mock_saloons = [
                    {"saloonId": 1, "saloonName": "CGV Vincom Center", "cityId": 1},
                    {"saloonId": 2, "saloonName": "Galaxy Cinema", "cityId": 1},
                    {"saloonId": 3, "saloonName": "Lotte Cinema", "cityId": 1},
                    {"saloonId": 4, "saloonName": "CGV Landmark", "cityId": 2},
                    {"saloonId": 5, "saloonName": "BHD Star Cinema", "cityId": 2}
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
                    {"cityId": 1, "cityName": "Ho Chi Minh City"},
                    {"cityId": 2, "cityName": "Ha Noi"}, 
                    {"cityId": 3, "cityName": "Da Nang"},
                    {"cityId": 4, "cityName": "Can Tho"},
                    {"cityId": 5, "cityName": "Hai Phong"}
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
                        "content": "Great movie! Highly recommend.",
                        "user": {"name": "John Doe"},
                        "createdAt": "2023-10-01"
                    },
                    {
                        "id": 2,
                        "content": "Amazing visual effects and storyline.",
                        "user": {"name": "Jane Smith"},
                        "createdAt": "2023-10-02"
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
                        "saloonName": "Saloon A",
                        "movieId": 1
                    },
                    {
                        "id": 2,
                        "movieBeginTime": "17:30",
                        "movieDate": "2025-10-30", 
                        "saloonName": "Saloon B",
                        "movieId": 1
                    },
                    {
                        "id": 3,
                        "movieBeginTime": "20:00",
                        "movieDate": "2025-10-30",
                        "saloonName": "Saloon A", 
                        "movieId": 1
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloon_times)
                self.wfile.write(response.encode())
                print("✅ Served saloon times")
            
            elif path.startswith('/api/movie/saloonTimes/getMovieSaloonTimeSaloonAndMovieId/'):
                # Get movie saloon times by saloon ID and movie ID - return array
                mock_saloon_times = [
                    {
                        "id": 1,
                        "movieBeginTime": "14:00",
                        "movieDate": "2025-10-30",
                        "saloonName": "CGV Vincom Center",
                        "movieId": 1,
                        "saloonId": 1
                    },
                    {
                        "id": 2,
                        "movieBeginTime": "17:30",
                        "movieDate": "2025-10-30",
                        "saloonName": "CGV Vincom Center", 
                        "movieId": 1,
                        "saloonId": 1
                    },
                    {
                        "id": 3,
                        "movieBeginTime": "20:00",
                        "movieDate": "2025-10-30",
                        "saloonName": "CGV Vincom Center",
                        "movieId": 1,
                        "saloonId": 1
                    }
                ]
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(mock_saloon_times)
                self.wfile.write(response.encode())
                print("✅ Served specific saloon times")
                    
            elif path == '/health':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"status": "OK", "message": "Mock Backend is running"})
                self.wfile.write(response.encode())
                print("✅ Health check")
                
            else:
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Endpoint not found"}')
                print(f"❌ Unknown endpoint: {path}")
                
        except ConnectionAbortedError:
            # Client disconnected, ignore silently
            print("🔌 Client disconnected")
            return
        except BrokenPipeError:
            # Broken pipe, ignore silently  
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
                        "message": "Ticket booked successfully!",
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
    print("   GET http://localhost:8080/health")
    print("🎬 Frontend should now work at http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopping...")
        httpd.server_close()
        print("✅ Server stopped")

if __name__ == "__main__":
    run_server()