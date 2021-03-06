import os,sys,time,re
from myReadline import readLine
from myRedirect import redirect
from myPipes import pipe

#xpid = os.getpid()

while 1:
    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1,"$".encode())

    Input = readLine()

    if Input == "":
        continue
    
    args = Input.split(' ') 

    if args[0] == "exit": #chceks first index of args if its exit we get out 
        os.write(2, "Exiting\n".encode())
        sys.exit(0)
        
    elif args[0] == "pwd":
        os.write(1, (os.getcwd() + "\n").encode())
    elif args[0] == "cd":
       try:
           if len(args) < 2: #nothing was input if length is less than 2 
               continue
           else:
               os.chdir(args[1])  #change directory
       except:
           pass
    else:
        rc = os.fork()
        if rc < 0: #invalid fork
            os.write(2, ("fork failed, returning %d\n" %rc).encode())
            sys.exit(1)
        elif rc == 0:   #child
            if '|' in args:
                pipe(args)
            if '<' in args or '>' in args:  #we will redirect
                redirect(args)
            else:
                for dir in re.split(":",os.environ['PATH']):
                    program = "%s/%s" % (dir,args[0])
                    try:
                        #trying to execute the program
                        os.execve(program,args,os.environ)
                    except FileNotFoundError:
                        pass
                os.write(2,('Child: failed exec %s\n' % args[0]).encode())
                sys.exit(1)  #terminate with error
        else: #parent waits for child to finish
            childPidCode = os.wait()
            
                        
