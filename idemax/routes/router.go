package routes

import (
	"github.com/gin-gonic/gin"
	"idemax/endpoints/tenants"
	"idemax/endpoints/idempotency"
	"idemax/endpoints/health"
)

// SetupRouter registers all routes
func SetupRouter(r *gin.Engine) {
	// Tenant Endpoints
	r.POST("/tenants", tenants.CreateTenant)

	// Idempotency Endpoints
	r.POST("/idempotencies", idempotency.SetIdempotencyKey)
	r.GET("/idempotencies/:tenant_id/:idempotency_key", idempotency.GetIdempotencyKey)
	r.DELETE("/idempotencies/:tenant_id/:idempotency_key", idempotency.DeleteIdempotencyKey)

	// Health Check
	r.GET("/health-check", health.HealthCheck)
}
