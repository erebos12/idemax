package utils

import (
	"os"

	"github.com/redis/go-redis/v9"
)

func GetRedisClient() *redis.Client {
	addr := os.Getenv("REDIS_HOST")
	if addr == "" {
		addr = "localhost:6379"
	}

	return redis.NewClient(&redis.Options{
		Addr: addr,
		DB:   0,
	})
}
