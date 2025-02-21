

# Idemax – For Maximal Idempotency! 🚀

**IdeMax** (Idempotency Key Service) manages idempotency keys in **Redis** to detect and prevent duplicate API requests.  

## **Functionality**  
- **Create** an idempotency key with status and expiration time.  
- **Retrieve** a stored key with status, HTTP status, and response data.  
- **Delete** a key to free up storage.  
- **Error handling** for missing or non-existent keys and tenants.  

## **Use Case**  

If you're building, for instance, a **payment app**, the flow would be:  

1. The client (browser) generates an idempotency key and sends it with the payment request.  
    - You can use Hashing Important Request Data
    - i.e. `Format: SHA-256(payment-amount + recipient + product-name)`
2. Before your payment service proceeds with the request, it asks **Idemax** if this key exists.  
3. Your payment app can then react like this:  
   - **Key does not exist →**  
     - **First, create the idempotency key** in **Idemax**, storing it as *"pending"*.  
     - Then, forward the request for processing.  
   - **Key exists & is completed →** Return the stored response (no duplicate payment).  
   - **Key exists & is still *"pending"*** → Wait or reject (depending on your logic).  
4. After **successful processing**, you update the idempotency service with the final status + response.  

This prevents **duplicate charges**, e.g., if the client resends the request due to a network issue. 🚀


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







