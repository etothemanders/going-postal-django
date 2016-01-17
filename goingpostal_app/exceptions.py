class UntrackableException(Exception):
    """
    Error raised when no activity data could be retrieved
    from the courrier's API.
    """

    def __init__(self, tracking_number):
        self.message = ('Sorry, tracking number {number} cannot be tracked.'
                        .format(number=tracking_number))


class DuplicateShipmentException(Exception):
    """
    Error raised when user tries to add a shipment with a
    tracking number which the user is already tracking.
    """

    def __init__(self, tracking_number):
        self.message = ('Sorry, you are already tracking {number}.'
                        .format(number=tracking_number))
