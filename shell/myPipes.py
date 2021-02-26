import os,sys

def pipe(args):
    left = args[0:args.index("|")]
    right = args[args.index("|") + 1]

    pr,pw = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returining %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        os.close(1) # close output of file descriptor
        os.dup(pw)   #duplicate of fd to write to
        os.set_inheritable(1,True)

        for fd in (pr,pw):
            os.close(fd)
        execution(left)
        os.write(2,("Couldn't execute : (").encode())
        sys.exit(1)
    else:
        os.close(0) #parent will close the keyboard fd
        os.dup(pr)  #duplicate read fd
        os.set_inheretable(0,True)

        for fd in (pr,pw):
            os.close(fd)
        if "|" in right:
            pipe(right)
        execution(right)
        os.write(2,( "Couldn't execute : (").encode())
        sys.exit(1)
def execution(args):
    for dir in re.split(":", os.environ["PATH"]):
        program = "%s/%s" % (dir,args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("%s : command not found\n" % args[0]).encode())
    sys.exit(1)
    
