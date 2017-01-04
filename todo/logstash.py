import logging
from logging import Filter

from crum import get_current_request

logger = logging.getLogger('todo.logging')

class LogStashFilter(Filter):
    """
    Adds extra context to every logstash entry
    """
    def filter(self, record):
        try:
            request = get_current_request()
            if request:
                record.request_id = getattr(request, 'request_id', None)
                if getattr(request, 'user', None) and request.user.is_authenticated():
                    record.user_id = request.user.id
        except Exception:
            logger.exception("Error while logging entry to logstash")
        return 1  # log this record
