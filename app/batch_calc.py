# app/batch_calc.py

import concurrent.futures
import asyncio
import math
import logging
from .crud import get_patients_in_batches, get_total_patient_count
from flask import current_app

logger = logging.getLogger(__name__)

def _calculate_batch_average(patients_batch):
    """Helper function to calculate average age for a list of patients."""
    if not patients_batch:
        return 0
    total_age = sum(p.age for p in patients_batch)
    return total_age / len(patients_batch)

def calculate_average_age_threaded(batch_size: int = 10) -> float:
    """
    Calculates the average age of all patients using ThreadPoolExecutor.
    """
    total_patients = get_total_patient_count()
    if total_patients == 0:
        return 0.0

    num_batches = math.ceil(total_patients / batch_size)
    all_ages = []

    # Use a thread pool to fetch and process batches concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_batches):
            offset = i * batch_size
            # Pass app context for database operations in threads
            app_context = current_app.app_context()
            futures.append(executor.submit(_get_and_process_batch_threaded, app_context, offset, batch_size))

        for future in concurrent.futures.as_completed(futures):
            try:
                batch_ages = future.result()
                all_ages.extend(batch_ages)
            except Exception as e:
                logger.error(f"Error processing batch in thread pool: {e}", exc_info=True)

    if not all_ages:
        return 0.0
    return sum(all_ages) / len(all_ages)

def _get_and_process_batch_threaded(app_context, offset, batch_size):
    """Helper for threaded execution to get patients and return their ages.
    Runs within a Flask app context to allow DB access."""
    with app_context:
        patients = get_patients_in_batches(batch_size, offset)
        return [p.age for p in patients]


async def _get_and_process_batch_async(offset, batch_size):
    """Helper for asyncio execution to get patients and return their ages.
    Note: For true async DB operations, you'd need SQLAlchemy.ext.asyncio
    and an async DB driver (e.g., aiosqlite). This example fetches
    synchronously but allows other coroutines to run."""
    # In a real async app, get_patients_in_batches would be an async def function.
    # For now, we simulate async I/O with asyncio.sleep.
    patients = get_patients_in_batches(batch_size, offset)
    await asyncio.sleep(0.001) # Simulate some async I/O work
    return [p.age for p in patients]

async def calculate_average_age_async(batch_size: int = 10) -> float:
    """
    Calculates the average age of all patients using asyncio coroutines.
    """
    total_patients = get_total_patient_count()
    if total_patients == 0:
        return 0.0

    num_batches = math.ceil(total_patients / batch_size)
    all_ages = []

    tasks = []
    for i in range(num_batches):
        offset = i * batch_size
        tasks.append(_get_and_process_batch_async(offset, batch_size))

    # Run all batch processing tasks concurrently
    results = await asyncio.gather(*tasks)

    for batch_ages in results:
        all_ages.extend(batch_ages)

    if not all_ages:
        return 0.0
    return sum(all_ages) / len(all_ages)