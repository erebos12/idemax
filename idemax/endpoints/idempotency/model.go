package idempotency

import "encoding/json"

// IdempotencyData represents the stored idempotency information
type IdempotencyData struct {
	Status     string          `json:"status"`
	HTTPStatus int             `json:"http_status"`
	Response   json.RawMessage `json:"response"`
	ExpiresAt  int64           `json:"expires_at"`
}

// IdempotencyRequest represents the request body for storing an idempotency key
type IdempotencyRequest struct {
	TenantID       string          `json:"tenant_id" binding:"required"`
	IdempotencyKey string          `json:"idempotency_key" binding:"required"`
	TTLSeconds     int64           `json:"ttl_seconds" binding:"required"`
	Status         string          `json:"status"`
	HTTPStatus     int             `json:"http_status"`
	Response       json.RawMessage `json:"response"`
}
