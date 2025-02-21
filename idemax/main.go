package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()

// TenantData represents tenant metadata
type TenantData struct {
	TenantID  string `json:"tenant_id"`
	Name      string `json:"name"`
	CreatedAt int64  `json:"created_at"`
}

// IdempotencyData represents the stored data
type IdempotencyData struct {
	Status     string          `json:"status"`
	HTTPStatus int             `json:"http_status"`
	Response   json.RawMessage `json:"response"`
	ExpiresAt  int64           `json:"expires_at"`
}

func getRedisAddr() string {
	addr := os.Getenv("REDIS_HOST")
	if addr == "" {
		addr = "localhost:6379" // Default fallback
	}
	return addr
}

func main() {
	// Initialize Gin router
	r := gin.Default()
	r.POST("/tenants", createTenant)
	r.POST("/idempotencies", setIdempotencyKey)
	r.GET("/idempotencies/:key", getIdempotencyKey)
	r.DELETE("/idempotencies/:key", deleteIdempotencyKey)
	r.GET("/health-check", healthCheck) // Added health-check route

	log.Println("Idempotency service running on :8080")
	r.Run(":8080")
}

func getRedisClient(tenantID string) *redis.Client {
	redisClient := redis.NewClient(&redis.Options{
		Addr: getRedisAddr(),
		DB:   getTenantDB(tenantID),
	})
	return redisClient
}

func getTenantDB(tenantID string) int {
	redisClient := redis.NewClient(&redis.Options{
		Addr: getRedisAddr(),
		DB:   0,
	})
	dbNum, err := redisClient.Get(ctx, "tenant_db:"+tenantID).Int()
	if err == redis.Nil {
		dbNum = len(getAllTenantIDs())
		redisClient.Set(ctx, "tenant_db:"+tenantID, dbNum, 0)
	}
	return dbNum
}

func getAllTenantIDs() []string {
	redisClient := redis.NewClient(&redis.Options{
		Addr: getRedisAddr(),
		DB:   0,
	})
	keys, _ := redisClient.Keys(ctx, "tenant_db:*").Result()
	return keys
}

func createTenant(c *gin.Context) {
	var tenant TenantData
	if err := c.ShouldBindJSON(&tenant); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
		return
	}

	tenant.CreatedAt = time.Now().Unix()
	dbNum := getTenantDB(tenant.TenantID)
	redisClient := redis.NewClient(&redis.Options{
		Addr: getRedisAddr(),
		DB:   dbNum,
	})

	tenantKey := "tenant:" + tenant.TenantID
	serializedData, _ := json.Marshal(tenant)
	err := redisClient.Set(ctx, tenantKey, serializedData, 0).Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create tenant"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Tenant created successfully", "tenant": tenant})
}

func setIdempotencyKey(c *gin.Context) {
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

	// Initialize Redis client for the given tenant
	redisClient := getRedisClient(request.TenantID)

	// Calculate expiration time
	expiresAt := time.Now().Unix() + request.TTLSeconds

	// Prepare data to be stored in Redis
	data := IdempotencyData{
		Status:     request.Status,
		HTTPStatus: request.HTTPStatus,
		Response:   request.Response,
		ExpiresAt:  expiresAt,
	}

	// Serialize the data
	serializedData, _ := json.Marshal(data)

	// Store in Redis with TTL
	err := redisClient.Set(ctx, "idempotency:"+request.IdempotencyKey, serializedData, time.Duration(request.TTLSeconds)*time.Second).Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to store idempotency key"})
		return
	}

	// Success response
	c.JSON(http.StatusCreated, gin.H{"message": "Idempotency key stored"})
}


func getIdempotencyKey(c *gin.Context) {
	tenantID := c.GetHeader("X-Tenant-ID")
	if tenantID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Missing tenant ID"})
		return
	}

	redisClient := getRedisClient(tenantID)
	key := c.Param("key")
	data, err := redisClient.Get(ctx, "idempotency:"+key).Result()
	if err == redis.Nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Idempotency key not found"})
		return
	} else if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error retrieving data"})
		return
	}

	var idempotencyData IdempotencyData
	json.Unmarshal([]byte(data), &idempotencyData)
	c.JSON(http.StatusOK, idempotencyData)
}

func deleteIdempotencyKey(c *gin.Context) {
	tenantID := c.GetHeader("X-Tenant-ID")
	if tenantID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Missing tenant ID"})
		return
	}

	redisClient := getRedisClient(tenantID)
	key := c.Param("key")
	err := redisClient.Del(ctx, "idempotency:"+key).Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete idempotency key"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Idempotency key deleted"})
}

// Health-check endpoint
func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "I'm alive"})
}
