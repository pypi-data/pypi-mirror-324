# -*- coding: UTF-8 –*-
import os.path
import redis
import socket
from mdbq.mysql import s_query
from mdbq.config import myconfig
import pandas as pd
import json
import datetime
import threading
import logging
from logging.handlers import RotatingFileHandler
import getpass
import platform

if platform.system() == 'Windows':
    D_PATH = os.path.join(f'C:\\Users\\{getpass.getuser()}\\Downloads')
else:
    D_PATH = os.path.join(f'/Users/{getpass.getuser()}/Downloads')


if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
    conf = myconfig.main()
    conf_data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    redis_password = conf['Windows']['company']['redis']['local']['password']
elif socket.gethostname() == 'MacBookPro':
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    redis_password = conf['Windows']['company']['redis']['local']['password']
else:
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    redis_password = conf['Windows']['company']['redis']['local']['password']  # redis 使用本地数据，全部机子相同

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# 获取当前模块的日志记录器
logger = logging.getLogger(__name__)

# 创建一个文件处理器，用于将日志写入文件
# file_handler = logging.FileHandler(os.path.join(D_PATH, 'logfile', 'redis.log'))
if not os.path.isdir(os.path.join(D_PATH, 'logfile')):
    os.makedirs(os.path.join(D_PATH, 'logfile'))
log_file = os.path.join(D_PATH, 'logfile', 'redis.log')
file_handler = RotatingFileHandler(log_file, maxBytes=3 * 1024 * 1024, backupCount=10)  # 保留10个备份文件
file_handler.setLevel(logging.INFO)  # 设置文件处理器的日志级别

# 创建一个日志格式器，并设置给文件处理器
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)


