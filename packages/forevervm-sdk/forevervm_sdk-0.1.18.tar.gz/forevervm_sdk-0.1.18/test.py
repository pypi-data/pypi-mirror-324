import sys

sys.path.append("src")

from src import ForeverVM

API_KEY = "j5UaCLApWIkJKLcb.VXQeTMuYDRQMQEnrV2nwEXBqPJWVJDfz"

fvm = ForeverVM(API_KEY)
with fvm.repl() as repl:
    result = repl.exec("def foo():\n  for i in range(10):\n    print(i)\n  return 100")
    print(result.result)

    result = repl.exec("foo()")
    for log in result.output:
        print(log)
    print(result.result)

# exec = fvm.exec("1 + 1")
# result = fvm.exec_result(exec["machine"], exec["instruction_seq"])

# import os
# # from forevervm import ForeverVM

# token = os.getenv("FOREVERVM_TOKEN")
# if not token:
#     raise ValueError("FOREVERVM_TOKEN is not set")

# # Initialize foreverVM
# fvm = ForeverVM(token)

# # Connect to a new machine
# with fvm.repl() as repl:
#     # Execute some code
#     exec_result = repl.exec("4 + 4")

#     # Get the result
#     print("result:", exec_result.result)

#     # Execute code with output
#     exec_result = repl.exec("for i in range(10):\n  print(i)")

#     for output in exec_result.output:
#         print(output["stream"], output["data"])
