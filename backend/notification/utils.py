from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@async_to_sync
async def send_notification_to_user(user_id, message):
    channel_layer = get_channel_layer()
    # group_name = f"chat_user_{user_id}_notifications"
    group_name = f"user_{user_id}"

    print(group_name + " w utils")
    print(message)
    # Add the user to the notification group
    # await channel_layer.group_add(group_name, "notifications")
    # print(channel_layer.__dict__)
    # Send the notification message to the group
    await channel_layer.group_send(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        },
    )