def log(message, typeValueTraceback = None):
    logData = ''
    if (message):
        logData = logData + message + '\n'

    if (typeValueTraceback):
        print typeValueTraceback

    if (typeValueTraceback) and isinstance(typeValueTraceback, list) and len(typeValueTraceback) == 3:
        logData = 'Type: ' + typeValueTraceback[0] + '\n'
        logData = 'Value: ' + typeValueTraceback[1] + '\n'
        logData = 'Trace back: ' + typeValueTraceback[2] + '\n'

    print logData
