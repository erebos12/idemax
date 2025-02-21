package idempotency

import (
	"net/http"
	"time"
	"idemax/utils/redis" 

	"github.com/gin-gonic/gin"
)

func SetIdempotencyKey(c *gin.Context) {
	var request IdempotencyRequest

	// Parse JSON body
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload", "details": err.Error()})
		return
	}

	if request.TTLSeconds <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid TTL value, must be greater than 0"})
		return
	}

	expiresAt := time.Now().Unix() + request.TTLSeconds

	data := IdempotencyData{
		Status:     request.Status,
		HTTPStatus: request.HTTPStatus,
		Response:   request.Response,
		ExpiresAt:  expiresAt,
	}

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
	if !redishelper.TenantExists(tenantID) {
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

	// Check if the tenant ID exists in Redis
	if !redishelper.TenantExists(tenantID) {
		c.JSON(http.StatusNotFound, gin.H{"error": "Tenant not found"})
		return
	}

	// Check if the idempotency key exists in Redis
	if !redishelper.IdempotencyKeyExists(key) {
		c.JSON(http.StatusNotFound, gin.H{"error": "Idempotency key not found"})
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


