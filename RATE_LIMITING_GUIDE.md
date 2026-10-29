# 🚦 Rate Limiting Guide

Complete guide to implementing and using rate limiting in the Insurance Claim Processing System.

---

## 📊 What Should Be Rate Limited?

### 1. **LLM API Calls** (Most Critical)
- OpenAI/Azure has rate limits
- Default: 3 requests/minute (free tier)
- Paid: Up to 60+ requests/minute
- Each claim processing = 2-4 LLM calls

### 2. **Vector Store Operations**
- Embedding generation (expensive)
- Semantic search queries
- Document insertions

### 3. **User Submissions**
- Claims per user per hour
- Prevent spam/abuse
- Protect database

### 4. **System Resources**
- Concurrent processing jobs
- Memory usage
- CPU usage

---

## 🔧 Implementation: Rate Limiting Layers

### Layer 1: OpenAI API Rate Limiting (Built-in)

OpenAI handles this automatically:

```python
from src.llm.client import get_llm

llm = get_llm()

# OpenAI automatically:
# ✅ Queues requests
# ✅ Respects rate limits
# ✅ Retries with exponential backoff
# ✅ Returns 429 error if exceeded
```

### Layer 2: Application-Level Rate Limiting

Create file: `src/utils/rate_limiter.py`

```python
"""
Rate limiting for claims processing
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Optional

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        self.requests_per_second = requests_per_minute / 60
        self.tokens = requests_per_minute
        self.last_update = time.time()
        self.lock = Lock()
    
    def acquire(self, tokens: float = 1.0) -> bool:
        """
        Acquire tokens. Returns True if allowed, False if rate limited.
        
        Usage:
            if limiter.acquire():
                # Process claim
            else:
                # Too many requests, wait or reject
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # Add tokens based on elapsed time
            self.tokens = min(
                self.requests_per_minute,
                self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_if_needed(self, tokens: float = 1.0) -> float:
        """
        Wait until tokens available. Returns wait time in seconds.
        
        Usage:
            wait_time = limiter.wait_if_needed()
            if wait_time > 0:
                print(f"Waited {wait_time}s for rate limit")
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            self.tokens = min(
                self.requests_per_minute,
                self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            
            # Calculate wait time
            wait_time = (tokens - self.tokens) / self.requests_per_second
            self.tokens = 0
            return wait_time


class UserRateLimiter:
    """Per-user rate limiting"""
    
    def __init__(self, requests_per_hour: int = 100):
        self.requests_per_hour = requests_per_hour
        self.user_requests = defaultdict(list)
        self.lock = Lock()
    
    def check_limit(self, user_id: str) -> tuple[bool, int]:
        """
        Check if user exceeded limit.
        Returns (allowed, requests_remaining)
        """
        with self.lock:
            now = time.time()
            one_hour_ago = now - 3600
            
            # Remove old requests
            requests = [
                t for t in self.user_requests[user_id]
                if t > one_hour_ago
            ]
            self.user_requests[user_id] = requests
            
            # Check limit
            if len(requests) >= self.requests_per_hour:
                return False, 0
            
            # Add current request
            requests.append(now)
            remaining = self.requests_per_hour - len(requests)
            
            return True, remaining


# Global instances
claim_limiter = RateLimiter(requests_per_minute=20)
user_limiter = UserRateLimiter(requests_per_hour=100)
```

### Layer 3: Workflow Integration

Update `src/orchestration/workflow.py`:

```python
from src.utils.rate_limiter import claim_limiter, user_limiter
import time

def build_workflow():
    """Build workflow with rate limiting"""
    
    def process_claim_with_limit(claim_state):
        """Process claim with rate limiting"""
        
        # Check user limit
        user_id = claim_state.get("user_id", "anonymous")
        allowed, remaining = user_limiter.check_limit(user_id)
        
        if not allowed:
            return {
                **claim_state,
                "error": "Rate limit exceeded. Max 100 claims per hour",
                "decision": "REJECTED"
            }
        
        # Wait for rate limit if needed
        wait_time = claim_limiter.wait_if_needed(tokens=2.0)
        if wait_time > 0:
            print(f"⏳ Rate limit: waiting {wait_time:.2f}s")
            time.sleep(wait_time)
        
        # Process normally
        return claim_state
    
    # Add to workflow
    graph.add_node("rate_limiter", process_claim_with_limit)
    graph.add_edge("rate_limiter", "intake_agent")
    graph.set_entry_point("rate_limiter")
    
    return graph
```

