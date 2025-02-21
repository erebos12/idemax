package tenants

import (
	"context"
	"encoding/json"
	"errors"

	"idemax/utils"
)

var ctx = context.Background()

func SaveTenant(tenant TenantData) error { 
	redisClient := utils.GetRedisClient()

	serializedData, _ := json.Marshal(tenant)
	err := redisClient.Set(ctx, "tenant:"+tenant.TenantID, serializedData, 0).Err()
	if err != nil {
		return errors.New("failed to store tenant")
	}

	return nil
}
