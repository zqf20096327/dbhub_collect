
# Cafe Maria
The game no one saw coming nor wanted in the first place.

## Common Questions
#### What is this?
A proof of concept demo of a text-based, multiplayer, restaurant sim game built entirely in MariaDB. Yes, the database. You host it on your server, and play solo or with friends if you have any.
#### What do you mean "entirely in MariaDB"?
Exactly what it says. There are no external components or scripts. The game lives entirely in the DB and is played via stored procedures that the players call when logged into the server.
#### What is the goal?
The goal of the game is to manage and run your own restaurant. If you want to throw chaos into the mix, invite some friends. Can't promise you'll still be friends afterwards.
#### Is this done?
Technically yes, but also no. This is a proof of concept demo and should not be considered a full game. At the moment, everything is fully playable from top to bottom (fun not guaranteed). That said, even though it is playable, there are a LOT of formulas and settings that are unbalanced, there are not nearly enough recipes (I provide 3).

## Installation
Install at your own risk. This is first and foremost a fun project, not a commercial project. While I tried my best to prevent SQL injection, and to keep things secure, it probably has vulnerabilities due to the nature of it. I highly ~~recommend~~ insist that you only run this on an isolated server by itself. Only host it publicly if you know exactly what you are doing, even then I don't recommend it.

**Pre-Step:** You'll want to set up your own MariaDB instance to host all this, I'm not going to cover that in here as there are a million ways to do it, and a million + one to not do it securely. These instructions assume you have access to a MariaDB instance that can be logged in as root.

**Important Note:** The install will generate 2 roles, a `player` and `admin`, as well as a new user named `manager`. Users with any of those names (roles live in the user table) must not exist before starting the install process. You have been warned.

**Another Important Note:** Collations may conflict. I used a default instance, but some may not, and defaults may change between versions. Before performing step 4, use a find a replace for any collations in the SQL so that it matches what `mysql.user` uses if it doesn't already.

1. Log into your MariaDB instance with root access. Without root, things may not go so well.
2. Create a new DB called `cafe_maria`.
3. Still as root, set the current DB to `cafe_maria` via the command `USE cafe_maria;`
4. Run the provided SQL in the selected DB.
   	* This was built and tested on `MariaDB Server v10.11`. The dump is fairly basic, but if there are any errors, you'll need to make any appropriate adjustments based on the errors and re-run the SQL.
   	* You can run them all by hand, or I created a singular SQL file that contains all the pieces in `Releases`.
   	* Either import the file, or copy and paste the whole thing. Up to you.
   	* **Special Note:** The file in `Releases` is not a true dump file. It is simply a generated file that contains all the SQL in this project.
5. If you do not want to allow users to log in from anywhere, you'll need to change a setting.
	* In the `cafe_maria.game_settings` table there is a row for `user_host`. This is what is used when creating a new user to say where they can log in from. The default is `'%'`. You can update that to restrict access.
6. Then you'll run the command to set up the game. `CALL server_setup();`
	* This does a few things. The most notable being that it sets up various pieces of data for the game, as well as creates the `manager` player.
7. At this point, you are almost ready to play. You can log out, then log back in as the `manager` user.
	* The `manager` initial password is just `manager`. It can be updated within the game if desired.
	* Important Note: Managers and players cannot run any sort of raw sql commands like INSERT,SELECT,UPDATE. They can only run specific stored procedures which we will call "commands" from this point.
8. Once you log in as the `manager`, if you aren't already there, go to the `cafe_maria` DB.
9. At this point, the game is set up and is almost ready to play. You can now run `CALL help;` to see a list of available commands at any point.
10. In that list, you'll see the command to start a new game. Run that now and you are ready to go!

## How to play
You must be wondering, how on earth do you play a game entirely in MariaDB. Well, it is simple. The entire game is played with stored procedures. Yes, I'm being serious.  Every command must start with `CALL`, case-insensitive, and end with a semi-colon. For example: `CALL help;`.

