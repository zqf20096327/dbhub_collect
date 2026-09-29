# regression_detection
A tool to identify regression issues in TiDB repo. It is a automation framework to identify a regression path with an given sql testcase.

# Simple way to use
## Prerequisite
- The testcase can be covered in a .sql file.
- The expected test results needs to be constant. For example, test result with up-to-date time value would be treated as a failure.
  
## Required Files
1. Clone TiDB repo to local.
2. Clone regression_detection to local.
3. Install tiup : curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
## Prepare
1. Edit detect.config in regression_detection
- cd regression_detection
- cp detect.config.example detect.config
- Make sure the following paratmers are configured properly. 
> 
> source=issue # Prefix in testcase folder
> 
> issue=52217 # Target issue number
> 
> max_attempts=1 # Maximum detection retries for a falky test.
>
> REGRESSION_DETECT_ROOT="/xxx/regression_detection/" # Path to the regression_detect root
> 
> TEST_SCRIPT_ROOT="/xxx/regression_detection/testcase" # Path to the regression_detect testcase folder
> 
> TIDB_LOC="/xxx/tidb" # Path to the tidb folder
> 
> TIUP_DATA_DIR="/Users/xxx/.tiup/data" # Path to the tiup data folder
2. Create a testcase: This operation would create the files needed for a testcase to detect regression. 
- cd regression_detection
- ./createtest.sh issue 52217
- Edit testcase/${source}${issue}_testcase.sql, please make sure a drop table command is added at the very beginning of a testcase.
> Please refer to [issue52217_testcase.sql](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/issue52217_testcase.sql) for reference.
- Fill in testcase/${source}${issue}.result. [Example-issue52217.result](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/issue52217.result). Bring up an release which could provide the expected results, say v7.5.0 for 52217. Sometimes it is hard to tell which is the right release to bring up. We could refer to the result by mysql8 instead.

## Release detection
- We need to identify the behavior of the testcase among releases and find out when the regression start to happen.
1. Run regression_detect_release.sh
+ The script would bring up releases specifed in the array ${versions} and string ${versions_name} in detect.config. Execute the testcase and check the results.
2. Check [tiup-check-status-${versions_name}-issue-52217.log](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/tiup-check-status-versions_master-issue-52217.log) and [tiup-check-full-${versions_name}-issue-52217.log](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/tiup-check-full-versions_master-issue-52217.log) to determine the test run status.
+ In the case of issue 52217, the testcase failed on releases prior to v7.5.0 since the grammar in testcase was not supported. It was successful in v7.6.0. Then the regression started to happen in v8.0.0 and nightly.
+ So the good label is v7.6.0 and the first bad label is v8.0.0. The pr caused this regression should be a commit between v7.6.0 and v8.0.0.

## Regression Commit 
1. Edit [testcase/${source}${issue}.config](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/issue52217.config) basd on the information so far.
+ Please make sure ${GOOD_COMMIT} and ${BAD_COMMIT} are configured based on the info according to release detection above.
+ For flaky tests, make sure ${max_attempts} is large enough to catch the failure.
2. Run regression_detect_main.sh. It detects the regression causing PR via git bisect.
3. Check [testcase/${source}${issue}/bisect-status-${source}-${issue}.log](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/bisect-status-issue-52217.log) to find out the first bad commit. If you need to double check the execution, please refer to the [full log](https://github.com/kennedy8312/regression_detection/blob/main/testcase/issue52217/bisect-full-issue-52217.log). 
