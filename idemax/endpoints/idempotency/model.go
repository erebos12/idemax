package idempotency

import "encoding/json"

// IdempotencyData represents the stored idempotency information
type IdempotencyData struct {
	Status     string          `json:"status"`
	HTTPStatus int             `json:"http_status"`
	Response   json.RawMessage `json:"response"`
	ExpiresAt  int64           `json:"expires_at"`
}
