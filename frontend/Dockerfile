# Build the Vite application
FROM node:24.18.0-alpine3.23 AS builder

ARG VITE_GOOGLE_CLIENT_ID
ARG VITE_API_URL
ARG ENV

# Make variables available to Vite during the build
ENV VITE_GOOGLE_CLIENT_ID=${VITE_GOOGLE_CLIENT_ID}
ENV VITE_API_URL=${VITE_API_URL}
ENV ENV=${ENV}

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci

COPY . .

# Build the application
RUN npm run build

# Serve with Nginx
FROM nginx:1.30.4-alpine

# Copy the custom frontend nginx configuration to override the default config
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy the built files
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
