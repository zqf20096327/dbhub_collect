# BookStore fullstack web application

![Snippet screenshot](./README_assets/snippet_for_readme.jpg)



## Fully functional web application fullstack project

This project is a part of my personal portfolio and is designed to accumulate and demonstrate 
technical stack that I have learned throughout my coding journey.

It is a fully complete and functional example of online bookstore library and shop. 
User can browse through various web app pages in order to search for books, 
checkout books, leave reviews and ratings and so on.
Design of the website is completely done by me as well as the book covers design etc.


### Technical stack

<br>

<div align="center">

<img src="README_assets/java.svg" width="55" height="55" alt="java">
<img src="README_assets/ts.svg" width="55" height="55" alt="ts">
<img src="README_assets/html.svg" width="55" height="55" alt="html">
<img src="README_assets/css.svg" width="55" height="55" alt="css">
<img src="README_assets/spring.svg" width="55" height="55" alt="spring">
<img src="README_assets/reactjs.svg" width="55" height="55" alt="react">
<img src="README_assets/hibernate.svg" width="55" height="55" alt="hibernate">
<img src="README_assets/postgresql.svg" width="55" height="55" alt="postgresql">
<img src="README_assets/tailwind.svg" width="55" height="55" alt="tw">
<img src="README_assets/docker.svg" width="55" height="55" alt="docker">
<img src="README_assets/swagger.svg" width="55" height="55" alt="swagger">
<img src="README_assets/openapi.svg" width="55" height="55" alt="openapi">
<img src="README_assets/stripe.svg" width="55" height="55" alt="stripe">
<img src="README_assets/git.svg" width="55" height="55" alt="git">

</div>

<br>

* Programming and markup languages: **Java, TypeScript, HTML, CSS** 
* Frameworks and libraries: **Spring Framework, ReactJS, Hibernate, Tailwind** 
* Testing tools: **JUnit, AssertJ, Mockito, Testcontainers**
* Database and other tools: **PostgreSQL, Docker, Stripe, Git, OpenAPI, Swagger**

**Deployed version** - [coming soon]()



## Brief overview of structure and functionality


### General project structure

This project consists of **two major parts**, as could be seen in the folder structure.

* **Backend** - REST API server-side application written in Java with usage of 
Spring Framework and PostgreSQL database.

* **Frontend** - Client side web application written in Typescript with usage of 
React and various additional tools like Tailwind etc.

**PostgreSQL** is used as DataBase system for server side to store all the data required for the application.

**Docker** containerization system is implemented to allow easy build and 
test run on any environment if required.

**Stripe payment** service is applied for processing payments made by users of the website. 


### General project functionality

In order to follow best practices I have implemented some common functionalities throughout this project.
Following is a brief description of those functionalities:

* **Authentication & Authorization** - implemented by using **Spring Security in conjunction with JWT** 
technologies. Only "Home", "Search" and few other pages are available to unauthenticated users. 
Other user-specific pages and application functions are available only after authentication.
Users are able to **Log in** and **Register** to the service. **JWTs** are generated via backend API 
and sent to user's frontend client, and then validated by backend each time a user tries to 
access any secured endpoint. **Admin** page and functionality is only available for **authorized** users. 
All user information including **authority** is stored in database after registration and encoded into JWT.


* **Pagination** - pagination logic is implemented for both frontend and backend, and is used on various 
website pages that fetch / show big amount of items to make appearance more user-friendly. For example, 
pagination is used on "Search" page, "History" page, "All book reviews" page and so on.


* **Books search** - search mechanism of the application allows users to search through all the books 
available at the store either **by title** or **by genre**.


* **Book checkout** - allows user to check out (rent) any book that is available and in stock. 
User gets the book displayed on the "shelf", and the book's "copies available" count gets decreased. 
The book is then available for 7 days free of charge. If user has any outdated books, checkout functionality 
becomes unavailable until outstanding fees are paid.


* **Bookshelf management** - shelf page provides a user with ability to manage current loans or 
display previous loans history. Current loans total count is limited, so only 5 books can be simultaneously
checked out by each user. Management functions are as follows:
  * **Renew loan** - allows user to renew loan expiry date back to 7 days from the current moment. 
  Only available if user has no outdated loans or fees pending.
  * **Return book** - allows user to return the book back to the store. 
  No fee is created unless returned book was overdue at the moment. Book's "copies available" value
  gets increased.
  * **History tab** - displays all records of previously checked books. Can be used to track the list 
  of books read by user.


