from Implementation.Biped import Biped

biped = Biped()
while (biped.get_keypad().get_pressed() is not Keys.ZERO):
    key_pressed = biped.get_keypad().get_pressed()
    
    new_dance = Keys.to_dance(key_pressed)
    if ((biped.state.name == "Dancing") and (biped.state.current_dance.name != new_dance)):
        biped.state.current_dance = Dance(biped, new_dance + ".sequence")
        
    
    distance = biped.get_sonic_sensor().get_distance()
    if (distance <= 20):
        if (biped.state.name != "Aggress"):
            biped.get_keypad().pressed = Keys.TWO
            biped.previous_state = biped.state
            biped.state = Aggress(biped)
    elif ((biped.previous_state is not None) and (biped.previous_state is not biped.state) and (biped.state.name != "Waiting")):
        biped.state = biped.previous_state
        biped.previous_state = biped.state
    
    biped.state.update()