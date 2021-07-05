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
Например, 10-12-2021-12:15-scan.txt"""

# ps a -o "user" -o "|%C" -o "|%c" -o "|%z"

TEST_DATA = r"""
USER    |%CPU|COMMAND        |   VSZ \n
root    | 0.0|bash           |  4240 \n
root    | 0.0|sh             |  2608 \n
root    | 0.0|mc             | 14832 \n
root    | 0.0|bash           |  4240 \n
root    | 0.0|nano           |  3716 \n
root    | 0.0|python3        | 12988 \n
root    | 0.0|su             |  4492 \n
testuser| 0.0|bash           |  4240 \n
testuser| 0.0|ps             |  5896 \n
"""

#result = str(subprocess.check_output(['ps', '-eo', 'user,size,pmem,pcpu,cmd'])).split(r'\n')
result = TEST_DATA.split(r'\n')
processes_count = len(result) - 1
result = [line.split('|') for line in result]
data = {}
resulting_proc_list = []
max_mem_user = {'id': 0, 'value': 0}
max_cpu_user = max_mem_user.copy()
mem_used = 0
cpu_used = 0
for process in range(result):
    data['name'] = process[0]
    data['cpu'] = float(process[1])
    data['size'] = int(process[2])
    resulting_proc_list.append(data)
    if max_mem_user['value'] < data['size']:
        max_mem_user['value'] = data['size']
        max_mem_user['id'] = len(resulting_proc_list)
    if max_cpu_user['value'] < data['cpu']:
        max_cpu_user['value'] = data['cpu']
        max_cpu_user['id'] = len(resulting_proc_list)
    cpu_used += data['cpu']
    mem_used += data['size']



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