* **Book's reviews and ratings** - functionality that allows users to leave a review for any book.
User is encouraged to **rate the book and leave a comment**. A review can be created without the comment text
while rating is required.
  * **Book's rating** will be fetched as an average among all book's reviews and shown on book's specific page.
  * **Latest reviews** are shown on the bottom of book's specific page as well.
  * **All book's reviews** are available for the user on a separate page that can be accessed from book's 
  specific page.


* **Discussions service** - allows users to open private discussions with administration. 
  * **New discussion tab** - user is encouraged to **open a discussion on any topic** and leave a message for 
  administration. This discussion can later be answered and closed by admin.
  * **All discussions tab** - provides a list of all person's discussions. Discussions answered by 
  administration are marked as "closed" and have admin reply attached, others are marked as "pending reply".
 

* **Payment service** - implemented by using **Stripe Payments** service as payment processor. Functionality 
allows users to pay outstanding fees. User enters credit card information and payment request with certain 
amount is created and processed by Stripe system. All **receipts** are available for application owner within 
his Stripe account and also are automatically sent to users via e-mail by Stripe. As this is a pet project for 
portfolio, a banner with test credit card info is present right on the payment page allowing user to test 
payment functionality without entering any valid credit card information.


* **Administration tools** - allows **authorized** users access to management instruments, such as adding 
or deleting books, changing item quantities, closing discussions etc.
  * **Add book tab** - provides a form for administrator to **create a new book item** and add it to the 
  database. Each book must contain "title", "author", "description", "copies", "copies available", 
  "cover image", "list of genres" fields filled out in order to be added to the database.
  * **Quantities tab** - displays a list of all book items available in the database and allows authorized 
  admin user to change "copies available" count of any book (increase or decrease) or to delete a book 
  completely.
  * **Discussions tab** -  displays a list of all open discussions and allows authorized admin user to add 
  administration response to any discussion and thus close it.



## Testing

Backend API part of the project is covered by tests. There are **unit tests** and **integration tests** 
to cover full API functionality as follows:

* **Unit tests** are written to cover:
  * **Repository layer** - covered 100% of used default and custom methods using JUnit, Mockito and 
  AssertJ provided by Spring Boot starter test package and embedded H2 autoconfigured test DB.
  * **Service layer** - covered ~95% of code by unit tests using JUnit, Mockito and AssertJ provided by 
  Spring Boot starter test package.
  * **Controller layer** - covered 100% of code by unit tests using JUnit, Mockito and AssertJ provided by 
  Spring Boot starter test package.


* **Integration tests** are written to cover end-to-end scenarios of application's expected behaviour.
Those tests use **Testcontainers** library to bootstrap **PostgreQSL** test DB container for each controller 
test class and **TestRestTemplate** to execute HTTP requests and run basic scenarios to simulate normal app
functionality. All API endpoints are 100% tested for expected successful results (2XX status codes) and 
all handled exceptions and most predictable errors (4XX status codes) throughout the project.

**NOTE:** All integration tests use **Testcontainers** and are marked with `@Disabled` JUnit annotation 
to avoid running them during Maven build with Docker compose. This is done because Testcontainers require 
valid running Docker environment to bootstrap postgre container, which is very problematic to achieve from 
inside another docker container while composing project's Docker image during docker compose script execution.



## REST API endpoints and Client routes

This project's backend API documentation is autogenerated and available by means of **OpenAPI & Swagger**.

You can easily access and test all the endpoints with brief descriptions via your browser after starting the
application by navigating to `http://localhost:8080/swagger-ui/index.html` in your browser. All logic related
to generating and describing documentation is mainly configured within backend project's 
`.../openapi/OpenApiConfiguration.java` file and throughout controllers.

Additionally, following is the list of all endpoints available within the project with short descriptions.


### Back-end

#### Open (unauthenticated) endpoints

Following is the list of endpoints that **do not require authentication** and are available to all users.


##### GET

