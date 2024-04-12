import microcontroller as mcu

# To divide lists into n sized chunks
def divide_chunks(l, n):
  list=[]
  for i in range(0, len(l), n): 
    x = i
    list.append(l[x:x+n]) 
  return list

# Outputs mcu's uid for unique idetification
def mcu_uid():
  uid = ""
  for i in mcu.cpu.uid:
    uid += "".join(["0"] * (3 - len(str(i)))) + str(i) + "-"
  return uid[:len(uid)-1]