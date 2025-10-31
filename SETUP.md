# CineVision Microservice - Setup Guide

## Yêu cầu hệ thống

### Bắt buộc phải có:
- **Docker Desktop** (Windows/Mac) hoặc **Docker + Docker Compose** (Linux)
- **Git**
- **Java 17** (JDK, không phải JRE)
- **Maven 3.6+**
- **Node.js 18+** và **npm**

### Kiểm tra version:
```bash
docker --version          # >= 20.0
docker-compose --version  # >= 2.0
java --version            # = 17.x.x
mvn --version            # >= 3.6
node --version           # >= 18.0
npm --version            # >= 8.0
```

## Cách setup nhanh

### 1. Clone repository
```bash
git clone https://github.com/linhne14/CineVisionMicroserviceProject.git
cd CineVisionMicroserviceProject
```

### 2. Chạy setup script (Windows)
```bash
.\quick-setup.ps1
```

### 3. Hoặc setup thủ công:

#### Bước 1: Cài đặt dependencies cho frontend
```bash
cd frontend
npm install
cd ..
```

#### Bước 2: Build Java services
```bash
# Set JAVA_HOME (Windows)
$Env:JAVA_HOME="C:\Program Files\Java\jdk-17"

# Hoặc (Linux/Mac)
export JAVA_HOME="/path/to/java-17"

# Build all services
mvn clean package -DskipTests
```

#### Bước 3: Khởi động infrastructure
```bash
# Start databases first
docker-compose up -d postgres mongodb redis kafka zookeeper zipkin

# Wait 30 seconds for databases to be ready
# Then start services
docker-compose up eureka-server api-gateway movie-service user-service email-service frontend
```

## Truy cập ứng dụng

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8080
- **Eureka Server**: http://localhost:8761
- **Movie Service**: http://localhost:8082
- **User Service**: http://localhost:8081  
- **Email Service**: http://localhost:8083

## Troubleshooting

### Lỗi thường gặp:

#### 1. "mvn command not found"
```bash
# Windows: Download Maven và add vào PATH
# Hoặc dùng Maven wrapper
./mvnw clean package -DskipTests
```

#### 2. "java.lang.UnsupportedClassVersionError"
```bash
# Check Java version
java --version

# Phải dùng Java 17, không phải 8 hoặc 11
```

#### 3. "Port already in use"
```bash
# Stop existing containers
docker-compose down

# Kill processes using ports
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

#### 4. "Connection refused" to database
```bash
# Restart databases
docker-compose restart postgres mongodb

# Check logs
docker-compose logs postgres
docker-compose logs mongodb
```

#### 5. Frontend build fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Reset environment hoàn toàn:
```bash
# Stop all containers
docker-compose down -v

# Remove all images
docker system prune -a

# Restart
.\quick-setup.ps1
```

## Development

### Chạy services riêng lẻ:
```bash
# Only databases
docker-compose up -d postgres mongodb redis

# Run Java service locally
cd movieService
mvn spring-boot:run -Dspring-boot.run.profiles=local

# Run frontend locally  
cd frontend
npm start
```

### Hot reload:
- Frontend: `npm start` (port 3001)
- Java services: Use IntelliJ IDEA với Spring Boot DevTools

## Database Data

Project đã có sẵn:
- **PostgreSQL**: 8 movies với đầy đủ thông tin
- **MongoDB**: User collection ready
- **Flyway migrations**: Auto-run khi start

## Liên hệ

Nếu vẫn gặp lỗi, gửi error logs và thông tin system:
```bash
# Get system info
docker --version
java --version
mvn --version
node --version

# Get error logs
docker-compose logs [service-name]
```