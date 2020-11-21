from table import Table
import time

TABLES = {"1046": Table(1046, [[0.03948170731707307, 0.09692911255411243], [0.4337906504065041, 0.09692911255411243], [0.03948170731707307, 0.4648944805194804], [0.4337906504065041, 0.4648944805194804]]),
    "1047": Table(1047, [[0.542530487804878, 0.08340097402597384], [0.9276930894308945, 0.08340097402597384], [0.542530487804878, 0.4554247835497834], [0.9276930894308945, 0.4554247835497834]])
}

table_46 = TABLES["1046"]


print("==== NO SLEEP AT ALL BRO ====")
table_46.did_change_state(2)
time.sleep(2)
table_46.did_change_state(1)
table_46.did_change_state(0)
table_46.did_change_state(2)

# print("==== SLEEPING FOR 19 SECONDS ====")
# table_46.did_change_state(2)
# time.sleep(19)
# table_46.did_change_state(0)

# print("==== CHANGE STATES FROM 0 -> 1 ====")
# table_46.did_change_state(1)
# table_46.did_change_state(0)

# print("==== CHANGE STATES FROM 0 -> 2 -> 1 -> 0, SLEEP 18 SECS ====")
# table_46.did_change_state(2)
# time.sleep(18)
# table_46.did_change_state(1)
# table_46.did_change_state(0)

# print("==== CHANGE STATES FROM 0 -> 2 -> 1 -> 2 -> 0, SLEEP 18 SECS ====")
# table_46.did_change_state(2)
# time.sleep(18)
# table_46.did_change_state(1)
# table_46.did_change_state(2)
# time.sleep(18)
# table_46.did_change_state(0)