* `.../api/books?page={pageNumber}&books-per-page={itemsPerPage}` - get paginated list of all books.


* `.../api/books/{bookId}` - get a book with `id` passed as a path variable.


* `.../api/books/search/by-title?page={pageNumber}&books-per-page={itemsPerPage}&title-query={titleQuery}` -
get paginated list of all books with `title` value containing `titleQuery` value from url param.


* `.../api/books/search/by-genre?page={pageNumber}&books-per-page={itemsPerPage}&genre-query={genreQuery}` -
get paginated list of all books with `genres` value containing `genreQuery` value from url param.


* `.../api/genres` - get a list of all genres.


* `.../api/reviews/{bookId}?page={pageNumber}&reviews-per-page={itemsPerPage}&latest={true/false}` - get
paginated list of all reviews for the book with `id` passed as a path variable. If `latest` is set to `true` 
then returned list is sorted by reviews `id` value in descending order.


* `.../api/reviews/average-rating/{bookId}` - get book's average rating, calculated from all book's reviews.


##### POST

* `.../api/auth/register` - register (create) a new user. This request will generate and return **JWT** that
  is used to access all secure endpoints of the application. Requires a valid personRegistrationDTO passed
  as a request body:

  ```json
  {
    "firstName": "Person first name",
    "lastName": "Person last name",
    "dateOfBirth": "1990-11-21",
    "email": "userEmail@email.com",
    "password": "userPassword"
  }
  ```


* `.../api/auth/authenticate` - log in to the service using your credentials. This request will generate
  and return **JWT** that is used to access all secure endpoints of the application. Requires a valid
  personLoginDTO passed as a request body:

  ```json
  {
    "email": "userEmail@email.com",
    "password": "userPassword"
  }
  ```


#### Secured (authenticated) endpoints

Following is the list of endpoints that **require authentication** and are available only to authenticated users.

All following endpoints **require JWT** passed as `Authorization` header (Bearer token).

##### GET

* `.../api/admin/secure/open-discussions?page={pageNumber}&discussions-per-page={itemsPerPage}` - get
  paginated list of all open discussions.


* `.../api/books/secure/is-checked-out/{bookId}` - check if a book with `id` passed as a path variable is
  currently checked out by user.


* `.../api/books/secure/is-reviewed/{bookId}` - check if a book with `id` passed as a path variable is
  already reviewed by user.


* `...api/checkouts/secure/current-loans-count` - get the amount of user's current checkouts.


* `...api/checkouts/secure/current-checkouts` - get a list of all user's current checkouts.


* `.../api/discussions/secure?page={pageNumber}&discussions-per-page={itemsPerPage}` - get paginated list
  of all person's discussions.


* `.../api/history-records/secure?page={pageNumber}&records-per-page={itemsPerPage}` - get paginated list
  of all person's history records.


* `.../api/payment/secure` - get the amount of person's current fees pending.


##### POST

* `.../api/admin/secure/add-book` - add new book to database. Requires a valid bookDTO passed as a request body:
  ```json
  { 
    "title": "Book title",
    "author": "Author Name",
    "description": "Book description",
    "copies": 10,
    "copiesAvailable": 10,
    "img": "data:image/jpeg;base64,/9j/4AAQS...",
    "genres": [
      {"description": "Science Fiction"},
      {"description": "Fantasy"},
      {"description": "Romance"}
    ]
  }
  ```


* `.../api/books/secure/review/{bookId}` - add a review for a book with `id` passed as a path variable. Requires 
a valid reviewDTO passed as a request body:

  ```json
  {
    "date": "2023-11-21T12:54:59.841",
    "rating": 4.5,
    "reviewDescription": "Comment message"
  }
  ```


* `.../api/discussions/secure/add-discussion` - add new open discussion. Requires a valid discussionDTO passed 
as a request body:

  ```json
  {
    "title": "Discussion title (subject)",
    "question": "Discussion question"
  }
  ```


* `.../api/payment/secure/payment-intent` - create payment intent via Stripe. Requires a valid paymentInfoDTO 
passed as a request body:

  ```json
  {
    "amount": 23,
    "currency": "USD",
    "receiptEmail": "userEmail@email.com"
  }
  ```


##### PUT

