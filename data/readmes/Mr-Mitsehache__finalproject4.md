#update git
1. git add .
2. git commit -m "detail" //save in my PC
3. git push //update in Github

#run first Project
npm i 
npm run dev
npx prisma migrate dev --name init
npm run db:seed

    #--- Main ---#
    1.Auth(S)✅
    2.DataBase(Succes)✅
    3.Navbar() ปรับให้ล็อกอินแล้วแสดงTab ล็อกเอาท์ไม่ย้ายหน้า
    4.post-login(/app/post-login) เพิ่มหน้าloading

    #--- User ---#
    1.Homepage(/app/store) เหลือตกแต่ง ย้ายไปเป็นหน้าแรก -> ( /app/ )
    2.Storepage(/app/store/[id]) เหลื่อตกแต่ง ดึงข้อมูลมาให้ครบ 
    3.Paymentpage(Working) เหลื่อตกแต่ง 

    #--- Store ---#
    1.Storepage(/app/organiza/[id]) เหลื่อตกแต่ง ดึงข้อมูลมาให้ครบ CRUD
    2.Dashboardpage(N)
    3.Managepage(N) ยังก่อน
    4.Task(N)

    #--- Admin ---#
    1.Dashboardpage(N)
    2.Managepage(N)
    3.Verifypage(N)

# เพิ่มเติม
--> ล้างฐานข้อมูล + apply migrations ใหม่ทั้งหมด + รัน seed <--
npx prisma migrate reset
