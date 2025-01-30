import asyncio
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg as NATSMessage
from typing import Callable, Any, List, Tuple


class LitefaasServer:
    def __init__(self, nats_url: str = "nats://localhost:4222", debug: bool = False):
        self.nats_url = nats_url
        self.functions = {}  # Changed to {subject: [(func, queue_group), ...]}
        self._nc = None
        self.debug = debug  # Added debug mode setting

    def func(self, subject: str, queue_group: str = None):
        """Function decorator

        Args:
            subject (str): NATS subject
            queue_group (str, optional): Queue group name. None if not using queue group
        """

        def decorator(func: Callable):
            if subject not in self.functions:
                self.functions[subject] = []

            # subject와 queue_group이 모두 동일한 경우 체크
            for existing_func, existing_queue in self.functions[subject]:
                if existing_queue == queue_group:
                    raise ValueError(
                        f"Queue group '{queue_group}' is already registered for subject '{subject}'"
                    )

            self.functions[subject].append((func, queue_group))
            return func

        return decorator

    async def _handle_message(self, msg, func: Callable):
        # 메시지 처리를 별도의 태스크로 실행
        asyncio.ensure_future(self._process_message(msg, func))

    async def _process_message(self, msg: NATSMessage, func: Callable):
        try:
            data = msg.data.decode()
            if self.debug:
                print(f"Request received: {data}")

            # Check if function is coroutine and handle appropriately
            if asyncio.iscoroutinefunction(func):
                result = await func(data)
            else:
                result = func(data)

            if self.debug:
                print(f"Sending response: {result}")
            await msg.respond(str(result).encode())

        except Exception as e:
            if self.debug:
                print(f"Error occurred: {str(e)}")
            await msg.respond(f"Error: {str(e)}".encode())

    async def start(self):
        """Start server"""
        if not self.functions:
            raise ValueError("No registered functions.")

        self._nc = NATS()
        try:
            await self._nc.connect(
                self.nats_url,
                reconnect_time_wait=2,
                max_reconnect_attempts=-1,
                ping_interval=20,
                max_outstanding_pings=5,
            )
            print("Connected to NATS server")

            # Set up subscription for each function
            for subject, handlers in self.functions.items():
                for func, queue_group in handlers:

                    def create_handler(f):
                        async def message_handler(msg):
                            await self._handle_message(msg, f)

                        return message_handler

                    # Use queue group only if specified
                    if queue_group:
                        await self._nc.subscribe(
                            subject,
                            cb=create_handler(func),
                            queue=queue_group,
                        )
                    else:
                        await self._nc.subscribe(subject, cb=create_handler(func))

            if self.debug:
                print(
                    f"Server started - Registered functions: {list(self.functions.keys())}"
                )
            await asyncio.Event().wait()
        except Exception as e:
            if self.debug:
                print(f"Server start failed: {str(e)}")


class LitefaasClient:
    def __init__(self, nc: NATS):
        self._nc = nc

    @classmethod
    async def connect(cls, nats_url: str = "nats://localhost:4222") -> "LitefaasClient":
        """클라이언트 인스턴스 생성"""
        nc = NATS()
        await nc.connect(nats_url)
        return cls(nc)

    async def call(self, subject: str, data: Any, timeout: float = 30.0) -> str:
        """함수 호출"""
        try:
            response = await self._nc.request(
                subject, str(data).encode(), timeout=timeout
            )
            result = response.data.decode()
            if result.startswith("Error:"):
                raise RuntimeError(result[6:].strip())
            return result
        except Exception as e:
            raise RuntimeError(f"함수 호출 실패 ({subject}): {str(e)}")

    async def close(self):
        """연결 종료"""
        await self._nc.close()

    async def subscribe(self, subject: str, callback):
        """브로드캐스트 메시지 구독"""
        await self._nc.subscribe(subject, cb=callback)


def run_server(faas_instance: LitefaasServer):
    """Run server"""
    try:
        asyncio.run(faas_instance.start())
    except KeyboardInterrupt:
        print("Server is shutting down.")
