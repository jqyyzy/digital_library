#!/usr/bin/env python3
"""
测试推荐系统对新用户的工作情况
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.recommender import TfidfRecommender

def test_recommendation():
    """测试推荐功能"""
    print("测试推荐系统...")

    # 创建推荐器实例
    recommender = TfidfRecommender(SessionLocal)

    # 获取数据库会话
    session = SessionLocal()

    try:
        # 测试现有用户 u123
        print("\n1. 测试现有用户 u123:")
        recs = recommender.recommend(session, uid="u123", q=None, k=5)
        print(f"   为 u123 生成 {len(recs)} 条推荐")
        for i, rec in enumerate(recs[:3]):
            print(f"   {i+1}. {rec['title']} (评分: {rec['score']:.3f})")

        # 测试新用户 user1000
        print("\n2. 测试新用户 user1000:")
        recs = recommender.recommend(session, uid="user1000", q=None, k=5)
        print(f"   为 user1000 生成 {len(recs)} 条推荐")
        if recs:
            for i, rec in enumerate(recs[:3]):
                print(f"   {i+1}. {rec['title']} (评分: {rec['score']:.3f})")
        else:
            print("   没有推荐结果（可能是冷启动情况）")

        # 测试带查询的推荐
        print("\n3. 测试带查询的推荐 (查询: 'python'):")
        recs = recommender.recommend(session, uid=None, q="python", k=5)
        print(f"   基于查询生成 {len(recs)} 条推荐")
        if recs:
            for i, rec in enumerate(recs[:3]):
                print(f"   {i+1}. {rec['title']} (评分: {rec['score']:.3f})")

        # 测试用户总数
        from backend.models import Event
        user_count = session.query(Event.uid).distinct().count()
        event_count = session.query(Event).count()
        print(f"\n数据库统计:")
        print(f"   用户总数: {user_count}")
        print(f"   事件总数: {event_count}")

    finally:
        session.close()

    print("\n测试完成!")

if __name__ == "__main__":
    test_recommendation()