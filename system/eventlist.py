
from util import hook

hook.create("connect", system=True)
hook.create("privmsg", system=True)
hook.create("joined", system=True)
hook.create("left", system=True)
hook.create("noticed", system=True)
hook.create("startup", system=True)
hook.create("shutdown", system=True)