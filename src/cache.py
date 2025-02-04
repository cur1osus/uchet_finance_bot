from cachetools import TTLCache

general_ttl = 6000

text_cache = TTLCache(maxsize=500, ttl=general_ttl)
button_cache = TTLCache(maxsize=500, ttl=general_ttl)
value_cache = TTLCache(maxsize=500, ttl=general_ttl)
photo_cache = TTLCache(maxsize=100, ttl=general_ttl)
