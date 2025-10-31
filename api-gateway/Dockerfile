# Multi-stage build for Spring Boot API Gateway
FROM eclipse-temurin:17-jdk-alpine AS build

# Install Maven
RUN apk add --no-cache maven

WORKDIR /app

# Copy parent pom first 
COPY pom.xml ../pom.xml

# Copy pom.xml for dependency caching
COPY api-gateway/pom.xml ./

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source and build
COPY api-gateway/src ./src
RUN mvn clean package -DskipTests

# Production stage
FROM eclipse-temurin:17-jre-alpine AS production

# Create app user
RUN addgroup --system spring && adduser --system spring --ingroup spring

WORKDIR /app

# Copy jar file
COPY --from=build /app/target/*.jar app.jar

# Change ownership
RUN chown spring:spring /app/app.jar

USER spring

# Labels
LABEL maintainer="cinevision-team" \
      version="1.0.0" \
      description="CineVision API Gateway" \
      org.opencontainers.image.source="https://github.com/linhne14/CineVisionMicroserviceProject"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# JVM options for gateway
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]