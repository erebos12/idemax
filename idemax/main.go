package main

import (
	"log"

	"idemax/routes"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	routes.SetupRouter(r)

	log.Println("Idempotency service running on :8080")
	r.Run(":8080")
}
