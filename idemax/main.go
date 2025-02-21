package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()

// TenantData represents tenant metadata
type TenantData struct {
	TenantID   string `json:"tenant_id"`
	Name       string `json:"name"`
	CreatedAt  int64  `json:"created_at"`
}

// IdempotencyData represents the stored data
type IdempotencyData struct {
	Status     string          `json:"status"`
	HTTPStatus int             `json:"http_status"`
	Response   json.RawMessage `json:"response"`
	ExpiresAt  int64           `json:"expires_at"`
}

func main() {
	// Initialize Gin router
	r := gin.Default()
	r.POST("/tenants", createTenant)
	r.POST("/idempotencies", setIdempotencyKey)
	r.GET("/idempotencies/:key", getIdempotencyKey)
	r.DELETE("/idempotencies/:key", deleteIdempotencyKey)

	log.Println("Idempotency service running on :8080")
	r.Run(":8080")
}

func getRedisClient(tenantID string) *redis.Client {
	redisClient := redis.NewClient(&redis.Options{
		Addr: "localhost:6379", // Change for production
		DB:   getTenantDB(tenantID),
	})
	return redisClient
}

func getTenantDB(tenantID string) int {
	redisClient := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
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
		Addr: "localhost:6379",
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
		Addr: "localhost:6379",
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
	var data IdempotencyData
	if err := c.ShouldBindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
		return
	}

	tenantID := c.GetHeader("X-Tenant-ID")
	if tenantID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Missing tenant ID"})
		return
	}

	redisClient := getRedisClient(tenantID)
	key := c.PostForm("idempotency_key")
	if key == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Missing idempotency_key"})
		return
	}

	data.ExpiresAt = time.Now().Unix() + int64(c.PostForm("ttl_seconds"))
	serializedData, _ := json.Marshal(data)
	err := redisClient.Set(ctx, "idempotency:"+key, serializedData, time.Duration(data.ExpiresAt)*time.Second).Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to store idempotency key"})
		return
	}

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

