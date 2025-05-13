from commands.core_commands import BaseCommandHandler
from commands.handlers.lists import Listhandler
from commands.handlers.hashmap import HashmapHandler
from commands.handlers.sets import SetHandler



command_handlers = {}




command_handlers.update({
    "PING": BaseCommandHandler.handle_ping,
    "SET": BaseCommandHandler.handle_set,
    "GET": BaseCommandHandler.handle_get,
    "DEL": BaseCommandHandler.handle_del,
    "EXISTS": BaseCommandHandler.handle_exists,
    "INCR": BaseCommandHandler.handle_incr,
    "EXPIRE": BaseCommandHandler.handle_expire,
    "TTL": BaseCommandHandler.handle_ttl,
    "LPUSH": Listhandler.handle_lpush,
    "RPUSH": Listhandler.handle_rpush,
    "LPOP": Listhandler.handle_lpop,
    "RPOP": Listhandler.handle_rpop,
    "LRANGE": Listhandler.handle_lrange,
    "LLEN": Listhandler.handle_llen,
    "LTRIM": Listhandler.handle_ltrim,
    "LINDEX": Listhandler.handle_lindex,
    "LSET" : Listhandler.handle_lset,
    "LREM": Listhandler.handle_lrem,
    "BRPOP": Listhandler.handle_brpop,
    "BLPOP": Listhandler.handle_blpop,
    "RPOPLPUSH": Listhandler.handle_rpoplpush,
    "HGET": HashmapHandler.handle_hget,
    "HSET": HashmapHandler.handle_hset,
    "HDEL": HashmapHandler.handle_hdel,
    "HMGET": HashmapHandler.handle_hmget,
    "HMSET": HashmapHandler.handle_hmset,
    "HGETALL": HashmapHandler.handle_hgetall,
    "HLEN": HashmapHandler.handle_hlen,
    "HKEYS": HashmapHandler.handle_hkeys,
    "HVALS": HashmapHandler.handle_hvals,
    "HEXISTS": HashmapHandler.handle_hexists,
    "HINCRBY": HashmapHandler.handle_hincrby,
    "HINCRBYFLOAT": HashmapHandler.handle_hincrbyfloat,
    "SADD": SetHandler.handle_sadd,
    "SREM": SetHandler.handle_srem,
    "SPOP": SetHandler.handle_spop,
    "SRANDMEMBER": SetHandler.handle_srandmember,
    "SMEMBERS": SetHandler.handle_smembers,
    "SISMEMBER": SetHandler.handle_sismember,
    "SCARD": SetHandler.handle_scard,
    "SUNION": SetHandler.handle_sunion,
    "SINTER": SetHandler.handle_sinter,
    "SDIFF": SetHandler.handle_sdiff,
    "SUNIONSTORE": SetHandler.handle_sunionstore,
    "SINTERSTORE": SetHandler.handle_sinterstore,
    "SDIFFSTORE": SetHandler.handle_sdiffstore
})

