import time
from typing import TYPE_CHECKING

from lonelypsp.auth.config import AuthResult
from lonelypsp.stateful.constants import BroadcasterToSubscriberStatefulMessageType
from lonelypsp.stateful.messages.confirm_subscribe import (
    B2S_ConfirmSubscribeExact,
    serialize_b2s_confirm_subscribe_exact,
)
from lonelypsp.stateful.messages.subscribe import S2B_SubscribeExact

from lonelypss.ws.handlers.open.errors import AuthRejectedException
from lonelypss.ws.handlers.open.processors.protocol import S2B_MessageProcessor
from lonelypss.ws.handlers.open.send_simple_asap import send_simple_asap
from lonelypss.ws.handlers.open.websocket_url import (
    make_for_receive_websocket_url_and_change_counter,
)
from lonelypss.ws.state import StateOpen


async def process_subscribe_exact(
    state: StateOpen, message: S2B_SubscribeExact
) -> None:
    """Processes a request by the subscriber to subscribe to a specific topic,
    receiving notifications within this websocket
    """
    url = make_for_receive_websocket_url_and_change_counter(state)
    auth_at = time.time()
    auth_result = await state.broadcaster_config.is_subscribe_exact_allowed(
        tracing=message.tracing,
        url=url,
        recovery=None,
        exact=message.topic,
        now=auth_at,
        authorization=message.authorization,
    )
    if auth_result != AuthResult.OK:
        raise AuthRejectedException(f"subscribe exact: {auth_result}")

    if message.topic in state.my_receiver.exact_subscriptions:
        raise Exception("already subscribed to exact topic")

    resp_tracing = b""  # TODO: tracing
    # TODO: not safe to use a different url here I believe, because we would need to
    # ensure nothing else gets queued to be sent between now and the send actually
    # being queued, which would require being in a send_task, not a process_task
    resp_authorization = (
        await state.broadcaster_config.authorize_confirm_subscribe_exact(
            tracing=resp_tracing,
            url=url,
            recovery=None,
            exact=message.topic,
            now=time.time(),
        )
    )

    # note we confirm before registering to ensure they don't receive notifications
    # on the topic before its been confirmed
    send_simple_asap(
        state,
        serialize_b2s_confirm_subscribe_exact(
            B2S_ConfirmSubscribeExact(
                type=BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_EXACT,
                topic=message.topic,
                authorization=resp_authorization,
                tracing=resp_tracing,
            ),
            minimal_headers=state.broadcaster_config.websocket_minimal_headers,
        ),
    )
    state.my_receiver.exact_subscriptions.add(message.topic)
    await state.internal_receiver.increment_exact(message.topic)


if TYPE_CHECKING:
    _: S2B_MessageProcessor[S2B_SubscribeExact] = process_subscribe_exact
