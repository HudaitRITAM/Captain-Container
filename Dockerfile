# ─────────────────────────────────────────────
#  Dockerfile – my-api
#  Stack : Node.js
# ─────────────────────────────────────────────

FROM node:20-alpine AS builder
WORKDIR /build

# Install dependencies first (layer caching)
COPY package*.json ./
RUN npm ci
COPY . .

# ── Runtime image (smaller) ─────────────
FROM node:20-alpine
WORKDIR /app

COPY --from=builder /build/node_modules ./node_modules
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/package.json ./

# Run as non-root for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Environment variables
ENV NODE_ENV=production
ENV LOG_LEVEL=info

EXPOSE 3000

CMD ["npm", "start"]
