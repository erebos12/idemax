

# Idemax – For Maximal Idempotency! 🚀

Idemax is a lightweight CRUD service for managing idempotency keys, backed by Redis.  
It ensures that API requests are processed only once, preventing duplicate operations in distributed systems.  

## Features  
- **Idempotency key storage** with expiration support  
- **Multi-tenant support** with dynamic Redis database assignment  
- **REST API** with CRUD operations  
- **Health-check endpoint** for easy monitoring  

---

## 🔧 Getting Started  

### Clone and Set Up  
```sh
git clone git@github.com:erebos12/idemax.git
cd idemax
```

### Build & Run the Service  
```sh
make start  # Build and runs the Go binary and REDIS
```

### Run Automated API Tests  
```sh
make it  # Executes BDD API tests
```
---







