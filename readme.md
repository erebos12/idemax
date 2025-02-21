

# Idemax – For Maximal Idempotency! 🚀

**IdeMax** (Idempotency Key Service) manages idempotency keys in **Redis** to detect and prevent duplicate API requests.  

## **Functionality**  
- **Create** an idempotency key with status and expiration time.  
- **Retrieve** a stored key with status, HTTP status, and response data.  
- **Delete** a key to free up storage.  
- **Error handling** for missing or non-existent keys and tenants.  

## **Use Case**  
The service ensures that repeated API requests (e.g., due to network failures or duplicate user actions) are not processed multiple times. Ideal for **payments, order processing, or external API integrations**. 🚀


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







