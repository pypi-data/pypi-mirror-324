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
from decimal import Decimal

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
    """
    存储 string
    """
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


class RedisDataHash(object):
    """
    存储 hash
    Redis缓存与MySQL数据联合查询处理器

    功能特性：
    - 支持带年份分表的MySQL数据查询
    - 多级缓存策略（内存缓存+Redis缓存）
    - 异步缓存更新机制
    - 自动处理日期范围和数据类型转换
    """

    def __init__(self, redis_engine, download, cache_ttl: int):
        """
        初始化缓存处理器

        :param redis_engine: Redis连接实例
        :param download: 数据下载处理器（需实现data_to_df方法）
        :param cache_ttl: 缓存存活时间（单位：分钟，内部转换为秒存储）
        """
        self.redis_engine = redis_engine
        self.download = download
        self.cache_ttl = cache_ttl * 60  # 转换为秒存储

    def get_from_mysql(
            self,
            db_name: str,
            table_name: str,
            set_year: bool,
            start_date,
            end_date
    ) -> pd.DataFrame:
        """
        从MySQL直接获取数据的核心方法

        处理逻辑：
        1. 当启用年份分表时(set_year=True)，自动遍历2024到当前年份的所有分表
        2. 合并所有符合条件的数据表内容
        3. 自动处理日期列格式转换

        :return: 合并后的DataFrame（可能包含多个分表数据）
        """
        # 原有实现保持不变
        dfs = []
        if set_year:
            # 处理年份分表情况（例如 table_2024, table_2025...）
            current_year = datetime.datetime.today().year
            for year in range(2024, current_year + 1):
                df = self._fetch_table_data(
                    db_name, f"{table_name}_{year}", start_date, end_date
                )
                if df is not None:
                    dfs.append(df)
        else:
            # 单表查询模式
            df = self._fetch_table_data(db_name, table_name, start_date, end_date)
            if df is not None:
                dfs.append(df)

        # 合并结果并处理空数据情况
        combined_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        if combined_df.empty:
            logger.warn(f"warning: {db_name}.{table_name} 未读取到数据")
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
        带缓存策略的数据获取主入口

        执行流程：
        1. 生成缓存键并检查TTL（存活时间）
        2. 当TTL<60秒时触发异步更新，同时直接访问MySQL获取最新数据
        3. 从Redis获取历史数据并进行日期过滤
        4. 若缓存数据不完整，触发异步更新并降级到MySQL查询
        5. 异常时自动降级到MySQL查询

        设计特点：
        - 缓存预热：首次访问时异步更新缓存
        - 降级机制：任何异常自动切换直连MySQL
        - 过时缓存：当TTL不足时并行更新缓存
        """
        # 时分秒部分重置为 00:00:00 这是个巨坑，不可以省略
        start_dt = pd.to_datetime(start_date).floor('D')
        end_dt = pd.to_datetime(end_date).floor('D')
        # 生成缓存键名
        cache_key = self._generate_cache_key(db_name, table_name, set_year)

        try:
            # 检查缓存
            ttl = self.redis_engine.ttl(cache_key)
            if ttl < 60:  # 当剩余时间不足1分钟时触发更新
                # 获取当前缓存
                cache_data = self._fetch_redis_data(cache_key)
                # 异步更新缓存
                self._trigger_async_cache_update(
                    cache_key, db_name, table_name, set_year, start_date, end_date, cache_data
                )
                # 立即降级返回MySQL查询
                return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)

            # 按年份范围获取缓存数据（优化大数据量时的读取效率）
            start_year = start_dt.year
            end_year = end_dt.year
            cache_data = self._fetch_redis_data(cache_key, start_year, end_year)
            # 空数据检查（缓存未命中）
            if cache_data.empty:
                self._trigger_async_cache_update(
                    cache_key, db_name, table_name, set_year, start_date, end_date, cache_data
                )
                return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)
            # 按请求范围过滤数据（应对按年存储的粗粒度缓存）
            filtered_df = self._filter_by_date_range(cache_data, start_dt, end_dt)
            if not filtered_df.empty:
                if '日期' in filtered_df.columns.tolist():
                    # 缓存数据的日期在请求日期范围内时，直接返回缓存数据
                    exsit_min_date = filtered_df['日期'].min()
                    if exsit_min_date <= start_dt:
                        return filtered_df
                else:
                    return filtered_df
            # 缓存数据不完整时触发异步更新缓存
            self._trigger_async_cache_update(
                cache_key, db_name, table_name, set_year, start_date, end_date, cache_data
            )
            # 立即降级返回MySQL查询
            return self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)

        except Exception as e:
            # 异常策略：立即返回MySQL查询，保障服务可用
            logger.error(f"Redis 连接异常: {e}，直接访问 MySQL")
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
    ) -> None:
        """
        异步缓存更新方法

        核心逻辑：
        1. 获取MySQL最新数据
        2. 合并新旧数据（保留历史数据中不在新数据时间范围内的部分）
        3. 智能存储策略：
           - 无日期字段：全量存储到"all"字段
           - 有日期字段：按年份分片存储（提升查询效率）

        设计特点：
        - 增量更新：仅合并必要数据，避免全量覆盖
        - 数据分片：按年存储提升大数据的读取性能
        - 容错处理：跳过无日期字段的异常情况
        """
        try:
            # 获取最新数据（使用最新查询条件）
            new_data = self.get_from_mysql(db_name, table_name, set_year, start_date, end_date)
            if new_data.empty:
                return

            # 合并缓存数据
            combined_data = self._merge_data(new_data, existing_data)

            if not combined_data.empty:
                # 处理无日期字段的特殊情况
                if '日期' not in combined_data.columns.tolist():
                    # 数据序列化
                    serialized_data = self._serialize_data(combined_data)
                    self.redis_engine.hset(cache_key, "all", serialized_data)
                    self.redis_engine.expire(cache_key, self.cache_ttl)
                else:
                    # 按年份分片存储策略
                    combined_data['年份'] = combined_data['日期'].dt.year
                    # 分组存储到Redis哈希的不同字段（例如2024字段存储当年数据）
                    for year, group in combined_data.groupby('年份'):
                        year_str = str(year)
                        serialized_data = self._serialize_data(group.drop(columns=['年份']))
                        self.redis_engine.hset(cache_key, year_str, serialized_data)
                    self.redis_engine.expire(cache_key, self.cache_ttl)
                logger.info(f"缓存更新 {cache_key} | 数据量: {len(combined_data)}")
        except Exception as e:
            logger.error(f"缓存更新失败: {cache_key} - {str(e)}")

    def _fetch_table_data(
            self,
            db_name: str,
            table_name: str,
            start_date,
            end_date
    ) -> pd.DataFrame:
        """执行MySQL查询并返回DataFrame（带异常处理）"""
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

    def _fetch_redis_data(self, cache_key: str, start_year: int = None, end_year: int = None) -> pd.DataFrame:
        """
        从Redis哈希表读取数据

        优化策略：
        - 当指定年份范围时，仅获取相关字段（hmget）
        - 未指定范围时全量获取（hgetall）
        --  从mysql过来的表，虽然没有日期列，但也指定了 start_year/end_year，再redis中存储的键名是"all"，所以要把 all也加进去
        """
        try:
            if start_year is not None and end_year is not None:
                # 按年份范围精确获取字段（提升性能）
                fields = [str(y) for y in range(start_year, end_year + 1)]
                fields += ['all']
                data_list = self.redis_engine.hmget(cache_key, fields)
                dfs = []
                for data, field in zip(data_list, fields):
                    if data:
                        df = pd.DataFrame(json.loads(data.decode("utf-8")))
                        df = self._convert_date_columns(df)
                        dfs.append(df)
                return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
            else:
                # 全量获取模式
                data_dict = self.redis_engine.hgetall(cache_key)
                dfs = []
                for field, data in data_dict.items():
                    try:
                        df = pd.DataFrame(json.loads(data.decode("utf-8")))
                        df = self._convert_date_columns(df)
                        dfs.append(df)
                    except Exception as e:
                        logger.info(f"Redis 数据解析失败 {cache_key} 字段 {field}: {e}")
                return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        except Exception as e:
            logger.info(f"Redis 数据获取失败 {cache_key}: {e}")
            return pd.DataFrame()

    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """统一日期列格式转换"""
        if "日期" in df.columns:
            df["日期"] = pd.to_datetime(df["日期"], format="%Y-%m-%d", errors="coerce")
        return df

    def _generate_cache_key(self, db_name: str, table_name: str, set_year: bool) -> str:
        """生成缓存键名"""
        return f"{db_name}:{table_name}_haveyear" if set_year else f"{db_name}:{table_name}"

    def _filter_by_date_range(
            self,
            df: pd.DataFrame,
            start_dt: datetime.datetime,
            end_dt: datetime.datetime
    ) -> pd.DataFrame:
        """按日期范围精确过滤数据"""
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
        """启动异步线程执行缓存更新（不阻塞主流程）"""
        thread = threading.Thread(
            target=self.set_redis,
            args=(cache_key, db_name, table_name, set_year, start_date, end_date, existing_data),
            daemon=True
        )
        thread.start()

    def _merge_data(self, new_data: pd.DataFrame, existing_data: pd.DataFrame) -> pd.DataFrame:
        """合并新旧数据集策略：保留现有数据中在新数据范围外的历史数据，并按日期排序"""
        if existing_data.empty or "日期" not in existing_data.columns:
            return new_data
        new_data["日期"] = pd.to_datetime(new_data["日期"])
        existing_data["日期"] = pd.to_datetime(existing_data["日期"])

        # 计算新数据日期范围
        new_min = new_data["日期"].min()
        new_max = new_data["日期"].max()

        # 保留现有数据中在新数据范围之外的部分
        valid_historical = existing_data[
            (existing_data["日期"] < new_min) | (existing_data["日期"] > new_max)
            ]
        merged_data = pd.concat([new_data, valid_historical], ignore_index=True)
        merged_data.sort_values(['日期'], ascending=[False], ignore_index=True, inplace=True)
        return merged_data

    def _serialize_data(self, df: pd.DataFrame) -> bytes:
        """
        高性能数据序列化方法

        处理要点：
        1. 日期类型转换为字符串
        2. Decimal类型转换为浮点数
        3. NaN值统一转换为None
        4. 优化JSON序列化性能
        """
        if df.empty:
            return json.dumps([], ensure_ascii=False).encode("utf-8")
        temp_df = df.copy()

        # 处理日期类型列（安全转换）
        date_cols = temp_df.select_dtypes(include=["datetime64[ns]"]).columns
        for col in date_cols:
            # 处理全NaT列避免类型错误
            if temp_df[col].isna().all():
                temp_df[col] = temp_df[col].astype(object)  # 转换为object类型避免NaT
            temp_df[col] = (
                temp_df[col]
                .dt.strftime("%Y-%m-%d")  # 安全使用dt访问器（因类型强制为datetime）
                .where(temp_df[col].notna(), None)
            )

        # 统一空值处理（保护全None列类型）
        def safe_null_convert(series):
            """保留全None列的原始dtype"""
            if series.isna().all():
                return series.astype(object).where(pd.notnull(series), None)
            return series.where(pd.notnull(series), None)

        temp_df = temp_df.apply(safe_null_convert)

        # 类型处理函数（增强嵌套结构处理）
        def decimal_serializer(obj):
            """递归序列化处理"""
            # 提前处理None值
            if obj is None:
                return None

            # 按类型分发处理
            if isinstance(obj, Decimal):
                return round(float(obj), 6)
            elif isinstance(obj, pd.Timestamp):
                return obj.strftime("%Y-%m-%d %H:%M:%S")  # 兜底处理漏网之鱼
            elif isinstance(obj, np.generic):  # 处理所有numpy标量类型
                return obj.item()
            elif isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            elif isinstance(obj, (list, tuple, set)):
                return [decimal_serializer(item) for item in obj]
            elif isinstance(obj, dict):
                return {decimal_serializer(k): decimal_serializer(v) for k, v in obj.items()}
            elif isinstance(obj, bytes):
                return obj.decode("utf-8", errors="replace")  # 二进制安全处理
            elif isinstance(obj, pd.Series):  # 防止意外传入Series对象
                return obj.to_list()
            else:
                # 尝试直接转换可序列化类型
                try:
                    json.dumps(obj)
                    return obj
                except TypeError:
                    logger.error(f"无法序列化类型 {type(obj)}: {str(obj)}")
                    raise

        # 序列化前防御性检查
        try:
            data_records = temp_df.to_dict(orient="records")
        except Exception as e:
            logger.error(f"数据转换字典失败: {str(e)}")
            raise

        # 空记录特殊处理
        if not data_records:
            return json.dumps([], ensure_ascii=False).encode("utf-8")

        # 执行序列化
        try:
            return json.dumps(
                data_records,
                ensure_ascii=False,
                default=decimal_serializer
            ).encode("utf-8")
        except TypeError as e:
            logger.error(f"序列化失败，请检查未处理的数据类型: {str(e)}")
            raise


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
