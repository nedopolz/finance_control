from aiokafka import AIOKafkaConsumer

from src.app.api.v1.services.DBservices import get_userDB_service
from src.app.proto_files.user_pb2 import UserCreatedMessage


class KafkaConsumer:
    def __init__(self, host: str, topic: str):
        self.consumer = AIOKafkaConsumer(topic, bootstrap_servers=host)
        self.user_service = get_userDB_service()

    async def consume_user_create(self) -> None:
        await self.consumer.start()

        async for msg in self.consumer:
            message = UserCreatedMessage()
            message.ParseFromString(msg.value)
            await self.user_service.create_user(message.externalID)  # TODO add retry
        await self.consumer.stop()
