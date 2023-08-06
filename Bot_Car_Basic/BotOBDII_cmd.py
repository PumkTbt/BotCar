import obd
def test():
    port = obd.scan_serial()
    return port
    #connect = obd.OBD(port[0])
def Mode_1(PID):
    try:
        port = obd.scan_serial()
        connect = obd.OBD(port[0])

        a=[]
        for i in PID:
            c = obd.commands[1][i]
            r = connect.query(c)
            if r.value == None:
                data = "Null"
            else:
                data = str(r.value)
            a.append(data)
        return a
    except:
        pass

if __name__ == '__main__':
    #PID_mode1 = [4, 5, 11, 12, 13, 15, 17, 31, 33, 51, 67, 70]
    PID_mode1 = [13, 12,4,5,15,70,11,31,17]
    #PID_mode1 = [13]
    data =  Mode_1(PID_mode1)
    print(data)