A simple evaluation for openGauss mainly on the concurrency performance

Before using the code given in this repository, you should first pull the docker image of opengauss.

Here are the function for each code:

1. connected_to_postgresSQL: using java to connect to the postgresSQL and constructs multiple concurrent query requests using java.util.concurrent, returning the time required to process the request
2. connected_to_gauss: using java to connect to the opengauss and constructs multiple concurrent query requests using java.util.concurrent, returning the time required to process the request
3. get_info_postgresSQL: connection is the same as connected_to_postgresSQL, then using the SQL query "SELECT datname, numbackends, xact_commit, xact_rollback, blks_read, blks_hit, tup_returned, tup_fetched FROM pg_stat_database" to get the infomation about the using of resourses.
4. get_info_gauss: connection is the same as connected_to_gauss, then using the SQL query "SELECT datname, numbackends, xact_commit, xact_rollback, blks_read, blks_hit, tup_returned, tup_fetched FROM pg_stat_database" to get the infomation about the using of resourses.

To make the comparison more credible, I'll try to keep the two java codes identical except for the part that connects to the database.
