FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod download

COPY . .
RUN go build -o app

FROM alpine
WORKDIR /app

COPY --from=builder /app/app .

EXPOSE 3003

CMD ["./app"]