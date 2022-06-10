import time

"""
Function to determine the states of Able & Baker whether they free or not
"""
def getWorker(lastAble, lastBaker, arrive):
    AbleState = 1
    BakerState = 1

    if arrive >= lastAble:
        AbleState = 0

    if arrive >= lastBaker:
        BakerState = 0

    if (AbleState == 0 and BakerState == 0) or (AbleState == 0 and BakerState == 1):
        return 'Able'
    elif (AbleState == 1 and BakerState == 0):
        return 'Baker'
    else:
        return 'Wait'

"""
 Function return arrival times
"""
def getArrivalTimes(InterArrivalTimes):
    arrivals = []
    for i in range(len(InterArrivalTimes)):
        if i == 0:
            arrivals.append(InterArrivalTimes[0])
            continue
        else:
            arrivals.append(InterArrivalTimes[i] + arrivals[i - 1])
    return arrivals

"""
Function to determine the amount of time from current clock to the end of 
nearest end of service done by the two servers.
"""
def waitTime(Able, Baker, timeClock):
    wait = 0
    if Able <= Baker:
        wait = Able
    else:
        wait = Baker
    return wait - timeClock

"""
Function determine which server is free
"""
def getFree(Able, Baker):
    if Able == 0 and Baker == 0:
        print('Able and Baker are free')
    elif Able != 0 and Baker == 0:
        print('Baker is FREE')
        Able -= 1
    elif Able == 0 and Baker != 0:
        print('Able is FREE')
        Baker -= 1
    else:
        Baker -= 1
        Able -= 1
    return Able, Baker


if __name__ == '__main__':
    #Initialize the variables:
    interArrivalTimes = [0, 2, 4, 4, 2, 2]
    serviceTimes = [5, 3, 3, 5, 6, 3]

    arrivalTimes = getArrivalTimes(interArrivalTimes)

    Able = {
        'ServiceTime': 0,
        'ServiceStart': 0,
        'ServiceEnd': 0
    }

    Baker = {
        'ServiceTime': 0,
        'ServiceStart': 0,
        'ServiceEnd': 0
    }

    queue = []
    totalWaiting = 0
    timeClock = 0
    
    endSimu = arrivalTimes[-1] + serviceTimes[-1] + 1
    
    AbleFree = Able['ServiceEnd']
    BakerFree = Baker['ServiceEnd']

    # Starting Simulation
    serviceId = 0
    numberOfWaitings = 0

    servicesTotal = len(serviceTimes)
    serviceTotalTime = sum(serviceTimes)

    while timeClock <= endSimu:

        print('\nt=', timeClock)
        AbleFree, BakerFree = getFree(AbleFree, BakerFree)

        try:
            #arrival event exist
            if queue or timeClock == arrivalTimes[0]:
                worker = getWorker(Able['ServiceEnd'],Baker['ServiceEnd'], timeClock)

                #There is services in the queue
                if queue and worker != 'wait':
                    waitService = queue.pop(0)
                    start = timeClock
                    serviceTime = waitService['ServiceTimes']
                    serviceId = waitService['serviceId']
                    print('waiting for customer..')
                else:
                    #There is no services in queue but there is a new service
                    print('new customer arrived..')
                    start = arrivalTimes.pop(0)
                    serviceTime = serviceTimes.pop(0)

                end = start + serviceTime

                #Able is now free after ending its service
                if worker == 'Able':
                    Able = {
                        'ServiceTime': serviceTime,
                        'ServiceStart': start,
                        'ServiceEnd': end
                    }

                    AbleFree = Able['ServiceTime'] - 1

                    print('Able is serving for', serviceTime, 's')

                #Baker is now free after ending its service
                elif worker == 'Baker':
                    Baker = {
                        'ServiceTime': serviceTime,
                        'ServiceStart': start,
                        'ServiceEnd': end
                    }

                    BakerFree = Baker['ServiceTime'] - 1

                    print('Baker is serving for', serviceTime, 's')
                
                #both Able and Baker are busy
                else:
                    queue = []
                    services = [serv['serviceId'] for serv in queue]
                    serviceId = timeClock

                    if serviceId not in services:
                        waitingAmount = waitTime(Able['ServiceEnd'], Baker['ServiceEnd'], timeClock)
                        queue.append({
                            'serviceId': serviceId,
                            'ServiceTimes': serviceTime,
                            'waitTime': waitingAmount
                        })
                        totalWaiting += waitingAmount
                        numberOfWaitings += 1

                    print('Able and Baker are busy, please wait..')
        except:
            pass

        time.sleep(1)
        timeClock += 1

    print('\nSimulation is DONE\n')

    print(
        'Average Waiting time of those who wait in queue d(n)= ', round(totalWaiting / numberOfWaitings, 2),
        '\nTime-average number in queue q(n)= ', round(totalWaiting / endSimu, 2),
        '\nTotal Busy Time B(t)= ', round(serviceTotalTime, 2),
        '\nUtilization u(n) of the worker= ', round(serviceTotalTime / 2 / endSimu, 2),
        '\nAverage service time= ', round(serviceTotalTime / servicesTotal, 2),
        '\nAverage waiting time= ', round(totalWaiting / servicesTotal, 2),
        '\nAverage time customer spends in the system= ', round((serviceTotalTime + totalWaiting) / servicesTotal, 2),
        '\nThroughput= ', round(servicesTotal / endSimu, 2),
    )
