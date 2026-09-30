# DevWork Instruction

## Registered User 
**Admin Email & Password**
| Email & Password | Value |
| :-----------------: | :-----------------: |
| **Email    :** | rai010303@gmail.com |
| **Password :** | 123123 |

**User Email & Password**
| No | Email & Password | Value |
| :-----------------: | :-----------------: | :-------------------: |
| 1 | **Email    :** | ridwan@gmail.com |
|   | **Password :** | 123123 |
| 2 | **Email    :** | ari123@gmail.com |
|   | **Password :** | 123123 |
| 3 | **Email    :** | adam123@gmail.com |
|   | **Password :** | 123123 |
| 4 | **Email    :** | asd123@gmail.com |
|   | **Password :** | 123123 |

**Notes**
- REFRESH IF THE STYLE IS ERROR (CTRL + SHIFT + R)
- Bootstrap v5.3
- PHP V8.1.6
- xampp v3.3.0
- YT Link : https://youtu.be/bvcH3t3sUyE

## If You Using PHP v8.2.0 with XAMPP v3.3.0 and get this kind of error

A PHP Error was encountered <br />
Severity: 8192 <br />
Message: Creation of dynamic property CI_URI::$config is deprecated <br />
Filename: core/URI.php <br />
Line Number: 101 <br />
Backtrace: <br />
File: C:\xampp\htdocs\app-spp\index.php <br />
Line: 315 <br />
Function: require_once <br />

***SOLUTION***
1. Open File : C:\xampp\htdocs\app-spp\system\core\URI.php <br />
add : #[\AllowDynamicProperties] <br />
before : class CI_URI { <br />

2. Open File : C:\xampp\htdocs\app-spp\system\core\Router.php <br />
add : #[\AllowDynamicProperties] <br />
befores : class CI_Router { <br />

3. Open File : C:\xampp\htdocs\app-spp\system\core\Controller.php <br />
add : #[\AllowDynamicProperties] <br />
before : class CI_Controller { <br />

4. Open File : C:\xampp\htdocs\app-spp\system\database\DB_driver.php <br />
add : #[\AllowDynamicProperties] <br />
before : abstract class CI_DB_driver { <br />

5. Open File : C:\xampp\htdocs\app-spp\system\core\Loader.php <br />
add : #[\AllowDynamicProperties] <br />
before : class CI_Loader { <br />



