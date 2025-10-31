# Multi-stage build for React frontend
FROM node:18-alpine AS build

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Set working directory
WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install dependencies (production only for smaller image)
RUN npm ci --only=production && npm cache clean --force

# Install dev dependencies for build
RUN npm ci

# Copy source code
COPY . .

# Build the app with optimization
RUN npm run build && \
    # Remove source maps for production
    find build -name "*.map" -delete

# Production stage - minimal nginx image
FROM nginx:1.25-alpine AS production

# Install curl for health checks and remove cache
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# Create nginx user
RUN adduser -D -S -h /var/cache/nginx -s /sbin/nologin -G nginx nginx

# Copy optimized nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build files from build stage with proper ownership
COPY --from=build --chown=nginx:nginx /app/build /usr/share/nginx/html

# Remove default nginx files to reduce size
RUN rm -rf /usr/share/nginx/html/index.html

# Add labels for better container management
LABEL maintainer="cinevision-team" \
      version="1.0.0" \
      description="CineVision React Frontend" \
      org.opencontainers.image.source="https://github.com/linhne14/CineVisionMicroserviceProject"

# Use non-root user for security
USER nginx

# Expose port
EXPOSE 80

# Health check with better performance
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Use dumb-init for proper signal handling
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["nginx", "-g", "daemon off;"]