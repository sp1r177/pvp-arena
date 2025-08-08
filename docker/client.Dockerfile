# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci || npm install
COPY . ./
RUN npm run build

# Static stage
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html