* `.../api/books/secure/checkout/{bookId}` - check out the book with `id` passed as a path variable.


* `.../api/books/secure/renew-checkout/{bookId}` - renew existing checkout of a book with `id` passed as
a path variable.


* `.../api/books/secure/return/{bookId}` - return the book with `id` passed as a path variable.


* `.../api/payment/secure/payment-complete` - reset user's fees pending amount to 0 after payment is
successfully complete.


##### PATCH

* `.../api/admin/secure/increase-quantity/{bookId}` - increase `copies` & `copiesAvailable` values
  of the book with `id` passed as a path variable by 1.


* `.../api/admin/secure/decrease-quantity/{bookId}` - decrease `copies` & `copiesAvailable` values
  of the book with `id` passed as a path variable by 1.


* `.../api/admin/secure/close-discussion` - add an administration response to any open discussion and
  close that discussion. Requires a valid discussionDTO passed as a request body:

  ```json
  { 
    "id": 1,
    "personEmail": "Person e-mail",
    "personFirstName": "Person first name",
    "personLastName": "Person last name",
    "title": "Discussion title (subject)",
    "question": "Discussion question",
    "adminEmail": "Administrator user e-mail",
    "response": "Administration response message",
    "closed": true
  }
  ```


##### DELETE

* `.../api/admin/secure/delete-book/{bookId}` - delete the book with `id` passed as a path variable 
from database.


### Front-end

Following are the routes available on front-end client application:

* `.../` - base url, redirects user to `.../home`;


* `.../home` - navigate to Home page;


* `.../search` - navigate to Search page;


* `.../book/:bookId` - navigate to specific Book page;


* `.../reviews/:bookId` - navigate to all reviews for specific book page;


* `.../shelf` - navigate to Shelf page;


* `.../discussions` - navigate to Discussions page;


* `.../fees` - navigate to Payment page;


* `.../admin` - navigate to Admin page;


* `.../login` - navigate to Login page;


* `.../register` - navigate to Register page;



## Additional libraries and APIs

This project is mostly a typical full-stack application powered by popular developing tools. For example, 
backend application is build with **Spring Boot 3** and uses main features of Spring REST, Spring JPA, 
Spring Security etc. Frontend application is created as **Vite + React + TypeScript** project and mostly 
uses ReactJS functionality.

However, a few extra libraries / dependencies were used in both frontend and backend applications. 
Below is a brief description of those libraries.


### Back-end

#### JWT

Backend REST API application uses Spring Security in conjunction with JWT for authentication & authorization.

