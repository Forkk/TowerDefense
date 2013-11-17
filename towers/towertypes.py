# vim: set expandtab ts=4 sw=4 softtabstop=4:

DEF_DESCRIPTION = "This is the default description for a tower. The developer who added it was probably too lazy to write a real one."

class TowerType(object):
    """
    Class representing information about a certain type of tower.
    """
    
    def __init__(self, name, tclass, cost, description=DEF_DESCRIPTION):
        self.name = name
        self.tclass = tclass
        self.cost = cost
        self.description = description

