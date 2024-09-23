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

def ohe():
    columns = "a, b, c"
    db = duckdb.connect()
    
    sql = f"""
        --create table tmp_data_store as
        with long_form as (
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
        using count(*)
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
    import time
    #time.sleep(2)
    print(db.execute(sql).df())
ohe()