import hashlib
import base64
from datetime import timedelta, datetime
from urllib.parse import urlparse, parse_qs


def split_url(url: str):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    link = parsed_url.path
    parameters = parse_qs(parsed_url.query)

    return base_url, link, parameters


def generate_md5_base64_url(
    url, secret: str, expire_seconds: int = 20, clientip: str = "127.0.0.1"
) -> str:
    """
    Generates an MD5 hash of the input , encodes it in url safe base64,
    link should not contain the parameter,
    nginx support 

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
    """
    # Create an MD5 hash of the data (binary output)
    expire = int((datetime.now() + timedelta(seconds=expire_seconds)).timestamp())
    _, link, parameters = split_url(url)

    signature = f"{expire}{link}{clientip} {secret}"

    md5_hash = hashlib.md5(signature.encode("utf-8")).digest()

    # Encode the MD5 hash in base64
    md5_encode = base64.urlsafe_b64encode(md5_hash).decode("utf-8").rstrip("=")
    seperator = "&" if parameters else "?"

    return f"{url}{seperator}md5={md5_encode}&expires={expire}"


def validate_md5_base64_url(url: str, secret: str, clientip: str = "127.0.0.1") -> bool:
    """
    Validates the md5 signature and expiry in the URL.

    :param url: The URL containing md5 and expires query parameters.
    :param secret: The secret used to validate the signature.
    :param clientip: The client IP to validate against.
    :return: True if the URL is valid, False otherwise.
    """
    _, link, parameters = split_url(url)

    # Extract md5 and expires from the URL parameters
    md5_encode = parameters.get("md5", [None])[0]
    expire = parameters.get("expires", [None])[0]

    if not md5_encode or not expire:
        return False  # Invalid URL, missing required parameters

    # Check if the URL has expired
    if int(expire) < int(datetime.now().timestamp()):
        return False  # Expired URL

    # Recreate the signature to compare
    signature = f"{expire}{link}{clientip} {secret}"
    
    # Create the MD5 hash of the signature (binary output)
    md5_hash = hashlib.md5(signature.encode("utf-8")).digest()

    # Encode the MD5 hash in base64 (url-safe encoding)
    generated_md5_encode = base64.urlsafe_b64encode(md5_hash).decode("utf-8").rstrip("=")

    # Validate if the generated MD5 hash matches the one in the URL
    return generated_md5_encode == md5_encode