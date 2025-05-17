# ba_meta require api 7
import ba, _ba
from bastd.ui.party import PartyWindow

old__init__ = PartyWindow.on_chat_message
def chat_handler(self, msg: str) -> None:
    old__init__(self, msg)
    player_name = msg.split(': ')[0]
    message = msg.split(': ')[-1]
    command = message.split(maxsplit=1)[0]
    arg = message.split(maxsplit=1)[-1] if len(message.split(maxsplit=1)) == 2 else None
    if command == '/par':
        if arg:
            if arg == 'del':
                if not player_name in BlastParticle.player_activates or BlastParticle.player_activates[player_name].get('active') is None:
                    _ba.chatmessage('у вас нет партиклов', sender_override='Server')
                    return
                else:
                    BlastParticle.player_activates[player_name].pop('active')
                    return
            else:
                if len(arg.split()) == 3:
                    color = tuple(map(float, arg.split()))
                else:
                    _ba.chatmessage('введите 3 значения', sender_override='Server')
                    return
        else:
            color = None
        if BlastParticle.player_activates.get(player_name):
            if BlastParticle.player_activates[player_name].get('active'):
                BlastParticle.player_activates[player_name]['color'] = color if color else (0.0,0.0,0.0)
            else:
                BlastParticle(player_name, color)
        else:
            BlastParticle(player_name, color)
PartyWindow.on_chat_message = chat_handler

class BlastParticle:
    player_activates = {} # example {'PC449444': {'active': True, 'color': (0.5,0.0,1.0)}, 'myxa': {'active': True, 'color': (1.0,0.0,1.0)}}
    def __init__(self, player_name, color):
        BlastParticle.player_activates[player_name] = {}
        BlastParticle.player_activates[player_name]['color'] = color if color else (0.0,0.0,0.0)
        BlastParticle.player_activates[player_name]['active'] = True
        if BlastParticle.player_activates[player_name]['active']:
            self.par_start(player_name)
      
    def get_pos(self, player_name):
        activity = _ba.get_foreground_host_activity()
        for player in activity.players:
            if player.getname(False, False) == player_name:
                position = tuple(player.position)
                return position
        return None
      
    def add_particle(self, player_name):
        if BlastParticle.player_activates[player_name].get('active') is None:
            self.timer = None
            return
        activity = _ba.get_foreground_host_activity()
        position = self.get_pos(player_name)
        color = BlastParticle.player_activates[player_name]['color']
        if position:
            with ba.Context(activity):
                self.scorch = ba.newnode(
                    'scorch',
                    attrs={
                        'position': position,
                        'size': 1.0,
                        'color': color}
                )
                ba.animate(self.scorch, 'presence', {1.000: 1, 3.000: 0})

    def par_start(self, player_name):
        self.timer = ba.Timer(0.7, ba.Call(self.add_particle, player_name), repeat=True)

# ba_meta export plugin
class ByFlou(ba.Plugin):
    pass