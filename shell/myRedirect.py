import os,re

def redirect(args):
    if '>' in args: #goes into
        os.close(1) #close fd from display
        os.open(args[args.index('>') + 1], os.O_WRONLY | os.O_CREAT) #create file if it doesn't yet exist
        os.set_inheritable(1,True)

        args.remove(args[args.index('>')+1])
        args.remove('>') #remove these because we have already used them.
    elif '<' in args: #goes out to
        os.close(0) #close fd from keyboard
        os.open(args[args.index('<') + 1], os.O_RDONLY) #open file to read from

        os.set_inheritable(0,True)

        args.remove(args[args.index('<')+1])
        args.remove('<')

    for dir in re.split(':', os.environ['PATH']):
        program = '%s/%s' % (dir,args[0])

        try:
            os.execve(program,args,os.environ)
        except FileNotFoundError:
            pass
    
