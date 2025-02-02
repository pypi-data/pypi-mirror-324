from yta_general_utils.date import current_datetime
from dataclasses import dataclass


@dataclass
class Response:
    """
    The response we send with any request we receive.
    """

    # TODO: Set type
    timestamp: any
    """
    The moment in which the response is sent.
    """
    remaining_requests: int
    """
    The amount of requests the user can make.
    """
    content: any
    """
    The content of the response, which varies according
    to the request.
    """

    def __init__(
        self,
        content: any
    ):
        # TODO: Validate (?)
        self.timestamp = current_datetime()
        # TODO: Obtain 'remaining_requests' from database.
        # The value should have been reduced during the
        # solving process so it should be read updated
        self.content = content

    def as_json(self):
        """
        Get the response attributes as a json dict to
        be sent to the user.
        """
        return {
            'timestamp': self.timestamp,
            'remaining_requests': self.remaining_requests,
            'content': self.content
        }