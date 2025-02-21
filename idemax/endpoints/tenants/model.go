package tenants

// TenantData represents tenant metadata
type TenantData struct {
	TenantID  string `json:"tenant_id"`
	Name      string `json:"name"`
	CreatedAt int64  `json:"created_at"`
}
