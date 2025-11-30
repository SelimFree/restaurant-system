import asyncio
import logging
import signal
from datetime import datetime, timedelta, timezone
from sqlalchemy import delete
from sqlalchemy.future import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.database import AsyncSessionLocal
from models.orders import Order
from models.order_items import OrderItem
from schemas.orders import OrderStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup_worker")

async def monthly_cleanup_task():
    logger.info("Starting Monthly Cleanup...")
    
    async with AsyncSessionLocal() as db:
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
            
            stmt = select(Order.id).where(
                Order.status == OrderStatus.SERVED.value, 
                Order.updated_at < cutoff_date
            )
            result = await db.execute(stmt)
            order_ids = result.scalars().all()

            if not order_ids:
                logger.info("No old orders found. Skipping.")
                return

            delete_stmt = delete(OrderItem).where(OrderItem.order_id.in_(order_ids))
            result = await db.execute(delete_stmt)
            await db.commit()
            
            logger.info(f"Deleted items for {len(order_ids)} orders. Rows removed: {result.rowcount}")

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            await db.rollback()

async def run_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        monthly_cleanup_task, 
        trigger='cron', 
        day=1, 
        hour=3, 
        minute=0
    )

    scheduler.start()
    logger.info("Worker Container Started. Next run scheduled for 1st of the month.")

    stop_event = asyncio.Event()
    
    def handle_sigterm(*args):
        stop_event.set()
    
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)

    await stop_event.wait()
    logger.info("Worker shutting down...")

if __name__ == "__main__":
    asyncio.run(run_scheduler())