At any point in the game while as a player or admin, running the help command, `help` will show you a list of commands you can run right now. This list is context and role specific. If you don't see the command in the list, you can't run it right now.

The game is made up of 2 game phases, a management phase and a timed kitchen phase. You will go from one phase to the other until you lose, or get tired of playing. For a brief overview: The management phase is the setup part for the kitchen phase. The kitchen phase is where you do the actual cooking and completing customer orders within a time limit. I'll go into detail more in their dedicated sections below.

### Winning
The game doesn't have a winning condition, you just keep going until you lose or get bored. If you really want a winning condition, I guess you can keep playing until you trigger an overflow error somewhere. As for losing, your restaurant has funds, when you get yourself stuck cause you can't afford anything, then you lose.

### Users
There are two user roles in the game: `admin`, and `player`. All users help with the cooking, but only the admin can make restaurant decisions. The original `manager` user created during setup is the only admin user. The admin can either play the game solo, or create new logins for friends with the `create_player` command. All created users will have the player role. New users will have their initial password be the same as their username. Once logged in, users can update their own passwords to something new with `update_password`.

At any point, the admin can ban a user with the `ban_player` command.

### Funds / Money
You use funds to buy new kitchen stations, maintain those stations (stations have a daily usage cost), as well as setting up the menu for the next kitchen round (you have to buy the required ingredients). You earn money by completing orders during the kitchen phase.

### Restaurant Rating
Believe it or not, your digital restaurant is not immune to reviews. Your rating affects the number of customers you get in the round. The higher your reviews, the more customers you get. Reviews are calculated based on how well you did during the kitchen phase. There are only two main criteria that goes into each customer order's score: the number of mistakes, and if you didn't complete the order.

For the reviews, it is a simplistic approach. A simple weighted average of your existing review with the review from the current round. It isn't perfect, but a lot more forgiving than the other one I had.

Fun side note about the review system: This wasn't my first idea. I originally wanted a more lifelike one, where each order had a chance to leave a review. All those reviews, averaged, gave you your rating. In the end, the big problem was that it was extremely punishing and overly difficult to improve your score if you had a few bad rounds early on. I may have it as an option later if people want it which is why I'm putting this note here.

## Management Phase
During the management phase, the goal is to prepare for the next kitchen phase. The admin will be doing all the work in this phase. They need to set the menu, as well as buy new cooking or plating stations. This is also where the admin can bring in other players to play with them.

#### Setting the Menu
After each kitchen phase, the menu is reset so you can decide what to cook the next round. When items are added to the menu via `menu_add`, any money needed to cover the basic ingredients will be subtracted from the restaurant funds. In addition, those ingredients are automatically added to the kitchen storage to use during the kitchen phase.

#### Buying Stations
As the ratings go up, more orders come in. The provided stations will not be enough to keep up with the orders. Thankfully, the manager can buy additional stations. There are various types of stations used during the kitchen phase, all of which can be bought and sold during the management phase. It is up to the manager to verify that they have the correct stations needed to complete the kitchen round. If you have french fries on the menu, you better have at least one fryer.

#### Ready to Play
To start the kitchen phase, your menu must have at least one item. Then run the `kitchen_open` command.

## Kitchen Phase
During the kitchen phase, the goal is to successfully complete customer orders within a set time limit *(Default 5 min)*. Yup, time based gameplay. Players earn money for successful orders, but lower the restaurant score by serving incorrect orders or not completing orders before the time runs out. I'll talk about customer orders a little later.

The whole kitchen phase is a very involved process. The players must check on any pending orders, assign one to an available plating station, retrieve raw food and ingredients needed from storage, prepare the food as directed in the customer's order, then put the prepared food on the plate in the plating station, and then finally serve the plate to the customer.

#### Multiplayer
Want to work on healthy communication techniques or destroy friendships? Add more players to the game during the management phase. During the kitchen phase, everyone is involved. Each player, including the admin can cook, plate, serve, sit around and do nothing, etc. How to organize yourselves is up to y'all. You can run it like a real kitchen, or make it into a free for all, and the admin can always `ban` players who don't play nice.