---

## 📊 Current Rate Limits (OpenAI)

### Free Tier
- **Requests**: 3 per minute
- **Tokens**: 40,000 per minute
- **Cost**: $0 (trial)

### Paid Tier
- **Requests**: 60+ per minute
- **Tokens**: 90,000+ per minute  
- **Cost**: $0.0015/1K tokens (input), $0.002/1K (output)

---

## 🎯 How Rate Limiting Works in Your System

### Scenario 1: Normal Usage (Under Limit)

```
User submits claim
    ↓
Check rate limit ✅ (tokens available)
    ↓
Process claim → Call LLM
    ↓
Return decision
    ↓
Consume tokens
```

**Result**: Instant processing ⚡

### Scenario 2: Rate Limited (Over Limit)

```
User submits claim
    ↓
Check rate limit ❌ (no tokens)
    ↓
Wait for tokens (2-3 seconds)
    ↓
Process claim → Call LLM
    ↓
Return decision
    ↓
Consume tokens
```

**Result**: Delayed but processed ⏳

### Scenario 3: Exceeded Limit

```
User submits claim
    ↓
Check user limit ❌ (100 claims/hour exceeded)
    ↓
Reject with error
    ↓
Return: "Rate limit exceeded"
```

**Result**: Rejected with clear message ❌

---

## 🛠️ Usage Examples

### Example 1: Check Before Processing

```python
from src.utils.rate_limiter import claim_limiter

if claim_limiter.acquire():
    # Process claim
    process_claim(claim_data)
else:
    # Rate limited
    print("Too many requests, please try again later")
```

### Example 2: Wait for Rate Limit

```python
from src.utils.rate_limiter import claim_limiter

wait_time = claim_limiter.wait_if_needed()
if wait_time > 0:
    print(f"Waiting {wait_time:.2f}s due to rate limits")
    time.sleep(wait_time)

# Now process
process_claim(claim_data)
```

### Example 3: Per-User Rate Limiting

```python
from src.utils.rate_limiter import user_limiter

user_id = "user_123"
allowed, remaining = user_limiter.check_limit(user_id)

if allowed:
    process_claim(claim_data)
    print(f"Claims remaining this hour: {remaining}")
else:
    print("User limit exceeded (100 per hour)")
```

---

## 📈 Monitoring Rate Limits

Create `src/utils/rate_limit_monitor.py`:

```python
"""
Monitor and log rate limit usage
"""

import json
from datetime import datetime
from src.logger import setup_logger

logger = setup_logger(__name__)

class RateLimitMonitor:
    def __init__(self):
        self.stats = {
            "total_requests": 0,
            "rate_limited_requests": 0,
            "average_wait_time": 0,
            "last_reset": datetime.now().isoformat()
        }
    
    def log_request(self, allowed: bool, wait_time: float = 0):
        """Log a request"""
        self.stats["total_requests"] += 1
        
        if not allowed:
            self.stats["rate_limited_requests"] += 1
        
        if wait_time > 0:
            avg = self.stats["average_wait_time"]
            total = self.stats["rate_limited_requests"]
            self.stats["average_wait_time"] = (avg * (total - 1) + wait_time) / total
        
        # Log
        logger.info(f"Rate limit stats: {json.dumps(self.stats)}")
    
    def get_stats(self) -> dict:
        """Get current statistics"""
        return self.stats
    
    def reset(self):
        """Reset statistics"""
        self.stats = {
            "total_requests": 0,
            "rate_limited_requests": 0,
            "average_wait_time": 0,
            "last_reset": datetime.now().isoformat()
        }

# Global monitor
monitor = RateLimitMonitor()
```

---

## 🔍 Checking Current Limits

