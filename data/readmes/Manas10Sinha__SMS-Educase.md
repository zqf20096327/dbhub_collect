# SMS Educase - School Management APIs

**Live Application:** [https://sms-educase.onrender.com](https://sms-educase.onrender.com)  
**Postman Collection:** [Access Here](https://app.getpostman.com/join-team?invite_code=bded7fe622cc348aa18966a0422b9c966eea96d4ed02734d46dd5aeaff07d6fc&target_code=74964134cd870f16b6386e6a1a4fc0d3)  
**Database (TiDB/MySQL):** [TiDB Cloud SQL Editor](https://tidbcloud.com/clusters/10450075568658030610/sqleditor?orgId=1372813089209275751&projectId=1372813089454593580)

## Objective
Node.js APIs to manage school data: add schools and list schools sorted by proximity to a user location.

## Endpoints

1. **Add School**  
   - `POST /api/addSchool`  
   - Payload: `{ name, address, latitude, longitude }`  

2. **List Schools**  
   - `GET /api/listSchools?lat={latitude}&lng={longitude}`  
   - Returns schools sorted by distance from the provided coordinates.

## Tech Stack
Node.js, Express.js, MySQL (TiDB Cloud)

## Hosting
APIs deployed on Render: [https://sms-educase.onrender.com](https://sms-educase.onrender.com)
