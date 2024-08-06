import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import os

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyPythonService"
    _svc_display_name_ = "My Python Service"
    _svc_description_ = "This is a sample Python service that logs the time every minute"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        self.main()

    def main(self):
        log_file_path = "C:/log.txt"  # 로그 파일 경로 설정
        while True:
            with open(log_file_path, "a") as log:
                log.write(f"Service is running at {time.ctime()}\n")
            time.sleep(60)  # 60초마다 실행

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
