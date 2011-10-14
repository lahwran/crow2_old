
from events import hook, Event, Registration, Order



def regmaker(func, args = (), keywords = {}):
    if len(args) < 1:
        name = func.func_name
    else:
        name = str(args[0])
        args = args[1:]
    keywords["commandname"] = name

    registration = Registration(func, args, keywords)

    return registration



hook.create("command", makereg = regmaker)
hook.create("privmsg")
hook.create("sieve")
hook.create("sending_chat")

@hook.privmsg
def privmsg(event):
    print event.msg, event

@hook.privmsg(chan="#risucraft")
def risucraft_spammed(event):
    print "QUICK +m RISUCRAFT! SOMEONE IS SPAMMING IT!"

@hook.sieve(position = Order.early)
def ignore(event):
    if "nick" in event and event.nick in ignorelist:
        event.cancel()


@hook.sending_chat
def censor(event):
    for i in censors:
        event.msg.replace(i, "[CENSORED]")

@hook.command
def google(event):
    googlesearch.google(event.arg)

event = Event({"msg": "hey there!", "chan": "#hell"})
hook.privmsg.fire(event)
event = Event({"msg": "blab blab blab", "chan": "#risucraft"})
hook.privmsg.fire(event)