class RedisData(object):
    def __init__(self, redis_engine, download, cache_ttl: int):
        self.redis_engine = redis_engine  # Redis 数据处理引擎
        self.download = download  # MySQL 数据处理引擎
        self.cache_ttl = cache_ttl * 60  # 缓存过期时间（秒）

    def get_from_mysql(
            self,
            db_name: str,
            table_name: str,
            set_year: bool,
            start_date,
            end_date
    ) -> pd.DataFrame:
        """
        从 MySQL 读取数据并返回 DataFrame

        Args:
            set_year: 表名是否包含年份后缀
        """
        dfs = []
        if set_year:
            current_year = datetime.datetime.today().year
            for year in range(2024, current_year + 1):
                df = self._fetch_table_data(
                    db_name, f"{table_name}_{year}", start_date, end_date
                )
                if df is not None:
                    dfs.append(df)
        else:
            df = self._fetch_table_data(db_name, table_name, start_date, end_date)
            if df is not None:
                dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        if combined_df.empty:
            logger.info(f"警告: {db_name}.{table_name} 未读取到数据")
        else:
            combined_df = self._convert_date_columns(combined_df)
        return combined_df

    def get_from_redis(
            self,
            db_name: str,
            table_name: str,
            set_year: bool,
            start_date,
            end_date
    ) -> pd.DataFrame:
        """
        从 Redis 获取数据，若缓存过期/不完整则触发异步更新
        """
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        cache_key = self._generate_cache_key(db_name, table_name, set_year)

        # 尝试获取缓存元数据
        try:
            ttl = self.redis_engine.ttl(cache_key)
            cache_data = self._fetch_redis_data(cache_key)
        except Exception as e:
            logger.info(f"Redis 连接异常: {e}，直接访问 MySQL")
            return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)

        # 缓存失效处理逻辑
        if ttl < 60 or cache_data.empty:
            self._trigger_async_cache_update(
                cache_key, db_name, table_name, set_year, start_date, end_date, cache_data
            )
            return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)

        # 处理有效缓存数据
        filtered_df = self._filter_by_date_range(cache_data, start_dt, end_dt)
        if not filtered_df.empty:
            return filtered_df

        # 缓存数据不满足查询范围要求
        self._trigger_async_cache_update(
            cache_key, db_name, table_name, set_year, start_date, end_date, cache_data
        )
        return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)

    def set_redis(
            self,
            cache_key: str,
            db_name: str,
            table_name: str,
            set_year: bool,
            start_date,
            end_date,
            existing_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        异步更新 Redis 缓存，合并新旧数据
        """
        try:
            # 从 MySQL 获取新数据
            new_data = self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)
            if new_data.empty:
                return pd.DataFrame()

            # 合并历史数据
            combined_data = self._merge_data(new_data, existing_data)

            # 序列化并存储到 Redis
            serialized_data = self._serialize_data(combined_data)
            self.redis_engine.set(cache_key, serialized_data)
            self.redis_engine.expire(cache_key, self.cache_ttl)

            logger.info(f"缓存更新 {cache_key} | 数据量: {len(combined_data)}")
            return combined_data

        except Exception as e:
            logger.info(f"缓存更新失败: {cache_key} - {str(e)}")
            return pd.DataFrame()

    # Helper Methods ------------------------------------------------

    def _fetch_table_data(
            self,
            db_name: str,
            table_name: str,
            start_date,
            end_date
    ) -> pd.DataFrame:
        """封装 MySQL 数据获取逻辑"""
        try:
            return self.download.data_to_df(
                db_name=db_name,
                table_name=table_name,
                start_date=start_date,
                end_date=end_date,
                projection={}
            )
        except Exception as e:
            logger.info(f"MySQL 查询异常 {db_name}.{table_name}: {e}")
            return pd.DataFrame()

    def _fetch_redis_data(self, cache_key: str) -> pd.DataFrame:
        """从 Redis 获取并解析数据（自动转换日期列）"""
        try:
            data = self.redis_engine.get(cache_key)
            if not data:
                return pd.DataFrame()
            # 反序列化数据
            df = pd.DataFrame(json.loads(data.decode("utf-8")))
            return self._convert_date_columns(df)
        except Exception as e:
            logger.info(f"Redis 数据解析失败 {cache_key}: {e}")
            return pd.DataFrame()

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """统一处理日期列转换"""
        if "日期" in df.columns:
            df["日期"] = pd.to_datetime(df["日期"], format="%Y-%m-%d", errors="coerce")
        return df

    def _generate_cache_key(self, db_name: str, table_name: str, set_year: bool) -> str:
        """生成标准化的缓存键"""
        return f"{db_name}:{table_name}_haveyear" if set_year else f"{db_name}:{table_name}"

    def _filter_by_date_range(
            self,
            df: pd.DataFrame,
            start_dt: datetime.datetime,
            end_dt: datetime.datetime
    ) -> pd.DataFrame:
        """按日期范围筛选数据"""
        if "日期" not in df.columns:
            return df
        date_mask = (df["日期"] >= start_dt) & (df["日期"] <= end_dt)
        return df[date_mask].copy()

    def _trigger_async_cache_update(
            self,
            cache_key: str,
            db_name: str,
            table_name: str,
            set_year: bool,
            start_date: str,
            end_date: str,
            existing_data: pd.DataFrame
    ):
        """启动异步缓存更新线程"""
        thread = threading.Thread(
            target=self.set_redis,
            args=(cache_key, db_name, table_name, set_year, start_date, end_date, existing_data),
            daemon=True
        )
        thread.start()

    def _merge_data(self, new_data: pd.DataFrame, existing_data: pd.DataFrame) -> pd.DataFrame:
        """合并新旧数据集"""
        if existing_data.empty or "日期" not in existing_data.columns:
            return new_data

        new_min = new_data["日期"].min()
        new_max = new_data["日期"].max()
        valid_historical = existing_data[
            (existing_data["日期"] < new_min) | (existing_data["日期"] > new_max)
            ]
        return pd.concat([new_data, valid_historical], ignore_index=True).drop_duplicates(subset=["日期"])

    def _serialize_data(self, df: pd.DataFrame) -> str:
        """序列化 DataFrame 并处理日期类型"""
        temp_df = df.copy()
        date_cols = temp_df.select_dtypes(include=["datetime64[ns]"]).columns
        for col in date_cols:
            temp_df[col] = temp_df[col].dt.strftime("%Y-%m-%d")
        return temp_df.to_json(orient="records", force_ascii=False)


if __name__ == '__main__':
    # # ****************************************************
    # # 这一部分在外部定义，只需要定义一次，开始
    # redis_config = {
    #     'host': '127.0.0.1',
    #     'port': 6379,  # 默认Redis端口
    #     'db': 0,  # 默认Redis数据库索引
    #     # 'username': 'default',
    #     'password': redis_password,
    # }
    # # redis 实例化
    # r = redis.Redis(**redis_config)
    # # mysql 实例化
    # d = s_query.QueryDatas(username=username, password=password, host=host, port=port)
    # # 将两个库的实例化对象传给 RedisData 类，并实例化数据处理引擎
    # m = RedisData(redis_engin=r, download=d)
    # # ****************************************************
    #
    # # 以下为动态获取数据库数据
    # db_name = '聚合数据'
    # table_name = '多店推广场景_按日聚合'
    # set_year = False
    # df = m.get_from_redis(
    #     db_name=db_name,
    #     table_name=table_name,
    #     set_year=set_year,
    #     start_date='2025-01-01',
    #     end_date='2025-01-31'
    # )
    # logger.info(df)
    #

    logger.info(socket.gethostname())
