import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
from collections import deque
from statistics import mean
import time


# 처리 시간 추적을 위한 큐
processing_times = deque(maxlen=100)


async def cpu_intensive_task(data: str) -> str:
    """CPU 집약적인 작업 (비동기 버전)"""
    start = time.time()
    
    # CPU를 많이 사용하는 계산
    result = 0
    for i in range(5000000):  # 백만 번 반복
        result += i * i
        # 더 복잡한 계산 추가
        if i % 2 == 0:
            result = result * 2
        else:
            result = result // 3
        
        # 다른 코루틴이 실행될 기회를 제공 (100000회마다)
        if i % 100000 == 0:
            await asyncio.sleep(0)
    
    duration = time.time() - start
    return f"비동기 처리 결과: {result % 10000}, 계산 시간: {duration:.3f}초, 입력: {data}"


def print_stats(prefix="비동기"):
    """현재 처리 통계 출력"""
    if not processing_times:
        return

    times = list(processing_times)
    avg_time = mean(times) * 1000  # ms로 변환

    print(f"\n=== {prefix} 처리 통계 ===")
    print(f"처리된 메시지 수: {len(times)}")
    print(f"평균 처리 시간: {avg_time:.2f}ms")

    if len(times) >= 100:
        print(f"최근 100개 평균: {avg_time:.2f}ms")
    if len(times) >= 10:
        print(f"최근 10개 평균: {mean(list(times)[-10:]) * 1000:.2f}ms")
    print(f"마지막 처리 시간: {times[-1] * 1000:.2f}ms")
    print("================\n")


async def message_handler(msg):
    try:
        start_time = time.time()

        # 메시지 데이터 디코딩
        data = msg.data.decode()
        print(f"비동기 서버 요청 받음: {data}")

        # CPU 집약적 작업을 비동기로 실행
        response = await cpu_intensive_task(data)

        # 응답 전송
        await msg.respond(response.encode())

        # 처리 시간 기록
        processing_time = time.time() - start_time
        processing_times.append(processing_time)

        # 통계 출력 (1, 10, 100개 단위로)
        if len(processing_times) in [1, 10, 100] or len(processing_times) % 100 == 0:
            print_stats()

    except Exception as e:
        print(f"에러 발생: {str(e)}")


async def main():
    # NATS 클라이언트 생성
    nc = NATS()

    try:
        # NATS 서버에 연결
        await nc.connect(
            "nats://localhost:4222",
            max_reconnect_attempts=-1,
            reconnect_time_wait=2,
            ping_interval=20,
            max_outstanding_pings=5,
        )
        print("비동기 서버: NATS 서버에 연결됨")

        # 여러 개의 구독자 설정
        subscription_tasks = []
        for _ in range(4):  # 스레드 서버와 동일한 수의 워커
            sub = await nc.subscribe(
                "cpu.request",
                cb=message_handler,
                queue="async_workers",
            )
            subscription_tasks.append(sub)

        print("비동기 서버: 구독 시작")

        # 종료 시그널 대기
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print("서비스 종료 중...")

    except Exception as e:
        print(f"에러 발생: {str(e)}")
    finally:
        # 연결 종료
        await nc.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("비동기 서버가 종료됩니다.")
