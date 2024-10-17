import pandas as pd
import polars as pl

import feature_engine

import duckdb


x = pd.DataFrame({
    'id': [1,2,3,4,5,6],
    'a': [str(x) for x in [1,2,3,1,2,3]],
    'b': [str(x) for x in [1,2,1,2,1,2]],
    'c': ['o','p','q','r','s','t'],
})
#https://sekuel.com/sql-courses/duckdb-cookbook/correlation-matrix-duckdb/

rows = 100_000
kv = {
    chr(i+65): list([str(x%i) for x in range(rows)]) 
    #i: list([str(x%i) for x in range(rows)]),
    #i: list([chr(x%26+65) for x in range(rows)]),
    for i in range(2,23)
}
kv['id'] = list(range(rows))
x = pd.DataFrame(kv)


"""
# https://stackoverflow.com/questions/15274305/is-it-possible-to-have-multiple-pivots-using-the-same-pivot-column-using-sql-ser
# https://duckdb.org/docs/sql/statements/pivot.html
# https://www.reddit.com/r/SQL/comments/ul4hth/one_hot_encoding_through_sql/

"""

def pdf():
    print(
        duckdb.sql("""
            pivot x
            on a
            using count(*)
            group by id
            order by id
        """)
    )
def bprint(*args, **kwargs):
    print("=================")
    print(*args, **kwargs)
    print("=================")

from functools import wraps
import time 
def time_it(func):
    @wraps(func)
    def with_timing(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        e = time.time()
        bprint(e-s)
        return res
    return with_timing

@time_it
def ohe():
    columns = ','.join([c for c in x.columns if c != 'id'])
    print(columns)
    db = duckdb.connect()
    
    sql = f"""
        --create table tmp_data_store as
        explain analyze with long_form as (
            unpivot x
            on {columns}
            into
                NAME categorical_col_name
                VALUE value
        )
        , transformed_kv as (
            select * exclude(categorical_col_name, value), categorical_col_name || '__' ||cast(value as varchar) as kv 
            from long_form
        )
        pivot transformed_kv
        on kv 
        using bool_or(id>0)
        group by id
        order by id;

        --select * from tmp_data_store
    """
    
    if False: # Enable to run sql statement-by-statement to workaround https://github.com/duckdb/duckdb/issues/13863
        print(sql)
        stmts = db.extract_statements(sql)
        print(stmts)
        for stmt in stmts[:-1]:
            print(stmt)
            print(db.sql(stmt.query))
        sql = stmts[-1].query
    memo_sql = "SELECT value AS memlimit FROM duckdb_settings() WHERE name = 'memory_limit';"
    change_memo_sql = "SET memory_limit = '20GiB';"
    change_memo_back_sql = "SET memory_limit = '12.1GiB';"
    db.execute(change_memo_sql)
    
    print(db.execute(memo_sql).df())
    
    res = db.sql(sql).show(max_width=250)#.df()
    #print(sorted(res.columns))
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(res)
    
    db.execute(change_memo_back_sql)

    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    print(res)

ohe()

@time_it
def ohe_pd():
    res = pd.get_dummies(x.drop(columns = 'id'))
    bprint(res.tail())
ohe_pd()
#https://stackoverflow.com/questions/68429779/is-there-a-way-to-make-get-dummies-work-faster