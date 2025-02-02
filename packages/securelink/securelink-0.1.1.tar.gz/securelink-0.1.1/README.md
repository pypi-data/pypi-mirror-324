# 📌 SecureLink 
##  Expirable Signed URL Generator & API
SecureLink is a lightweight and flexible library for generating and verifying expirable signed URLs to control access to protected resources.

* 📦 Library Mode – Use it as a Python package to generate secure URLs.
* 🌍 API Mode – Deploy it as a FastAPI service to generate URLs via HTTP requests.


## 🚀 Features

* ✅ Expirable Links – Set expiration time for secure access
* ✅ Signed URLs – MD5
* ✅ FastAPI API – Built-in API for generating & verifying links
* ✅ Pluggable Architecture – Extendable for different signing strategies
* ✅ Works with Any Server – Supports Nginx  etc.

##  📦 Installation

####  Library Mode:

```bash
   pip install securelink
```

####  API Mode:

```bash
   
   pip install securelink[api]

```
## 🔧 Environment Variables
*  SECRET_KEY: Used for signing and validating secure links.

*   API_KEY: Used for API authentication if needed.


##   📝 Example Scenarios

####  Library Mode:


```python

import time
import securelink.sign

secure_url = securelink.sign.generate_md5_base64_url(
    "http://127.0.0.1/secure/", "secret", 5, "127.0.0.1"
)

print("✅ Normal success validation:", securelink.sign.validate_md5_base64_url(secure_url, "secret", "127.0.0.1"))
print("❌ Invalid IP validation:", securelink.sign.validate_md5_base64_url(secure_url, "secret", "10.44.0.1"))
print("❌ Invalid secret validation:", securelink.sign.validate_md5_base64_url(secure_url, "wrong secret", "127.0.0.1"))

time.sleep(8)
print("⏳ Delayed validation:", securelink.sign.validate_md5_base64_url(secure_url, "secret", "127.0.0.1"))

```
### 🚀 Running as an API:

```bash

   uvicorn securelink.api:app
   INFO:     Started server process [2928]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Once the API is running, you can access the interactive documentation at:
```
   http://127.0.0.1:8000/docs
```

## 📌 Nginx Configuration Example

```conf
location ^~ /secure/ {
    secure_link $arg_md5,$arg_expires;
    secure_link_md5 "$secure_link_expires$uri$remote_addr secret";

    if ($secure_link = "") {
        return 403;
    }

    if ($secure_link = "0") {
        return 410;
    }

    return 200;
}
```

## 📌 Notes

*  ✅ The signature includes the expiration time, requested resource path, and client IP (if provided).
  
*  ✅ The validation function ensures the signature is valid and the expiration time has not passed.

*  🔑 The secret key must be the same for both generation and validation.

*  ⏳ The timestamp of Nginx and the URL signing app should be the same.

*  🌐 (nginx) The link can be accessed only from the client IP that was used for signing.

*  🔗 (nginx) Only the specified endpoint can be accessed using a single sign.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.