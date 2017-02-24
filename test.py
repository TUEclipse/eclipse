from Stepper import Stepper
  # TEST FILE FOR DETERMINING IF IT WORKS
  # ONLY RUN THIS FILE

t=Stepper(0,0)
#print t.x_raw
#print t.y_raw
#t.change_position()
#t.forward(4,40)
t.run()
#t.forward(19,4)
#steps = raw_input("How many steps forward? ")

# Testing (The delay value has to be divided by 1000 to achieve the desired delay)
#t.backwards(int(Stepper.delay) / 1000.0, int(steps))
