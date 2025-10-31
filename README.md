# 🎬 CineVision Microservice Project

Modern sinema bileti satış uygulaması - Spring Boot mikroservis mimarisi ile geliştirilmiş, React.js frontend'e sahip tam kapsamlı bir sistem.

## ✨ Özellikler

- **🏗️ Mikroservis Mimarisi**: Bağımsız, ölçeklenebilir servisler
- **🔍 Service Discovery**: Eureka Server ile otomatik hizmet keşfi  
- **🚪 API Gateway**: Merkezi routing ve load balancing
- **🗄️ Çoklu Veritabanı**: PostgreSQL + MongoDB + Redis
- **📬 Message Queue**: Kafka ile asenkron iletişim
- **📊 Monitoring**: Zipkin distributed tracing
- **⚛️ Modern Frontend**: React.js + Redux + Material-UI
- **🐳 Containerization**: Docker + Docker Compose
- **🔧 Production Ready**: Health checks, connection pooling, migrations

## 🏆 Mikroservisler

| Servis | Port | Teknoloji | Açıklama |
|--------|------|-----------|----------|
| **Eureka Server** | 8761 | Spring Cloud | Service Discovery |
| **API Gateway** | 8080 | Spring Cloud Gateway | Routing & Load Balancing |
| **Movie Service** | 8082 | Spring Boot + PostgreSQL | Film yönetimi & rezervasyon |
| **User Service** | 8081 | Spring Boot + MongoDB | Kullanıcı yönetimi & auth |
| **Email Service** | 8083 | Spring Boot + Kafka | Email bildirimleri |
| **Frontend** | 3000 | React.js | Kullanıcı arayüzü |

## 🚀 Hızlı Başlangıç

### 📋 Gereksinimler
- **Docker Desktop** (Windows/Mac) veya **Docker + Docker Compose** (Linux)
- **Java 17 JDK**
- **Maven 3.6+** 
- **Node.js 18+**

### ⚡ Tek Komutla Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/linhne14/CineVisionMicroserviceProject.git
cd CineVisionMicroserviceProject

# Otomatik setup (Windows)
.\quick-setup.ps1

# Manuel kurulum için SETUP.md dosyasına bakın
```

### 🌐 Erişim Adresleri

| Servis | URL | Açıklama |
|--------|-----|----------|
| **Frontend** | http://localhost:3000 | Ana uygulama |
| **API Gateway** | http://localhost:8080 | API endpoint |
| **Eureka Dashboard** | http://localhost:8761 | Service registry |
| **Zipkin Tracing** | http://localhost:9411 | Distributed tracing |

## 📊 Database

### PostgreSQL (Movie Service)
- **8 adet örnek film** verisi
- **Flyway migrations** ile otomatik schema
- **HikariCP connection pooling**

### MongoDB (User Service)  
- User collection hazır
- Otomatik bağlantı yapılandırması

## 🛠️ Geliştirme

### Lokal Geliştirme
```bash
# Sadece veritabanlarını başlat
docker-compose up -d postgres mongodb redis

# Java servisini lokal çalıştır
cd movieService
mvn spring-boot:run -Dspring-boot.run.profiles=local

# Frontend'i geliştirme modunda çalıştır
cd frontend  
npm start
```

### Docker Build
```bash
# Tek servis build
docker-compose build movie-service

# Tüm Java servislerini build
docker-compose build eureka-server api-gateway movie-service user-service email-service
```

## 🔧 Troubleshooting

Problem yaşıyorsanız:

```bash
# Troubleshooting tool'u çalıştır
.\troubleshoot.ps1

