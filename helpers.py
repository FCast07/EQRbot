
def parse_extension(text):
    # all IN arguments in the graph
    # m = re.findall(r"(in\()([\(A-Za-z0-9_\),]+)", text)
    m = text.split()
    intext = set()
    for el in m:
        if el.startswith("in("):
            intext.add(el)
    ins = set()
    for group in intext:
        pred = group[3:-1]
        if pred[-1] == ',':
            ins.add(pred[:-2])
        else:
            ins.add(pred[:-1])

    #print "IN Arguments are:\n"+str(ins)+"\n"

    # all arguments in the argument graph
    # a = re.findall(r"(arg\()([\(A-Za-z0-9_\),]+)", text)
    totalargs = text.split()
    alltext = set()
    attackstext = set()
    for el in totalargs:
        #if "arg(" in el:
        if el.startswith("arg("):
            alltext.add(el)
        else:
            if el.startswith("attack("):
                attackstext.add(el)

    args = set()
    inargs = set()
    for group in alltext:
        pred = group[4:-1]
        if pred[-1] == ',':
            if pred[:-2] in ins:
                inargs.add(pred[:-2])
            else:
                args.add(pred[:-2])
        else:
            if pred[:-1] in ins:
                inargs.add(pred[:-1])
            else:
                args.add(pred[:-1])

    # structured attacks extraction
    all_str_attacks = set()
    all_str_acc_attacks = set()
    #print 'attacks set: ',attackstext
    for group in attackstext:
        pred = group[7:-1]
        if pred[-1] == ',':
            pred = pred[:-2]
        else:
            pred = pred[:-1]

        #print pred, '\n'

        lpc = 0 # left paranthesis count
        rpc = 0 # left paranthesis count
        brindex = 0

        for ch in pred.split('[',1)[1]: # split at the first occurence
            if ch == "(":
                lpc = lpc +1
            if ch == ")":
                rpc = rpc +1

            brindex = brindex + 1
            if lpc == rpc and lpc>0:
                break

        all_str_attacks.add(pred)
        orig_arg = pred.split('[',1)[1][:brindex]

        if orig_arg in inargs:
            all_str_acc_attacks.add(pred)

    #print 'all attacks: ',all_str_acc_attacks

    # all attacks in the graph
    # r = re.findall(r"(att\()([\(A-Za-z0-9_\),]+)", text)
    text = text[1:-1]
    r = text.split()
    att_text = set()

    for el in r:
        #if "att(" in el:
        if el.startswith("att("):
            att_text.add(el)

    att = set()
    for group in att_text:
        pred = group[4:-1]
        if pred[-1] == ',':
            pred = pred[:-2]
        else:
            pred = pred[:-1]
        #S = pred[:-1].split('),')
        #att.add((S[0]+')',S[1]))

        lpc = 0 # left paranthesis count
        rpc = 0 # right paranthesis count
        brindex = 0

        for ch in pred:
            if ch == "(":
                lpc = lpc +1
            if ch == ")":
                rpc = rpc +1

            brindex = brindex + 1
            if lpc == rpc and lpc>0:
                break
        att.add((pred[:brindex], pred[brindex+1:]))

    return [args,inargs,att,all_str_attacks,all_str_acc_attacks]
