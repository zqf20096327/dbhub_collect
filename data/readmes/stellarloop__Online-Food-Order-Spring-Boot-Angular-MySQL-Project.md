<img width="703" height="397" alt="image" src="https://github.com/user-attachments/assets/1a2a9e86-3d62-4b93-af8a-298ead05b4d1" />

A normal Online Food Order Spring Boot Angular MySQL Project which implements the MVC (Model-View-Control) Architecture.
As View, Angular-8 with routing is used. For the backend, Spring Boot v2.1.6 is used. For the Database Support, MySql has been used. Java Persistence Api (JPA) is used to write the Business Logic. REST Api's are written to communicate between server ports (Angular-> port:4200, SpringBoot -> port:8080, MySql -> port:3306)

The project consist of a Login and Register page when user navigates to localhost:4200. On successfull login or Registration as a user, a welcome page all the user details and option to order your food. The Menu page list all the available items in database with their available quantity. When items are added to cart and navigated to payment page, it asks for card details. On clicking the pay now option, the purchased quantity get's seperated from DB as well as Menu component.

Similarly, when a person logins or registers as a merchant, a page with the merchant details appers with an option to alter the menu. If a merchant add the quantity a post request is made and the DB updates itself. The component refreshes itself and the page doesn't need to refresh to see the changes.

Software Requirements :-
Java 7 or Above installed on device
MySQL Server
NodeJS - npm
<br>
Login Details Merchant :
<br>
userename - <!-- merchant -->
<br>
password - <!-- merchant  -->
</br>
Login Details For User :-
<br>
username - <!-- user -->
<br>
password - <!-- user -->
