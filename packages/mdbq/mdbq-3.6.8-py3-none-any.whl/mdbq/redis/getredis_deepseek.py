# -*- coding: UTF-8 –*-
import redis
import socket
from mdbq.mysql import s_query
from mdbq.config import myconfig
import pandas as pd
import json
import datetime
import threading


if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
    conf = myconfig.main()
    conf_data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    redis_password = conf['Windows']['company']['redis']['local']['password']
# elif socket.gethostname() == 'MacBook-Pro.local':
#     conf = myconfig.main()
#     conf_data = conf['Windows']['xigua_lx']['mysql']['local']
#     username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
#     redis_password = conf['Windows']['company']['redis']['local']['password']
else:
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    redis_password = conf['Windows']['company']['redis']['local']['password']  # redis 使用本地数据，全部机子相同


class RedisData:
    def __init__(self, redis_engine, download, cache_ttl: int = 60):
        """
        初始化Redis数据处理对象

        :param redis_engine: Redis连接引擎
        :param download: 数据库下载处理器
        :param cache_ttl: 缓存过期时间（分钟）
        """
        self.redis_engine = redis_engine
        self.download = download
        self.cache_ttl = cache_ttl * 60  # 转换为秒
        self.lock = threading.Lock()  # 线程锁

    def _handle_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """统一处理日期列转换"""
        if '日期' in df.columns:
            df['日期'] = pd.to_datetime(df['日期'], errors='coerce', format='%Y-%m-%d')
        return df

    def get_from_mysql(self, db_name: str, table_name: str,
                       start_date, end_date,
                       set_year: bool) -> pd.DataFrame:
        """
        从MySQL获取数据

        :param set_year: 是否按年份分表
        """
        try:
            if set_year:
                current_year = datetime.datetime.now().year
                dfs = []
                # 动态获取需要查询的年份范围
                min_year = min(2024, pd.to_datetime(start_date).year)  # 根据实际需求调整
                for year in range(min_year, current_year + 1):
                    table = f"{table_name}_{year}"
                    df = self.download.data_to_df(
                        db_name=db_name,
                        table_name=table,
                        start_date=start_date,
                        end_date=end_date,
                        projection={}
                    )
                    if not df.empty:
                        dfs.append(df)
                _df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
            else:
                _df = self.download.data_to_df(
                    db_name=db_name,
                    table_name=table_name,
                    start_date=start_date,
                    end_date=end_date,
                    projection={}
                )

            if _df.empty:
                print(f"空数据 - {db_name}.{table_name}")
                return pd.DataFrame()

            return self._handle_datetime_columns(_df)

        except Exception as e:
            print(f"MySQL查询失败: {str(e)}")
            return pd.DataFrame()

    def get_from_redis(self, db_name: str, table_name: str,
                       start_date, end_date,
                       set_year: bool) -> pd.DataFrame:
        """
        从Redis获取数据（带自动缓存更新）
        """
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)

        # 生成统一缓存键
        cache_key = f"{db_name}:{table_name}{'_year' if set_year else ''}"

        try:
            # 检查缓存状态
            with self.lock:  # 保证线程安全
                ttl = self.redis_engine.ttl(cache_key)

                if ttl < 300:  # 剩余时间小于5分钟时触发更新
                    print(f"异步缓存更新: {cache_key}")
                    threading.Thread(
                        target=self._update_cache,
                        args=(cache_key, db_name, table_name,
                              start_date, end_date, set_year),
                        daemon=True
                    ).start()

            # 获取缓存数据
            cached_data = self.redis_engine.get(cache_key)
            if not cached_data:
                return self._fallback_to_mysql(db_name, table_name,
                                               start_date, end_date, set_year)
            json_str = cached_data.decode('utf-8')
            _df = pd.read_json(json_str, orient='records')
            _df = self._handle_datetime_columns(_df)

            # 数据范围校验
            if '日期' in _df.columns:
                cache_min = _df['日期'].min()
                cache_max = _df['日期'].max()

                # 请求范围超出缓存范围时需要更新
                if start_dt < cache_min or end_dt > cache_max:
                    print(f"请求范围超出缓存 {start_dt.strftime('%Y-%m-%d ')} - {end_dt.strftime('%Y-%m-%d ')}")
                    self._update_cache(cache_key, db_name, table_name,
                                       start_date, end_date, set_year, _df)
                    return self._fallback_to_mysql(db_name, table_name,
                                                   start_date, end_date, set_year)

                return _df[(start_dt <= _df['日期']) & (_df['日期'] <= end_dt)]
            return _df

        except Exception as e:
            print(f"Redis操作失败: {str(e)}")
            return self._fallback_to_mysql(db_name, table_name,
                                           start_date, end_date, set_year)

    def _update_cache(self, cache_key: str, db_name: str, table_name: str,
                      start_date: str, end_date: str, set_year: bool,
                      existing_df: pd.DataFrame = None) -> None:
        """缓存更新核心逻辑"""
        try:
            # 获取最新数据
            new_data = self.get_from_mysql(
                db_name=db_name,
                table_name=table_name,
                start_date=start_date,
                end_date=end_date,
                set_year=set_year
            )

            # 合并历史数据
            if existing_df is not None and not new_data.empty:
                combined = pd.concat([existing_df, new_data], ignore_index=True)
                combined = combined.drop_duplicates(subset='日期', keep='last')
            else:
                combined = new_data

            if not combined.empty:
                # 转换日期类型为字符串
                temp_df = combined.copy()
                datetime_cols = temp_df.select_dtypes(include=['datetime64[ns]']).columns
                temp_df[datetime_cols] = temp_df[datetime_cols].astype(str)

                # 存储到Redis
                with self.lock:
                    self.redis_engine.set(
                        cache_key,
                        temp_df.to_json(orient='records', force_ascii=False),
                        ex=self.cache_ttl
                    )
                print(f"缓存更新成功: {cache_key} | 记录数: {len(combined)}")

        except Exception as e:
            print(f"缓存更新失败: {str(e)}")

    def _fallback_to_mysql(self, db_name: str, table_name: str,
                           start_date: str, end_date: str,
                           set_year: bool) -> pd.DataFrame:
        """降级到直接MySQL查询"""
        print(f"降级到MySQL查询: {db_name}.{table_name}")
        return self.get_from_mysql(
            db_name=db_name,
            table_name=table_name,
            start_date=start_date,
            end_date=end_date,
            set_year=set_year
        )


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
    #     _db_name=db_name,
    #     _table_name=table_name,
    #     _set_year=set_year,
    #     start_date='2025-01-01',
    #     end_date='2025-01-31'
    # )
    # print(df)
    #

    print(socket.gethostname())