Add to Streamlit app (`ui/app.py`):

```python
import streamlit as st
from src.utils.rate_limit_monitor import monitor

# In System Status page
st.subheader("Rate Limiting Status")

stats = monitor.get_stats()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Requests", stats["total_requests"])

with col2:
    st.metric("Rate Limited", stats["rate_limited_requests"])

with col3:
    st.metric("Avg Wait (sec)", f"{stats['average_wait_time']:.2f}")
```

---

## 📊 Rate Limit Configuration

Update `config/settings.py`:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Rate limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 20
    RATE_LIMIT_USER_REQUESTS_PER_HOUR: int = 100
    RATE_LIMIT_ENABLED: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
```

Add to `.env`:

```
# Rate limiting configuration
RATE_LIMIT_REQUESTS_PER_MINUTE=20
RATE_LIMIT_USER_REQUESTS_PER_HOUR=100
RATE_LIMIT_ENABLED=true
```

---

## 🚨 What Happens When Rate Limited?

### OpenAI Rate Limit Hit

```
Error: RateLimitError
Status Code: 429
Message: "Rate limit exceeded"

Response:
{
    "error": {
        "message": "Rate limit exceeded for your plan",
        "type": "rate_limit_error"
    }
}
```

**System Response:**
- ✅ Automatic retry with exponential backoff
- ✅ Wait 2-30 seconds
- ✅ Retry up to 3 times
- ❌ If still failed, return error to user

### Application Rate Limit Hit

```
Message: "Too many requests. Please wait X seconds"
Status: 429
Action: User should retry after delay
```

---

## 💡 Best Practices

### 1. **Configure Appropriate Limits**
- Free tier: 20 claims/minute max
- Paid tier: 100+ claims/minute
- Per-user: 100 claims/hour

### 2. **Monitor Usage**
- Track rate limit hits
- Alert if approaching limits
- Adjust configuration as needed

### 3. **Handle Gracefully**
- Return clear error messages
- Suggest retry time
- Log all rate limit events

### 4. **Scale Appropriately**
- Upgrade API plan for more throughput
- Use queuing for batch processing
- Consider async processing

---

## 🎯 Implementation Checklist

- [ ] Create `src/utils/rate_limiter.py`
- [ ] Create `src/utils/rate_limit_monitor.py`
- [ ] Update `src/orchestration/workflow.py` with rate limiting
- [ ] Update `config/settings.py` with configuration
- [ ] Add to `.env` file
- [ ] Add monitoring to Streamlit UI
- [ ] Test rate limiting behavior
- [ ] Monitor production usage
- [ ] Adjust limits based on usage

---

## 📈 Monitoring Dashboard

Add to Streamlit System Status:

```python
# Rate Limiting Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Requests This Hour",
        monitor.stats["total_requests"],
        "Rate: 20/min"
    )

with col2:
    rate_limited_pct = (
        monitor.stats["rate_limited_requests"] / 
        max(monitor.stats["total_requests"], 1) * 100
    )
    st.metric(
        "Rate Limited %",
        f"{rate_limited_pct:.1f}%",
        "Should be < 5%"
    )

# Alert if too high
if rate_limited_pct > 10:
    st.warning("⚠️ High rate limit hits! Consider upgrading API plan")
```

---

## 🚀 Current System Status

**Current Rate Limiting:**
- ✅ OpenAI built-in rate limiting (automatic)
- ⚠️ Application-level: Not implemented yet
- ⚠️ Per-user limiting: Not implemented yet
- ⚠️ Monitoring: Not implemented yet

**Next Steps:**
1. Add implementation files from above
2. Integrate with workflow
3. Test with high load
4. Monitor in production

---

## 📚 Additional Resources

- OpenAI Rate Limits: https://platform.openai.com/docs/guides/rate-limits
- Token Bucket Algorithm: https://en.wikipedia.org/wiki/Token_bucket
- Rate Limiting Best Practices: https://cloud.google.com/architecture/rate-limiting-strategies

---

*Last Updated: 2024-10-29*
*Rate Limiting Guide v1.0*

**Ready to implement rate limiting!** 🚦
