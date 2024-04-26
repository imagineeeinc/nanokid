# prints the mcu uid
import microcontroller as mcu
uid = ""
for i in mcu.cpu.uid:
  uid += "".join(["0"] * (3 - len(str(i)))) + str(i) + "-"
uid = uid[:len(uid)-1]
print(uid)