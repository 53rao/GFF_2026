"""
seed_data.py — Database Seed Script for Demo Customers
======================================================
Populates the local database with realistic SBI demo customers matching the
frontend mock data (`lib/mock-data.ts`), along with historical engagement logs
and initial cases.
"""

from __future__ import annotations

import asyncio


async def seed_database() -> None:
    """
    Seeds database tables with initial customers, accounts, and sample cases.
    
    TODO: Open session, check empty tables, insert demo records from mock definitions.
    """
    pass


if __name__ == "__main__":
    asyncio.run(seed_database())
