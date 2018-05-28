# Jeff Starr, 5 September, 2017
# Exercise 9-9 of Python Crash Course
# This exercise implements a simple observer pattern in which each 
# ElectricCar instance subscribes to its battery ("observes it")
# and re-calculates its (the car's) range if the battery is upgraded.  
# This was necessary
# because I wanted to model the range as an attribute of the car instead
# of a calculation within the get_range method of the battery as the book
# implemented it. (I think range should be an attribute of the car.)

# The book didn't mention nor require observer pattern.  I thought it was
# called for, researched and found the pattern.

class Car():
    """A simple model of a car."""

    def __init__(self,make,model,year):
        """Initialize attributes to describe a car."""

        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0        

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()

    def fill_gas_tank(self):
        print("Gas tank all filled up!")

    def read_odometer(self):
        """Print a statement showing the car's mileage."""
        print("This car has "+ str(self.odometer_reading) + " miles on it.")

    def update_odometer(self,mileage):
        """
        Set the odometer reading to a given value.
        Reject if it attempts to roll the odometer back.
        """

        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer.")

    def increment_odometer(self, miles):
        """Add the given amount to the odometer reading."""
        if miles >= 0:
            self.odometer_reading += miles
        else:
            print("You can't roll back an odometer.")        


class ElectricCar(Car):
    """Represents aspects of a car, specific to electric vehicles."""
    def __init__(self,make,model,year):
        """
        Initializes attributes of the parent class.  It takes the attributes
        necesasry to create a car.
        """

        super().__init__(make,model,year)
            """
            Special function that connects the child class with the parent
            class.
            """

        # Create a new instance of Battery() and store it in the attribute
        # self.battery.

        self.battery = Battery()

        # Here's where the observer pattern begins.  The purpose of the
        # observer pattern is so that the range  attribute of 
        # electric car will update if the battery upgrades to a larger size.

        # Register the electric car instance (self) with battery 
        # by calling this battery.register method so that new range 
        # will calculate if battery upgrades.

        self.battery.register(self)
        
        # Go ahead and calculate the initial range...which will change if the
        # battery upgrades.
        self.calculate_range()
    
    
    def calculate_range(self):
        """A method to calculate range from battery and model."""
        if self.model.lower() == 'model s':
            if self.battery.battery_size == 70:
                self.range = 240
            elif self.battery.battery_size ==85:
                self.range = 240*85/70
        elif self.model.lower() == 'model x':
            if self.battery.battery_size == 70:
                self.range = 250
            elif self.battery.battery_size ==85:
                self.range = 250*85/70
        elif self.model.lower() == 'model 3':
            if self.battery.battery_size == 70:
                self.range = 245
            elif self.battery.battery_size ==85:
                self.range = 245*85/70

    # This is part of the observer pattern.  This battery_upgraded() method
    # should run all the methods that should be run if a battery upgrades.
    # The Battery() itself 
    def battery_upgraded(self):
        self.calculate_range()

    def fill_gas_tank(self):
        """Electric cars do not have gas tanks so this overrides the 
        method."""
        print("This car does not have a gas tank!")
    
    def print_range(self):
        """Print a statement about the range this car has with its battery."""
        
        print("This " + self.model + " with a " + 
            str(self.battery.battery_size) +
            " kWh battery has a range of " + str(self.range))

class Battery():
    """Model a simple battery for an electric car."""
    def __init__(self, battery_size=70):
        """Initialize the battery's attributes."""
        self.battery_size = battery_size
        
        # This lets electric car instances subscribe to their
        # batteries and re-calculate range whenever their battery is upgraded.
        # A "set" is an unordered collection with no duplicates.
        self.subscribers = set()

    # The electric car instance registers with its battery and gets added
    # to the set of subscribers, an attribute of the battery.
    def register(self,who):
        self.subscribers.add(who)
    def unregister(self,who):
        self.subscribers.discard(who)
    
    # This dispatch method tells all the subscribers to run their 
    # battery_upgraded method.  (If a battery upgrades, other things besides
    # calculate_range() might need to run like weight of the car.)
    # Battery does not need to know all those methods.  They are inside the 
    # battery upgraded method of the electric car subscribers.

    def battery_upgraded_dispatch(self):
        for subscriber in self.subscribers:
            subscriber.battery_upgraded()

    def describe_battery(self):
        """Print a statement describing the battery size."""
        print("This car has a " + str(self.battery_size) + "-kWh battery.")

    def upgrade_battery(self):
        """Check battery_size and upgrade to 85 kWh if it is not 85 already."""

        if self.battery_size == 70:
            self.battery_size = 85
            # This command kicks off the recalculation by all subscribers
            self.battery_upgraded_dispatch()

        elif self.battery_size == 85:
            print("You've already got the biggest, baddest battery we have.")

#_____________________

my_car = ElectricCar('Tesla','Model S',2020)
my_car.fill_gas_tank()


print('\n'+my_car.get_descriptive_name())

my_car.update_odometer(1000)

my_car.read_odometer()

my_car.increment_odometer(100)

my_car.read_odometer()


my_car.increment_odometer(-100)

my_car.read_odometer()

my_car.increment_odometer(10)

my_car.read_odometer()

my_car.battery.describe_battery()

my_car.print_range()

my_car.battery.upgrade_battery()

my_car.battery.describe_battery()

print(my_car.range)

my_car.print_range()

print(240*85/70)

my_car.battery.upgrade_battery()

my_car1=Car('Toyota','FJ Cruiser',2007)
my_car1.fill_gas_tank()



