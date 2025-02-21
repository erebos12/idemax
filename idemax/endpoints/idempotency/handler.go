package idempotency

import (
	"encoding/json"
	"net/http"
	"time"
	"idemax/utils"

	"github.com/gin-gonic/gin"
)

// SetIdempotencyKey handles storing a new idempotency key
func SetIdempotencyKey(c *gin.Context) {
	var request struct {
		TenantID       string          `json:"tenant_id" binding:"required"`
		IdempotencyKey string          `json:"idempotency_key" binding:"required"`
		TTLSeconds     int64           `json:"ttl_seconds" binding:"required"`
		Status         string          `json:"status"`
		HTTPStatus     int             `json:"http_status"`
		Response       json.RawMessage `json:"response"`
	}

	// Parse JSON body
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload", "details": err.Error()})
		return
	}

	// Calculate expiration time
	expiresAt := time.Now().Unix() + request.TTLSeconds

	// Prepare data to be stored in Redis
	data := IdempotencyData{
		Status:     request.Status,
		HTTPStatus: request.HTTPStatus,
		Response:   request.Response,
		ExpiresAt:  expiresAt,
	}

	// Store idempotency key in Redis
	err := StoreIdempotencyKey(request.TenantID, request.IdempotencyKey, data, request.TTLSeconds)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to store idempotency key"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Idempotency key stored"})
}

// GetIdempotencyKey handles retrieving an existing idempotency key
func GetIdempotencyKey(c *gin.Context) {
	tenantID := c.Param("tenant_id")
	key := c.Param("idempotency_key")

	// Check if tenant ID exists in Redis
	if !TenantExists(tenantID) {
		c.JSON(http.StatusNotFound, gin.H{"error": "Tenant not found"})
		return
	}

	// Retrieve the idempotency key
	idempotencyData, err := RetrieveIdempotencyKey(tenantID, key)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Idempotency key not found"})
		return
	}

	c.JSON(http.StatusOK, idempotencyData)
}


func DeleteIdempotencyKey(c *gin.Context) {
	tenantID := c.Param("tenant_id")
	key := c.Param("idempotency_key")

	// Check if tenant ID exists in Redis
	if !TenantExists(tenantID) {
		c.JSON(http.StatusNotFound, gin.H{"error": "Tenant not found"})
		return
	}

	// Attempt to delete the idempotency key
	err := RemoveIdempotencyKey(tenantID, key)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete idempotency key"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Idempotency key deleted"})
}

func TenantExists(tenantID string) bool {
	redisClient := utils.GetRedisClient()

	// Check if the tenant key exists in Redis
	exists, err := redisClient.Exists(ctx, "tenant:"+tenantID).Result()
	if err != nil || exists == 0 {
		return false
	}
	return true
}
