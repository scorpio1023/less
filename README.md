less
====

a django project used to maintain the server information of my group

there are several server machine which installed different OS(such as: RHEL5.x RHEL6.x...)
when we have to work based on a certain OS environment, we will look for it one by one.
it's not convenient.

This project help us to get what we need immediately!

as it can get information from other server, here I use command 'ssh' to get it done.
I have tried 'pexpect', it will elapse much time on looking for the expect words, sending 
words. I use a third-party module 'paramiko' instead

so before use this app, 
    "paramiko" SHOULD BE INSTALLED AND BE AVAILABLE


