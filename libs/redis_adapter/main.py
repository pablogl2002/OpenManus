import redis


class RedisHandler:
	def __init__(self, redis_broker, redis_broker_port, redis_db, redis_pwd):
		self.handler = redis.Redis(
			host=redis_broker,
			port=redis_broker_port,
			db=redis_db,
			password=redis_pwd,
			encoding='utf-8',
			decode_responses=True,
		)

	def exists(self, key):
		return self.handler.exists(key)

	def set(self, key, value, expiry=None):
		if expiry:
			self.handler.setex(key, expiry, value)
		else:
			self.handler.set(key, value)

	def get(self, key):
		return self.handler.get(key)

	def get_pattern(self, pattern):
		return self.handler.scan_iter(pattern)
	
	def delete(self, key: str):
		self.handler.delete(key)

	def publish(self, topic, data):
		return self.handler.publish(topic, data)

	def hset(self, name, key, value):
		self.handler.hset(name=name, key=key, value=value)

	def hget(self, name, key=None):
		if key:
			return self.handler.hget(name=name, key=key)
		else:
			return self.handler.hgetall(name)

	def hdel(self, name, key=None):
		if key:
			self.handler.hdel(name, key)
		else:
			all_keys = list(self.handler.hgetall(name).keys())
			self.handler.hdel(name, *all_keys)