# Veya manuel reset
docker-compose down -v
docker system prune -a
.\quick-setup.ps1
```

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| **[QUICK-START.md](QUICK-START.md)** | 🚀 Hızlı başlangıç - clone sonrası ilk çalıştırma |
| **[SETUP.md](SETUP.md)** | 📋 Detaylı kurulum rehberi ve gereksinimler |
| **[troubleshoot.ps1](troubleshoot.ps1)** | 🔧 Otomatik problem çözme aracı |
| **[quick-setup.ps1](quick-setup.ps1)** | ⚡ Tek tıkla kurulum scripti |

**Yaygın problemler için yukarıdaki dokümanlara bakın**
However, People must create an account to comments on movies. Only admins
can add movie,actor or director to the system. This authorization process is controlled
with Jwt token.

## Technologies Of Project
There are many technologies in this project. These are:
<h5> Backend Techologies </h5>
<ul>
    <li>Java 17</li>
    <li>Spring Boot 2.7.0 </li>
    <li>Spring Cloud</li>
    <li>Spring Data Jpa</li>
    <li>Spring Security</li>
    <li>Lombok</li>
    <li>WebClient</li>
    <li>Apache Kafka</li>
    <li>Jwt</li>
    <li>Java Mail Sender</li>
    <li>Zipkin</li>
    <li>Resilience4j</li>
    <li>PostgreSql</li>
    <li>MongoDB</li>
    <li>Redis</li>
    <li>Docker</li>
</ul>
<h5> Frontend Techologies </h5>
<ul>
    <li>JavaScript</li>
    <li>React</li>
    <li>Bootstrap</li>
    <li>Redux</li>
</ul>

## Usage Of Technologies In Project
There are 5 services in this project and each service 
are written with N-layered architecture. Spring Cloud
used for microservice infrastructure.
Netflix Eureka Server used to create eureka server. This 
eureka server contains movie service, user service and email service
eureka clients and api-gateway service. In addition,
Zipkin and Sleuth were used to monitor cross-service logs. Also,
Resilience4j used as Circuit Breaker.
<br>
<br>
In the Api Gateway, Spring Cloud Gateway was used for managing
requests.
<br>
<br>
In the Eureka Server, Netflix Eureka Server was used. And Spring
Security was used to secure eureka server.
<br>
<br>
WebFlux was used for communication between Movie and User Services.
And, Apache Kafka was used for asynchronous communication
between Movie and Email Services.
<br>
<br>
In the User Service, MongoDB used as database. Spring Security
was used for encrypting user's passwords and generating Jwt token.
<br>
<br>
In the Movie Service, PostgreSql used as database and Spring Data Jpa
was used. Webflux and Apache Kafka was used for communication with other services.
Resilience4J Circuit Breaker was used here. Displaying and coming soon movies
are cached using with Redis.
<br>
<br>
In the Email Service, Apache Kafka was used for receiving the 
message from Movie Service. Java Mail Sender and FreeMarker template 
was used for creating email template and sending email.
<br>
<br>
PostgreSql, MongoDB, Apache Kafka and Zipkin run as Docker container
in the docker-compose.yml file.

On the Frontend side, JavaScript and React was used. Also,
Axios was preferred to send request to the backend. For state management,
Redux was used. For, design of the UI, Bootstrap and Css are used.

## Architectural Design
<p align="center">
    <img src="architectural_design.jpeg" />
</p>

## How can I use the Project ?
Download the source code of project. Open this project with your 
favorite IDE. Make sure Java 17, Node.js and Docker are installed on
your computer. And, follow these steps:

<ol>
    <h3> <li>Run docker-compose.yml file</li> </h3>
<p>
This docker compose file is necessary to run postgre, mongo, 
kafka etc. Open cmd in the project directory and type

    docker compose up -d

command to run the containers.
</p>

 <h3> <li>Run Eureka Server</li> </h3>
<p>
    Go to EurekaServerApplication class which is in eureka-server module
and run this class to create eureka server. If you want to display
eureka server panel, you can go to <b>localhost:8080/eureka/web </b> or
<b>localhost:8761</b> addresses. Then, enter username= <b>eureka</b> and 
password= <b>password</b>.

</p>

 <h3> <li>Run Api Gateway</li> </h3>
<p>
   To forward the requests to the relevant services, Gateway must be 
run. Go to ApiGatewayApplication class which is in api-gateway modules
and run this class. If you want to check that the api-gateway is registered 
to the eureka server, you can display the eureka server panel.
</p>

 <h3> <li>Run Movie Service</li> </h3>
<p> 
To run movie service go to movie service module. And, run 
MovieServiceApplication class.
</p>

<h3> <li>Run User Service</li> </h3>
<p> 
In the user service module, find UserServiceApplication class and run this
class.
</p>

<h3> <li>Run Email Service</li> </h3>
<p> 
EmailServiceApplication class is in email service module. To run email service module,
run this class.
</p>

<h3> <li>Run Email Service</li> </h3>
<p> 
EmailServiceApplication class is in email service module. To run email service module,
run this class. If this module is started successfully, you can view 
all running services in the eureka server using with eureka panel which is
running on localhost:8761 or localhost:8080/eureka/web.
</p>
<h5>Important Note: <br>
Change mail configurations in application.yml file with your own configurations.
</h5>

<h3> <li>Start React (Frontend) Application</li> </h3>
<p> 
Go to frontend package which is the location of frontend code.
Firstly, type

    npm install

command in cmd for downloading package.json dependencies. Then, To start
the React app, type

    npm start

command. After that, npm will start your React Application
on <b> localhost:3000 </b>.

</p>


</ol>


## Project UI

https://user-images.githubusercontent.com/79381882/194945895-f7e2d2d2-4899-4ade-8c79-ecb647949ffd.mp4

<h4>Main Page</h4>

<img src="homa_page.jpg">

[For more UI Images](https://github.com/VonHumbolt/CineVisionMicroserviceProject/tree/main/frontend)
