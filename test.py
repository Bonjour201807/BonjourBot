from bonjour.agent.run_task import RunTask

policy_handle = RunTask()
while 1:
    u_input = input('user: ')
    print('bonjour: ', policy_handle.run({'query': u_input, 'uid': 'bz'}))