#### Inventory & Storage
While juggling all their responsibilities, each player must also manage their own inventory. There are limits on how much a player can hold *(default 5 items)*. Using the kitchen storage is key for that. While inventories are per user, the storage is unlimited and shared among all users.

Kitchen storage is a catch-all. I originally had numerous storage locations like a cooler, heated tops, etc, but it just wasn't fun to remember all of that. So now everything goes in the storage and is magically kept at the correct temperature and freshness and whatever digital health regulations dictate the food be stored at.

#### Playing
Using the `view_recipe` and `help` commands are essential in the kitchen phase. They essentially tell the player how to play the game. Calling `view_recipe` on a food item will show the player exactly how to cook it, including all the commands involved. Using the `help` command details the args needed to run each command.

When time runs out, the players will not be able to run cooking or serving commands anymore. To officially end the kitchen phase and go to the management phase, the manager must run the `kitchen_close` command.

#### Customer Orders
Customer orders are ultimately what the gameplay revolves around. Orders will come in at random times throughout the phase, so be sure to be keeping track of what orders are waiting via the `view_orders` command. I'm not heartless, so no orders come in during the last minute of the phase.

Each menu item has an associated category, and each category has a chance at appearing on an order. So yes, it is possible to have an order with 4 foods on it.

* Entree: All orders will have exactly one entree.
* Appetizers have a 25% chance of being on an order.
* Sides have a 50% chance.
* Desserts have a 20% chance.

**Special Note:** Since this project is just a proof of concept, the code is in there for other food types, not all may be included in the provided base project. Feel free to add them to your own games.

#### How to fulfill orders
Orders must be assigned to a plating station, then prepared food must be added to the same plating station. Once all the correct food items are on the plate, the plate can be served. A successful result will mark the order as complete and clear the plating station automatically for a new order. A failed order (some dumb player put a steak on a burger order), the plating station will not be cleared and the players can try again.

#### Interaction Commands
Many commands in this phase interact with aspects of the kitchen or food. Most of the interaction commands have the pattern: `location_name` followed by `_interaction_type`. The args sometimes differ for each location and interaction type, so be sure to read the in game help for each command. There really are only 2 core interaction commands, `put` and `take`.

* `_put` will put something from the player's inventory into the specified location.
  * For locations, like stations, that contain multiple possibilities, the first arg will designate the specific numerical location.
  * Example: `CALL grill_put(2, 'raw_beef');` will put raw_beef at grill station 2.
* `_take` will take something from the location and add it to the player's inventory if there is room available.
  * For locations, like stations, that contain multiple possibilities, the arg will designate the specific numerical location.
  * Example: `CALL storage_take('raw_beef');` Will take a raw beef from the kitchen storage and add it to the player's inventory.

In addition to those, there are some other interaction commands like `cut`, `flatten`, or `grind`. These will take something from the player's inventory and turn them into something else. Use these when the recipe says to use them.

#### Interacting with the plating stations
As you know, plating stations hold the orders while players work to fulfill them. Only one order can be assigned to each plating station at a time, but the manager can buy more stations during the management phase as needed. After assigning an order, players cook the foods to fulfill that order. Using the `help` command will show the available interactions with the station. Players can `assign` orders to the station, `put` food onto a plating station, as well as `take` items off of it. Using `clear` will put that order back into the queue and discard all the food in that station. Finally players can `serve` the plate to complete the order. The player can also `view` the status of each plating station by using `CALL view_plating;`.

#### Cooking stations
Cooking stations are similar to the plating stations. There can be multiple grill stations and players can `put` and `take` food from each of them. The main difference from the plating station is that these stations perform timed actions on the food to turn it into something else. The grill is a perfect example. Using `CALL grill_put(2, 'raw_beef');` will put raw_beef on to grill station 2. In addition to that, it starts a timer. Once that timer is up, that raw_beef turns into something else, in this case, `steak`. So the player now must use `CALL grill_take(2);` to take the `steak` from station 2 and add it to their inventory. At any point during this phase, the player can use view commands, which is simply `view_` and then the station name, to view the status of each station of that type.

