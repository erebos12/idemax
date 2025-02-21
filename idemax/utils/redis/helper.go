package redishelper

import (
	"context"
	"idemax/utils"
)

var ctx = context.Background()

// TenantExists checks if the tenant ID exists in Redis
func TenantExists(tenantID string) bool {
	redisClient := utils.GetRedisClient()

	exists, err := redisClient.Exists(ctx, "tenant:"+tenantID).Result()
	if err != nil || exists == 0 {
		return false
	}
	return true
}

// IdempotencyKeyExists checks if the idempotency key exists in Redis
func IdempotencyKeyExists(key string) bool { 
	redisClient := utils.GetRedisClient()

	exists, err := redisClient.Exists(ctx, "idempotency:"+key).Result()
	if err != nil || exists == 0 {
		return false
	}
	return true
}
