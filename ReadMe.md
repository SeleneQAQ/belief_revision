# Belief Agent

### How to Run

Open command prompt in the belief_revision and run the python script interface.py

When running the program, the user will start with an empty belief base. The user needs to choose an action. The available actions each time are:

m: Menu

p: Print all beliefs

r: revision

c: contraction

pos: Calculate possibility order

agm: Test for agm postulates

res: Resolution

q: Quit


When actions r or res are selected, the user has to put in a new belief to the belief base. When c is selected the user has to pick a belief that is already in the belief base.

Only 4 different letters can be used when writing in a new belief, those letters are p,q,r and s. The user can change those letters (i.e. adding more letters) if he wants in the interface.py file, line 16.


When writing in a belief please use the following signs:

~ for not

& for and 

| for or

'''>>''' for implies

