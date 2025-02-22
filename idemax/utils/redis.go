package utils

import (
	"os"
	
	"sync"

	
	"github.com/redis/go-redis/v9"
)



var (
	redisClient *redis.Client
	once        sync.Once
)

// Initializee Redis-connection only once
func InitRedis() {
	once.Do(func() {
		addr := os.Getenv("REDIS_HOST")
		if addr == "" {
			addr = "localhost:6379"
		}

		redisClient = redis.NewClient(&redis.Options{
			Addr: addr,
			DB:   0,
		})
	})
}

// GetRedisClient returns global instance of redis client
func GetRedisClient() *redis.Client {
	if redisClient == nil {
		InitRedis()
	}
	return redisClient
}

