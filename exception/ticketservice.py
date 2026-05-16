class InsufficientInventory(Exception): ...



class TicketAlreadyExist(Exception): ...


class TicketAlreadyCanceled(Exception): ...


class TicketNotSubmitted(Exception): ...



class TicketNotFound(Exception): ...



class NoChairFound(Exception):
    """Raise if Chair number is Invalid Or booked"""
    ...



class NoCapacity(Exception): ...

class InvalidDateTime(Exception): ...