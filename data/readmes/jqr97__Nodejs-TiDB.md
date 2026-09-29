# Steps to setup prisma ORM
1. initialize a Node.js project and add the Prisma CLI as a development dependency to it

        npm init -y
        npm install prisma --save-dev

2. invoke the Prisma CLI by prefixing it with npx
        
        npx prisma

3. set up your Prisma project by creating your Prisma schema file with the following command:

        npx prisma init

# Connect to the database

4. change the provider = in prisma/schema.prisma file:

    provider = "mysql"

5. change the .env file:
    
    DATABASE_URL="mysql://[username]:[password]@[hostip url]:[port number]/[database name]"

6. Introspect the database
    
    run the following code in terminal:
        
        npx prisma db pull
        
7. Install the Prisma API:

    run the following code in terminal:
    
        npm install @prisma/client
        
        npx prisma generate
