### Project3-Benchmarking-openGauss-Against-PostgreSQL

This project researches the differences between OpenGauss and PostgreSql-14.11 in efficiency and safety. It proposes some criteria and key metrics for evaluating the quality of databases and places emphasis on performance in complex data-intensive scenarios. It also gives test code for measuring differences between OpenGauss and PostgreSql-14.11 on these metrics. We executing these code on the elastic cloud server(ECS) and gained some conclusions about the features of OpenGauss. You can recurrence it as directed by [OpenGauss installation and deployment guide](OpenGauss_installation_and_deployment_guide.docx) and [report](report.pdf) in this project.

Here are some of our test results. You can see OpenGauss almost always performs worse than PostgreSql-14.11 in both simple and complex data-intensive scenarios, even in growth ratio this conclusion is true. OpenGauss only has advantages in query with index in extremely complex data-intensive scenarios.

1. Efficiency comparison in insert operations:

![insert1](assets/efficiency%20diagram/insert/insert1.png) | ![insert2](assets/efficiency%20diagram/insert/insert2.png)
---|---

![insert3](assets/efficiency%20diagram/insert/insert3.png)

2. Efficiency comparison in select operations:

![select1](assets/efficiency%20diagram/select/select1.png) | ![select2](assets/efficiency%20diagram/select/select2.png)
---|---

![select3](assets/efficiency%20diagram/select/select3.png)

3. Efficiency comparison in update operations:

![update1](assets/efficiency%20diagram/update/update1.png) | ![update2](assets/efficiency%20diagram/update/update2.png)
---|---

![update3](assets/efficiency%20diagram/update/update3.png)

4. Efficiency comparison in delete operations:

![delete1](assets/efficiency%20diagram/delete/delete1.png) | ![delete2](assets/efficiency%20diagram/delete/delete2.png)
---|---

![delete3](assets/efficiency%20diagram/delete/delete3.png)

5. Efficiency comparison in join operations:

![join1](assets/efficiency%20diagram/join/join1.png) | ![join2](assets/efficiency%20diagram/join/join2.png)
---|---

![join3](assets/efficiency%20diagram/join/join3.png)

6. Efficiency comparison in index operations:

![index1](assets/efficiency%20diagram/index/index1.png) | ![index2](assets/efficiency%20diagram/index/index2.png)
---|---

![index3](assets/efficiency%20diagram/index/index3.png)