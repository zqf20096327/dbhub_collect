# RandomTidbits
This is where I'll throw random code that will serve of no use to anyone but myself. Most of the time it will just be practice code.


var money = 250;
var amountOfPhones;
var amountOfAccessories;
var loop;
const phonePrice = 25;
const accessoryPrice = 7;

function buyPhones() {
	for (loop = 1; loop == 1 ;) {
		if (money > phonePrice) {
            //buy phone
            money = money - phonePrice;
            amountOfPhones++;
            console.log("You just bought a phone! Woo.");
            if (money > 50) {
                //buy accessory
                console.log("I guess I'll get an accessory also..");
                money = money - accessoryPrice;
                amountOfAccessories++;
                console.log("You just bought an accessory!");
            } else {
                console.log("I don't have enough for an accessory.. I need"+				" to eat sometime this week.");
            }
        }
		else {
			loop = 0;
        }
	}
	console.log("Waaaow. Now I only have $" + money + ". But at least I have " + amountOfPhones + " shiny new phones! And " + amountOfAccessories + " legit accessories! .... .. . .. ");
}
