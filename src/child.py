import sys

# word = sys.stdin.readline().rstrip()
# filename = sys.stdin.readline().rstrip()

# print(word)
# print(filename)

# print(sys.argv[0])
# print(sys.argv[1])


for arg in sys.argv[1:]:
    print(arg)
# sys.argv[1] - первый параметр

# try:
#   with open(filename, "rb") as fh:
#     while True:
#       current = fh.readline()
#       if not current:
#           break
#       if (word in current ):
#           pass
#           # print("find: {0} {1}".format(filename,word))
# except :
#     pass