All logic related to generating, issuing and validating JWTs is written manually with use of:
* **[io.jsonwebtoken ---> jjwt-api](https://mvnrepository.com/artifact/io.jsonwebtoken/jjwt-api)**;
* **[io.jsonwebtoken ---> jjwt-impl](https://mvnrepository.com/artifact/io.jsonwebtoken/jjwt-impl)**;
* **[io.jsonwebtoken ---> jjwt-jackson](https://mvnrepository.com/artifact/io.jsonwebtoken/jjwt-jackson)**

Maven dependencies are available via links above.

#### OpenAPI & Swagger

Backend REST API application uses **[Swagger](https://swagger.io/specification/)** to provide autogenerated 
documentation.

Maven dependency is available here:
**[org.springdoc ---> springdoc-openapi-starter-webmvc-ui](https://mvnrepository.com/artifact/org.springdoc/springdoc-openapi-starter-webmvc-ui)**.

#### Stripe

Payment functionality in this project is powered with **[Stripe](https://stripe.com)**.
It is one of the biggest and most popular payment processors available with huge variety of services.

Maven dependency is available here:
**[com.stripe ---> stripe-java](https://mvnrepository.com/artifact/com.stripe/stripe-java)**.

#### Model Mapper

DTO classes are implemented in this project for each entity class that is transferred between REST API 
and frontend client via HTTP. Model Mapper simplifies conversions between entity classes and dto classes.

Maven dependency is available here: 
**[org.modelmapper ---> modelmapper](https://mvnrepository.com/artifact/org.modelmapper/modelmapper)**.

#### Project Lombok

Project Lombok is used to reduce the amount of boilerplate code throughout the project. Easy to get into and
can be included as a maven dependency while building project template with Spring Boot. 

#### Testcontainers

Powerful service to provide fast bootstrap of testing containers for integration or unit testing purposes.
Used within this project's integration tests to quickly bootstrap PostgreSQL containers for each test class.

All logic related to creating test containers is written with use of:
* **[org.springframework.boot ---> spring-boot-testcontainers](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-testcontainers)**;
* **[org.testcontainers ---> junit-jupiter](https://mvnrepository.com/artifact/org.testcontainers/junit-jupiter)**;
* **[org.testcontainers ---> postgresql](https://mvnrepository.com/artifact/org.testcontainers/postgresql)**

Maven dependencies are available via links above or can be included as a maven dependency while building 
project template with Spring Boot.

#### Httpclient5

Httpclient5 is used to enhance basic RestTemplate functionality, specifically for testing purposes.

Maven dependency is available here:
**[org.apache.httpcomponents.client5 ---> httpclient5](https://mvnrepository.com/artifact/org.apache.httpcomponents.client5/httpclient5)**.


### Front-end

#### React Router

Client side routing is powered by **[React Router](https://reactrouter.com)**.
Library allows configuration of Route components to provide easy navigation throughout the 
application web pages.

Quick start with React Router using npm: `npm install react-router-dom`. Additional info is available 
via link above.

#### Swiper

Books carousel on home page is configured using **[Swiper](https://swiperjs.com/react)**. 
Easy to use, a lot of configuration options.

Quick start with Swiper using npm: `npm install swiper`. Additional info is available via link above.

#### JWT Decode

JWTs obtained from REST API backend application contain valuable info encoded into payload, for example user's 
authorities, that allow access to some pages or functions of frontend client application. This jwt-decode npm 
package provides a number of functions useful when jwt payload info needs to be extracted and decoded.

Quick start with jwt-decode using npm: `npm install jwt-decode`.

#### Stripe

Payment functionality in this project is powered with **[Stripe](https://stripe.com)**.
It is one of the biggest and most popular payment processors available with huge variety of services.

Quick start with Stripe using npm: 
* `npm install jwt-decode`;
* `npm install @stripe/react-stripe-js`;
* `npm install @stripe/stripe-js`

Additional info is available via link above.

#### Styles

All the css styles in this project are configured using **[Tailwind CSS](https://tailwindcss.com)**.
Powerful & popular framework designed to economize tons of css code and .css files and build designs 
and layouts directly in markup code. Additional info is available via link above.



## Implementation and start up

There are currently two ways to run this application locally on your machine: 

* By downloading this repository ZIP on your computer and running the code with your preferable IDEs;


* By downloading this repository ZIP on your computer and running docker containers created with 
docker-compose.yml file available in the root of this project.

  
Download ZIP from this repository and choose one of the following.


### Running the code with IDEs

This project is basically fully prepared for running on local machines, however there are several 
steps that need to be done in order to run both frontend and backend applications without getting any errors.

Following are the necessary actions with brief description.


#### Back-end REST API start-up

* Firstly, download ZIP from this repository and unarchive it;


* Create local PostgreSQL DataBase on your machine either by running a docker container of 
postgres official image or by creating a DB via pgAdmin 4;


* Open `BookStore_Backend` folder in your preferable IDE;


* Navigate into `BookStore_FullStack/BookStore_Backend/src/main/resources` directory, remove `.blank` from
`application.properties.blank` file name and open this file;


* Make sure that `spring.datasource.url`, `spring.datasource.username` and `spring.datasource.password` 
values are matching with the corresponding parameters of the DataBase created earlier;


* Enter missing values for `jwt_secret` and `stripe.key.secret` variables. Project will start up and work 
without Stripe keys, but payment functionality will not work properly. JWT secret has to be >= 256-bit, 
otherwise you will get errors trying to access secured endpoints.
  * JWT secret is any 256-bit string or encoded 256-bit string of your choice;
  * Stripe secret key can be obtained from your Stripe account;


* Navigate into `BookStore_Backend/src/main/java/com/iliamalafeev/bookstore/bookstore_backend`, open 
`BookStoreBackendApplication.java` file and run it.


If startup goes successfully - application will connect to your database and all required tables will be 
automatically created using `data.sql` and `schema.sql` files located in `resources` directory. After that 
backend API should be up and running, ready to accept requests from the frontend.


#### Front-end Client application start-up

* Open `BookStore_Frontend` folder in your preferable IDE;


* Open `.env` file and replace `VITE_STRIPE_PUBLIC_KEY` variable value with your Stripe public key that can be 
obtained from your Stripe account;


* Open new terminal / command line window for this folder and run `npm install` command to download and install 
all project's dependencies. This procedure might take a little while;


* Once all the dependencies are installed, simply run `npm run dev` command. This should start the frontend 
application locally.


If startup goes successfully - application will be up and running on port 5173 and will be accessible through 
your web browser. **Please note**, that in order to access all the functionality of this application it is 
preferable to keep the backend application running as well.

**Important note:** admin functionality will not be accessible inside the application via regular user register 
procedure. Therefore, I added one default user with **admin** authority to database initialization file. You can 
log in with these credentials:

* `login`: **admin@email.com** 
* `password`: **adminpassword**. 

Another option is to register a new user and then access your database via IDE or pgAdmin 4. Within the database 
open table `person` and change **ROLE_USER** value of `role` column to **ROLE_ADMIN** for your user entity. Now 
when you re-login - new JWT will be issued with another authority and admin navigation tab will appear on the 
navbar of the website. 



### Running the code with Docker

If you are familiar with Docker and have it installed on your computer it should be even easier to test run the 
application on your local machine.

There are two multi-stage **Dockerfiles** created for this project - one inside `BookStore_Backend` folder and 
another one inside `BookStore_Frontend` folder. They describe the instructions on how to build separate docker 
images for Backend and Frontend applications correspondingly. 

There is also a single **docker-compose.yml** file inside the root of this repository. It contains the 
instructions on how to build all the required images based on those Dockerfiles and runs them as a multi-container.

Following is the brief instruction on how to run the application locally with Docker:

* Firstly, download ZIP from this repository and unarchive it;


* Navigate into `BookStore_FullStack/BookStore_Backend/src/main/resources` directory, remove `.blank` from
`application.properties.blank` file name and open this file in any text editor or IDE;


* Enter missing values for `jwt_secret` and `stripe.key.secret` variables. Project will start up and work 
without Stripe keys, but payment functionality will not work properly. JWT secret has to be >= 256-bit, 
otherwise you will get errors trying to access secured endpoints.
  * JWT secret is any 256-bit string or encoded 256-bit string of your choice;
  * Stripe secret key can be obtained from your Stripe account;


* Repeat previous 2 steps with 
`BookStore_FullStack/BookStore_Backend/src/test/resources/application.properties.blank` file;


* Open `BookStore_Frontend` folder in your preferable IDE;


* Open `.env` file and replace `VITE_STRIPE_PUBLIC_KEY` variable value with your Stripe public key that can be 
obtained from your Stripe account;


* Open new terminal / command line window and navigate into unarchived project root folder;


* Run `docker-compose up` command. This will automatically build necessary docker images and run multi-container 
based on those images. You will see the logs in your terminal / command line window. If you do not want to occupy 
your current terminal / command line window, run this command in detached mode instead: `docker-compose up -d`. 
This procedure might take a little while on first startup since docker will be downloading all required images.


If startup goes successfully - application will be up and running on port 5173 and will be accessible through
your web browser.

**Important note:** admin functionality will not be accessible inside the application via regular user register
procedure. Therefore, I added one default user with **admin** authority to database initialization file. You can
log in with these credentials:

* `login`: **admin@email.com**
* `password`: **adminpassword**.

Another option is to register a new user and then access the database created with docker container via
terminal / command line, IDE or pgAdmin 4. Within the database open table `person` and change **ROLE_USER** value 
of `role` column to **ROLE_ADMIN** for your user entity. Now when you re-login - new JWT will be issued with 
another authority and admin navigation tab will appear on the navbar of the website. 



## Contribution

Thank you for reading this file up to this point! I highly appreciate the time you spent on reviewing this 
document and do hope that you liked this project.

If you have any questions, found any bugs or want to discuss something with me - please feel free to contact 
me via any option available on my profile page.

**Good luck!**