Extract the system logs from SecurityCenter. 

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Use the interactive menu
  -n number_of_logs, --number-of-logs number_of_logs
                        define the number of logs to retrieve (default: 500)
  -o output_filename, --output output_filename
                        define the output file name (default: logs-[current
                        date].csv
  -H output_filename, --host output_filename
                        define the hostname of the SecurityCenter instance




Compile the .py code with your host included using the following command: (may require installation)

pyinstaller.exe SCLogs.py --onefile
