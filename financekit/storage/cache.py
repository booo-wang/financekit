"""数据缓存机制"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib


class DataCache:
    """简单的数据缓存类"""

    def __init__(self, cache_dir: Optional[Path] = None, ttl_hours: int = 24):
        """
        初始化缓存

        Args:
            cache_dir: 缓存目录
            ttl_hours: 缓存有效期（小时）
        """
        self.cache_dir = cache_dir or Path(__file__).parent.parent.parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, key: str) -> str:
        """生成缓存键"""
        return hashlib.md5(key.encode()).hexdigest()

    def _get_cache_file(self, key: str) -> Path:
        """获取缓存文件路径"""
        cache_key = self._get_cache_key(key)
        return self.cache_dir / f"{cache_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存数据

        Args:
            key: 缓存键

        Returns:
            缓存数据或None
        """
        cache_file = self._get_cache_file(key)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # 检查是否过期
            timestamp = datetime.fromisoformat(cache_data["timestamp"])
            if datetime.now() - timestamp > self.ttl:
                cache_file.unlink()
                return None

            return cache_data["data"]
        except (json.JSONDecodeError, KeyError, OSError):
            return None

    def set(self, key: str, data: Any):
        """
        设置缓存数据

        Args:
            key: 缓存键
            data: 要缓存的数据
        """
        cache_file = self._get_cache_file(key)

        cache_data = {"timestamp": datetime.now().isoformat(), "data": data}

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, default=str)
        except OSError as e:
            print(f"缓存写入失败: {e}")

    def clear_expired(self):
        """清理过期缓存"""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)

                timestamp = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - timestamp > self.ttl:
                    cache_file.unlink()
            except (json.JSONDecodeError, OSError):
                pass

    def clear_all(self):
        """清空所有缓存"""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                pass
