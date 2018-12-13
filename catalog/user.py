import logging

logger = logging.getLogger(__name__)

def jwt_get_username_from_payload_handler(payload):
    logger.error(payload)
    return payload.get('sub').replace('|', '.')
