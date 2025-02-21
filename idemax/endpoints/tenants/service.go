package tenants

import (
	"errors"
	"time"
)


func CreateNewTenant(tenant TenantData) (TenantData, error) {
	tenant.CreatedAt = time.Now().Unix()

	// Store tenant in Redis
	err := SaveTenant(tenant)
	if err != nil {
		return TenantData{}, errors.New("failed to create tenant")
	}

	return tenant, nil
}
