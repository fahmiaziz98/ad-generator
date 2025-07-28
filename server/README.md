# API Documentation

## Overview
This document provides detailed information about the API endpoints available in the AI Ad Generator project. The API supports generating advertisements and images for products based on user input.

---

## Endpoints

### 1. Generate Advertisement (Non-Streaming)

**Endpoint:**
```
POST /api/v1/generate
```

**Description:**
Generates an advertisement for a product without streaming.

**Request Headers:**
- `accept: application/json`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "product_name": "Aurora Pro Wireless Earbuds",
  "brand_name": "SoundWave",
  "category": ["Electronics", "Audio"],
  "price": 199,
  "discounted_price": 149,
  "description": "Premium wireless earbuds with noise cancellation and 24-hour battery life",
  "product_url": "https://shop.soundwave.com/aurora-earbuds",
  "ad_type": "social_media",
  "ad_tone": "playful"
}
```

**Response:**
```json
{
  "ad_content": "> 🎶🎧 Ditch the drama, keep the beats! 🎧🎶\n\nIntroducing the Aurora Pro Wireless Earbuds from SoundWave! ✨ Immerse yourself in crystal-clear audio and say buh-bye to distractions with our amazing noise cancellation. \n\n✅ 24-hour battery? Road trip READY!\n✅ Supreme comfort for all-day vibes.\n✅ Seriously sleek design – you’ll look good listening! 😎\n\nSnag yours today for just $149! ➡️ [https://shop.soundwave.com/aurora-earbuds]\n\n#WirelessEarbuds #SoundWave #AudioBliss #TechDeals #ListenUp",
  "product_info": {
    "product_name": "Aurora Pro Wireless Earbuds",
    "brand": "SoundWave",
    "category": [
      "Electronics",
      "Audio"
    ],
    "description": "Premium wireless earbuds with noise cancellation and 24-hour battery life",
    "price": "199.0",
    "discounted_price": "149.0",
    "store_link": "https://shop.soundwave.com/aurora-earbuds"
  },
  "ad_settings": {
    "ad_type": "social_media",
    "ad_tone": "playful"
  },
  "generation_time": 8.631563663482666,
  "model_used": "google/gemma-3-12b-it",
  "request_id": "0ccb9943-8d2a-4f47-8421-6e0c18d738c7",
  "timestamp": "2025-07-28T21:45:02.657861"
}
```

---

### 2. Generate Advertisement (Streaming)

**Endpoint:**
```
POST /api/v1/generate-stream
```

**Description:**
Generates an advertisement for a product in a streaming format.

**Request Headers:**
- `accept: application/json`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "product_name": "Aurora Pro Wireless Earbuds",
  "brand_name": "SoundWave",
  "category": ["Electronics", "Audio"],
  "price": 199,
  "discounted_price": 149,
  "description": "Premium wireless earbuds with noise cancellation and 24-hour battery life",
  "product_url": "https://shop.soundwave.com/aurora-earbuds",
  "ad_type": "social_media",
  "ad_tone": "playful"
}
```

**Response:**
```json
{
  "status": "processing",
  "message": "Generating your advertisement...",
  "request_id": "db546d8d-863e-4dfb-9335-745c9d91fd26"
}
```

**Streaming Response Example:**
```json
{"status": "streaming", "content": ">", "progress": 0.2}
{"status": "streaming", "content": " 🎶", "progress": 0.4}
{"status": "completed", "ad_content": "> 🎶 Ditch the drama, keep the beats! 🎶\n\nMeet the Aurora Pro Wireless Earbuds from SoundWave!"}
```

---

### 3. Generate Image

**Endpoint:**
```
POST /api/v1/generate-image
```

**Description:**
Generates an image for a product based on the provided description.

**Request Headers:**
- `accept: application/json`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "product_name": "Aurora Pro Wireless",
  "brand_name": "SoundWave",
  "description": "Premium wireless earbuds with noise cancellation and 24-hour battery life"
}
```

**Response:**
```json
{
  "image_path": "uploads/Aurora_Pro_Wireless_SoundWave.png",
  "image_url": null,
  "source": "generated",
  "generated": true
}
```

---

### 4. Retrieve Image

**Endpoint:**
```
GET /api/v1/images/{image_name}
```

**Description:**
Retrieves a generated image by its name.

**Request Headers:**
- `accept: application/json`

**Path Parameter:**
- `image_name`: The name of the image file to retrieve (e.g., `Aurora_Pro_Wireless_SoundWave.png`).

**Response:**
The image file is returned format .png (Download)


---

## Notes
- Ensure that all required fields are provided in the request body to avoid validation errors.
- The `generate-stream` endpoint streams the advertisement content in chunks, allowing for real-time updates.
- The `generate-image` endpoint creates a product image based on the description and other details provided.

For further assistance, contact [fahmiazizfadhil999@gmail.com](mailto:fahmiazizfadhil999@gmail.com).
