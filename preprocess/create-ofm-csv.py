# Pre-process data for app

import psrcelmerpy

# connect to Elmer
e_conn = psrcelmerpy.ElmerConn()

# combine intercensal and post-censal data
sql_query = """SELECT a.publication_dim_id, a.estimate_year, HU = SUM(a.housing_units), OHU = SUM(a.occupied_housing_units), GQPOP = SUM(a.group_quarters_population), HHPOP = SUM(a.household_population)
                    FROM ofm.estimate_facts AS a
                    WHERE a.publication_dim_id = 10 AND a.estimate_year BETWEEN 2020 AND 2024
                    GROUP BY a.estimate_year, a.publication_dim_id
                    UNION ALL
                    SELECT a.publication_dim_id, a.estimate_year, HU = SUM(a.housing_units), OHU = SUM(a.occupied_housing_units), GQPOP = SUM(a.group_quarters_population), HHPOP = SUM(a.household_population)
                    FROM ofm.estimate_facts AS a
                    WHERE a.publication_dim_id = 11 AND a.estimate_year BETWEEN 2010 AND 2019
                    GROUP BY a.estimate_year, a.publication_dim_id
                    ORDER BY estimate_year
                    ;
            """

df = e_conn.get_query(sql_query)

# export data as csv
df.to_csv(r"C:\Users\CLam\github\shiny-py\data\ofm-estimates.csv", index=False)
