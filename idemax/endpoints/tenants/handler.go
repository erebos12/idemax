package tenants

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// CreateTenant handles storing a new tenant
func CreateTenant(c *gin.Context) {
	var tenant TenantData 
	if err := c.ShouldBindJSON(&tenant); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
		return
	}

	tenant.CreatedAt = time.Now().Unix()
	if err := SaveTenant(tenant); err != nil { // ✅ Call SaveTenant directly
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create tenant"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Tenant created successfully", "tenant": tenant})
}
