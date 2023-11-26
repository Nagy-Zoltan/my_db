## Usage

Run netcat to establish tcp connection to the database:
```commandline
nc localhost 1234
```
Type one of the commands specified in the next chapter.

## Commands

Create new database:
```commandline
db create "database name"
```
Delete database by name:
```commandline
db drop name "database name"
```
Delete database by id:
```commandline
db drop id "database id"
```
Switch to database by name:
```commandline
db name "database name"
```
Switch to database by id:
```commandline
db id "database id"
```
Get key from database:
```commandline
get "key name"
```
Set key in database:
```commandline
set "key name" "value"
```
Delete key in database:
```commandline
del "key name"
```
Get all keys in database:
```commandline
getall
```


## Examples

See examples in the screenshot.
