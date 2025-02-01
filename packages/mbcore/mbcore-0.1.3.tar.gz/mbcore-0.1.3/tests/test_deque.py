import asyncio
from mbcore.deque import AsyncDeque
import pytest

@pytest.fixture(scope="function")
def deque():
    return AsyncDeque(maxsize=5)

@pytest.mark.asyncio    
async def test_async_deque_left_right(deque: AsyncDeque):
    """Test AsyncDeque with left and right operations."""
    print("Starting test_async_deque_left_right")

    # Add items to the left
    for i in range(5):
        deque.interrupt(i)

    # Add items to the right
    consumer_task = asyncio.create_task(consumer(deque, items_to_consume=10))
    for i in range(5):
        await deque.put(f"Right Item {i}")

    await consumer_task

    # Ensure all tasks are marked as done
    await deque.join()

    # Check if the deque is empty
    assert deque.empty()
    print("Deque is empty")

    # Check the size of the deque
    assert len(deque) == 0
    print("Deque size is 0")

async def producer_left(deque:AsyncDeque):
    for i in range(5):
        deque.interrupt(f"Left Item {i}")
        print(f"Produced to left: Left Item {i}")
        await asyncio.sleep(0.1)

async def producer_right(deque:AsyncDeque):
    for i in range(5):
        await deque.put(f"Right Item {i}")
        print(f"Produced to right: Right Item {i}")
        await asyncio.sleep(0.1)

async def consumer_left(deque:AsyncDeque):
    for _ in range(5):
        item = await deque.get_left()
        print(f"Consumed from left: {item}")
        deque.task_done()
        await asyncio.sleep(0.2)

async def consumer_right(deque):
    for _ in range(5):
        item = await deque.get()
        print(f"Consumed from right: {item}")
        deque.task_done()
        await asyncio.sleep(0.2)

async def consumer(deque:AsyncDeque, items_to_consume=5):
    """Combined consumer that handles both sides of the deque."""
    items_consumed = 0
    while items_consumed < items_to_consume:
        try:
            # Alternately try both sides
            if items_consumed % 2 == 0:
                item = await asyncio.wait_for(deque.get(), timeout=0.5)
            else:
                item = await asyncio.wait_for(deque.get_left(), timeout=0.5)
            print(f"Consumed: {item}")
            deque.task_done()
            items_consumed += 1
        except asyncio.TimeoutError:
            # If timeout occurs, try the other side next time
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Consumer error: {e}")
            break

@pytest.mark.asyncio
async def test_producer_consumer(deque:AsyncDeque):
    print("Starting test_producer_consumer")
    total_items = 10  # Total items to be produced
    
    # Create producers and consumers
    producers = [
        producer_left(deque),
        producer_right(deque)
    ]
    
    consumers = [
        consumer(deque, total_items // 2),
        consumer(deque, total_items // 2)
    ]

    # Run everything concurrently with timeout
    try:
        await asyncio.wait_for(
            asyncio.gather(*producers, *consumers, return_exceptions=True),
            timeout=10.0
        )
    except asyncio.TimeoutError:
        print("Test timed out")
    except Exception as e:
        print(f"Test error: {e}")
    
    # Ensure all tasks are marked as done
    await deque.join()

    # Verify final state
    assert deque.empty(), "Deque should be empty after test"
    print("Deque is empty after test")


if __name__ == "__main__":
    asyncio.run(test_async_deque_left_right(AsyncDeque(maxsize=5)))
    asyncio.run(test_producer_consumer(AsyncDeque(maxsize=5)))
