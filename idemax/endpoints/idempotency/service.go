package idempotency

import (
	"context"
	"encoding/json"
	"errors"
	"time"

	"idemax/utils"
)

var ctx = context.Background()

// StoreIdempotencyKey saves an idempotency key in Redis
func StoreIdempotencyKey(tenantID, key string, data IdempotencyData, ttlSeconds int64) error {
	redisClient := utils.GetRedisClient()

	data.ExpiresAt = time.Now().Unix() + ttlSeconds
	serializedData, _ := json.Marshal(data)

	err := redisClient.Set(ctx, "idempotency:"+key, serializedData, time.Duration(ttlSeconds)*time.Second).Err()
	if err != nil {
		return errors.New("failed to store idempotency key")
	}

	return nil
}

// RetrieveIdempotencyKey fetches an idempotency key from Redis
func RetrieveIdempotencyKey(tenantID, key string) (*IdempotencyData, error) {
	redisClient := utils.GetRedisClient()

	data, err := redisClient.Get(ctx, "idempotency:"+key).Result()
	if err != nil {
		return nil, errors.New("idempotency key not found")
	}

	var idempotencyData IdempotencyData
	json.Unmarshal([]byte(data), &idempotencyData)

	return &idempotencyData, nil
}

// RemoveIdempotencyKey deletes an idempotency key from Redis
func RemoveIdempotencyKey(tenantID, key string) error {
	redisClient := utils.GetRedisClient()

	_, err := redisClient.Del(ctx, "idempotency:"+key).Result()
	if err != nil {
		return errors.New("failed to delete idempotency key")
	}

	return nil
}
