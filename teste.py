from datetime import datetime
dateTimeObj = datetime.now()
timeStr = dateTimeObj.strftime("%H%M%S")
print('Current Timestamp : ', "1_"+timeStr)