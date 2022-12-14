import relay

class Valve(relay.RelayBoard):

    def __init__(self):
        relay.RelayBoard.__init__(self)
        self.current_position = 10 # angle degress
        self.lasttimems = 0
        self.direction = "STOP"
        self.ANGLESPEED = 90/120 # per second

    def update(self, currtimems):
        had_change = False
        next_dir= self.__derive_direction()
        if self.direction != next_dir:
            had_change = True
        self.direction = next_dir
        next_pos = self.__derive_position(self.current_position, currtimems,self.lasttimems, self.direction)
        if self.current_position != next_pos:
            had_change = True
        self.current_position = next_pos
        self.lasttimems = currtimems
        return had_change

    def set_position(self, newpos):
        self.current_position = newpos
        self.lasttimems = self._getcurrms()

    def __derive_direction(self):
        # derive direction from current relay state. Might look weird (and can be prone to error if the logic of relays is changed)
        # but it makes sure the direction is derived the reality of the relays on not a top level assumption
        if(not self.Relay_State1 and not self.Relay_State2):
            return "STOP"
        if(self.Relay_State1 and not self.Relay_State2):
            return "COLDER"
        if(not self.Relay_State1 and self.Relay_State2):
            return "HOTTER"
        return "INVALID"

    def __derive_position(self,curr_position,ctimems,ltimems,dir):
        new_pos = curr_position
        if dir == "HOTTER":
            if curr_position<90:
                new_pos = new_pos + ((ctimems-ltimems) / 1000) * self.ANGLESPEED
                if new_pos>90:
                    new_pos = 90
        if dir == "COLDER":
            if curr_position>0:
                new_pos = new_pos - ((ctimems-ltimems) / 1000) * self.ANGLESPEED
                if new_pos<0:
                    new_pos = 0

        return new_pos







