"""
common
"""

# Alt Corp
from altcorp.models import AltCorpRequest

DEFAULT_ICON_SIZE = 32


def add_common_context(request, context: dict) -> dict:
    """adds the common context used by all view"""
    pending = AltCorpRequest.pending().count()
    danger = AltCorpRequest.danger().count()
    revoke = AltCorpRequest.expired_revoke_deadlines().count()
    new_context = {
        **{
            "total_count": {
                "pending": pending,
                "danger": danger,
                "revoke": revoke,
            },
        },
        **context,
    }
    return new_context
