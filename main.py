import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

led_pins = [
    board.IO21,
    board.IO26, # type: ignore
    board.IO47,
    board.IO33, # type: ignore
    board.IO34, # type: ignore 
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39
    # do the rest...
]

leds = [DigitalInOut(pin) for pin in led_pins]

for led in leds:
    led.direction = Direction.OUTPUT

# Set a new max volume for normalization 
max_volume_value = 42000  # Adjust based on observed sensitivity 
decay_rate = 0.05  # how fast or slow the volume goes down 

# Track previous displayed volume
displayed_volume = 0

# Function to normalize and filter microphone volume level
def get_volume():
    # Read raw microphone value
    raw_value = microphone.value
    
    # divide the raw value measured by the max volume set to get the normalized value between 0 and 1
    normalized_value = raw_value / max_volume_value
    
    # Set a threshold to filter out low noise values
    volume = max(0, normalized_value - 0.1)  # Adjust threshold if necessary
    
    return volume

# Function to update LEDs based on the displayed volume level
def update_leds(volume):
    led_count = len(leds)
    led_to_turn_on = int(volume * led_count)
    
    # Turn on LEDs up to led_to_turn_on and turn off the rest
    for i in range(led_count):
        leds[i].value = i < led_to_turn_on

# Main loop
while True:
    volume = get_volume()  # Get the current volume level
    print(f"Current volume): {volume}")  # Print the volume for monitoring

    # Fast rise, slow decay logic
    if volume > displayed_volume:
        displayed_volume = volume  # Immediate update if volume is higher
    else:
        displayed_volume = max(0, displayed_volume - decay_rate)  # Gradual decay

    update_leds(displayed_volume)  # Update LEDs based on displayed volume
    sleep(0.05)                    # Small delay for smooth updates

    # instead of blinking,
    # how can you make the LEDs
    # turn on like a volume meter?
