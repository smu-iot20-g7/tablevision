from table import Table

table15 = Table(15)
# A to C
table15.did_change_state(2)
print(table15.print_states())
# C to C
print("Same state again")
table15.did_change_state(2)
print(table15.print_states())
# C to B
table15.did_change_state(1)
print(table15.print_states())
# B to A
table15.did_change_state(0)
print(table15.print_states())