If you want a high-level view of all the kitchen stations at any time, run `CALL view_stations;`. To see the current status of the phase phase like time remaining and number of completed orders, run `CALL view_status;`.

There are too many commands to cover for the kitchen phase, so you get to do the legwork for that. Use the help command while playing in the kitchen phase to see the available commands.

## Development
Here are some notes to help you develop and expand on your own game instance if you want. Just be sure to throw me in the credits somewhere.

#### Project Organization
Most logic happens in stored procedures. I make a distinction between which can be called by users and which are used internally. Internal (or private) procedures are prefixed with `__` for a reason. There are some internal dev procedures that look at the names and will do something different depending on if it is a private one or not.

#### Adding your own Content

**Commands:** Commands are stored in the `commands` table, and their running permissions are stored in the `command_permissions` table. When adding procedures, you can run `___DEV_refresh_command_list` to automatically add any new callable procedures and delete any removed ones. That command also adds entries into the permissions table. Once the command has been created, permissions must be set. 

**Command Permissions:** Command permissions are how you tell the players what commands can be run and when. It also what drives the context specific `help` command. When it comes to values, most are true (1), false (0), or any value (NULL). The exception being the `game_state` column which takes either a NULL or a value from `game_states.game_state`. When the permissions are set the `___DEV_refresh_command_permissions` needs to be run. This will update the permissions lookup table as well as refresh any existing user's permissions.

**New Recipes:** What is a cooking game without recipes? I provide 3 to show the proof of concept, but more can be added. Any new foods must be added to the `food` table, that also means any foods that are simply steps along the way to cooking the final result (like `cut_potato`). Any sort of food assembly must go into the `food_assembly` table, and any foods that get processed from one to another (raw_beef -> steak, or potato -> cut_potato) need to get an entry into the `food_processing` table. If the processing does not take place on a cooking station, don't add a cooking time, leave it at 0, if it does require a station, add a time you think makes sense.

Adding the recipe for the final food is a bit more involved. This data is located in `recipe_steps` and it is a recursive table that details any prerequisites for each step. When adding a new recipe, be sure the food items for each step are already in the `food` table, I also recommend starting from taking the ingredients out of storage and work your way to the final result. Add any new directions for pulling each new ingredient out of storage, and use existing steps whenever you can. If your recipe calls for raw_beef, use the existing step for taking raw beef out of storage. For a more in-depth look, you will have to look at examples from the other bits. `Hamburger` is the most advanced one as it has the `assembly` step as well as station steps.

Once that is done, the resulting food needs an entry in the `menu_items` table for it to show up in the management phase as a potential menu item.

**New Instant Processing Command:** It is possible to add new instant commands for cooking, while I have procedures like `cut` , nothing is stopping you from adding your own for your own recipes. Take a look at the `cut` procedure on how to set up a new one. It is really easy.

**Adding a new type of cooking station:** To add a station, you will need 3 new commands `put`, `take`, and `view`. Thankfully, you can use the grill as a reference on how to set that up. In addition, you will need to add a new entry in the `stations` table.
 
 **New Features:** Adding new features is a bit more case specific so that is up to you. That said, most of what is in the doc and existing pieces will help get you started.
 
## FAQS
#### But why?
I wanted a challenge to see if it was possible. Things kinda spiraled out of control, now here we are.
#### Will there be updates?
Maybe. I had other ideas I wanted to implement, but life is just so busy.
#### Will there be a Cafe Maria 2?
No, why would you want that?
#### Is this vulnerable SQL injection or have any security vulnerabilities?
eh, probably. Someone is bound to find something wrong with it.

##
### Thank you! Best of luck and happy digital cooking!
