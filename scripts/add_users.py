#!/usr/bin/env python3
"""
添加更多用户ID和模拟用户行为数据到events表
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timedelta
from backend.database import SessionLocal
from backend.models import Event, Item

def add_users(num_users=10, events_per_user=5):
    """添加新用户和模拟行为数据"""
    session = SessionLocal()

    # 获取所有可用的图书ID
    item_ids = [item.id for item in session.query(Item.id).all()]
    if not item_ids:
        print("错误：没有找到图书数据")
        return

    print(f"找到 {len(item_ids)} 本图书")

    # 现有用户列表
    existing_users = set([uid[0] for uid in session.query(Event.uid).distinct().all()])
    print(f"现有用户: {existing_users}")

    # 生成新用户ID
    new_users = []
    user_counter = 1000  # 起始ID
    while len(new_users) < num_users:
        uid = f"user{user_counter}"
        if uid not in existing_users:
            new_users.append(uid)
            existing_users.add(uid)
        user_counter += 1

    print(f"将添加 {len(new_users)} 个新用户: {new_users}")

    # 为每个用户添加事件
    total_added = 0
    for uid in new_users:
        # 随机选择一些图书
        user_item_ids = random.sample(item_ids, min(events_per_user, len(item_ids)))

        for item_id in user_item_ids:
            # 随机生成时间戳（最近30天内）
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            ts = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # 随机选择行为类型
            action = random.choice(['click', 'borrow', 'like'])

            event = Event(
                uid=uid,
                item_id=item_id,
                action=action,
                ts=ts
            )
            session.add(event)
            total_added += 1

    # 提交到数据库
    session.commit()
    session.close()

    print(f"成功添加 {len(new_users)} 个新用户和 {total_added} 条事件记录")

    # 验证添加结果
    session = SessionLocal()
    total_users = session.query(Event.uid).distinct().count()
    total_events = session.query(Event).count()
    session.close()

    print(f"现在总共有 {total_users} 个不同用户")
    print(f"现在总共有 {total_events} 条事件记录")

if __name__ == "__main__":
    add_users(num_users=10, events_per_user=5)