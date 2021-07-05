import subprocess

"""
TODO:
Скрипт-парсер системных процессов команды 'ps aux' на subprocess. 
Парсер должен вывести в стандартный вывод в качестве результата работы:
    Отчёт о состоянии системы: 
    Процессов запущено: 833
    Пользовательских процессов: root: 533 user1: 231 ...
    Всего памяти используется: 553.3 mb
    Всего CPU используется: 33.2% 
    Больше всего памяти использует: (%имя процесса, первые 20 символов если оно длиннее) 
    Больше всего CPU использует: (%имя процесса, первые 20 символов если оно длиннее)
Отчёт должен быть сохранён в отдельный txt файл с названием текущей даты и времени проверки. 
Например, 10-12-2021-12:15-scan.txt

"""
"""command - ps a -o "user" -o "|%C" -o "|%c" -o "|%z""""

TEST_DATA = r"""
USER      SIZE %CPU CMD \n
root       696  0.0 /bin/bash \n
root       320  0.0 /bin/sh \n
root      3156  0.0 mc \n
root       696  0.0 bash -rcfile .bashrc \n
root       760  0.0 nano \n
root      3220  0.0 python3 \n
root       588  0.0 su testuser \n
testuser   696  0.0 bash \n
testuser  1044  0.0 ps -eo user,size,pcpu,cmd \n
"""

#result = str(subprocess.check_output(['ps', '-eo', 'user,size,pmem,pcpu,cmd'])).split(r'\n')
result = TEST_DATA.split(r'\n')
result = [line.split() for line in result]
users = [line[0] for line in result[1:-1]]
processes_count = len(users)
users = list(set(users))
processes = [line[-1] for line in result[1:-1]]
print(processes)
data = {}
resulting_proc_list = []
for process in range(len(processes)):
    data['name'] = processes[process]
    data['size'] = result[process + 1][1]
    data['cpu'] = result[process + 1][2]
    resulting_proc_list.append(data)

print(resulting_proc_list)

mem_used = 0
cpu_used = 0
most_mem = ''
most_cpu = ''

report = 'Отчет о состоянии системы:' + '\n'
report += "Пользователи системы: '" + "', '".join(users) + "'" + '\n'
report += 'Процессов запущено: ' + str(processes_count) + '\n'
report += 'Всего памяти используется: ' + str(mem_used) + ' mb\n'
report += 'Использование CPU: ' + str(cpu_used) + '%\n'
report += 'Больше всего памяти использует: ' + str(most_mem)[:20] + '%\n'
report += 'Больше всего CPU использует: ' + str(most_cpu)[:20] + '%\n'

print(report)
