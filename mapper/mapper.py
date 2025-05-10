from commands.core_commands import BaseCommandHandler
from commands.handlers.lists import Listhandler



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
    "RPOPLPUSH": Listhandler.handle_rpoplpush
})