import subprocess
from datetime import datetime

"""
TODO:
Скрипт-парсер системных процессов команды 'ps aux' на subprocess. 
Парсер должен вывести в стандартный вывод в качестве результата работы:
    Отчёт о состоянии системы: 
    !Процессов запущено: 833
    !Пользовательских процессов: root: 533 user1: 231 ...
    !Всего памяти используется: 553.3 mb
    !Всего CPU используется: 33.2% 
    Больше всего памяти использует: (%имя процесса, первые 20 символов если оно длиннее) 
    Больше всего CPU использует: (%имя процесса, первые 20 символов если оно длиннее)
Отчёт должен быть сохранён в отдельный txt файл с названием текущей даты и времени проверки. 
Например, 10-12-2021-12:15-scan.txt"""

# ps a -o "user" -o "|%C" -o "|%c" -o "|%z"

TEST_DATA = r"""
USER    |%CPU|COMMAND        |   VSZ \n
root    | 0.0|bash           |  4240 \n
root    | 0.3|sh             |  2608 \n
root    | 0.0|mc             | 14832 \n
root    | 0.2|bash           |  4240 \n
root    | 0.0|nano           |  3716 \n
root    | 0.0|python3        | 12988 \n
root    | 0.0|su             |  4492 \n
testuser| 0.1|bash           |  4240 \n
testuser| 0.5|ps             |  5896 \n
"""

result = str(subprocess.check_output(['ps', 'a', '-o', 'user', '-o', '|%C', '-o', '|%c', '-o', '|%z'])).split(r'\n')
# result = TEST_DATA.split(r'\n')
result = [line.split('|') for line in result]
users = {user[0]: 0 for user in result[1:-1]}
data = {}
processes_by_user = {}
resulting_proc_list = []
max_mem_user = {'id': 0, 'value': 0}
max_cpu_user = max_mem_user.copy()
mem_used = 0
cpu_used = 0
processes_count = 0
for process in range(1, len(result[1:])):
    # Если число элементов текущей строки меньше, чем у предыдущего, значит пора выходить
    if len(result[process]) < len(result[process - 1]):
        break
    # Посчитаем количество процессов
    processes_count += 1
    # Посчитаем сколько процессов выходит на каждого пользователя
    for user in users:
        if user == result[process][0]:
            if user in processes_by_user.keys():
                processes_by_user[user] += 1
            else:
                processes_by_user[user] = 1
    # Соберем данные
    data['name'] = result[process][0]
    data['cpu'] = float(result[process][1])
    data['process'] = result[process][2]
    data['size'] = int(result[process][3])
    resulting_proc_list.append(data)
    # Посчитаем суммарное использование ЦПУ и памяти
    cpu_used += data['cpu']
    mem_used += data['size']
    # Найдем процесс, использующий больше всего памяти
    if max_mem_user['value'] < data['size']:
        max_mem_user['value'] = data['size']
        max_mem_user['id'] = data['process']
    # Найдем процесс, использующий больше всего ЦПУ
    if max_cpu_user['value'] < data['cpu']:
        max_cpu_user['value'] = data['cpu']
        max_cpu_user['id'] = data['process']

most_mem = ''
most_cpu = ''

report = 'Отчет о состоянии системы:' + '\n'
report += "Пользователи системы: '" + " , '".join([user.strip() for user in processes_by_user.keys()]) + "'\n"
report += 'Процессов запущено: ' + str(processes_count) + '\n'
processes_by_user = ", ".join([list(processes_by_user.keys())[value].strip() + ': ' +
                               str(processes_by_user[list(processes_by_user.keys())[value]])
                               for value in range(len(processes_by_user))])
report += "Пользовательских процессов: " + processes_by_user + '\n'

report += 'Всего памяти используется: ' + (mem_used / 1024).__format__('0.00f') + ' mb\n'
report += 'Использование CPU: ' + str(cpu_used) + '%\n'
report += 'Больше всего памяти использует: ' + max_mem_user['id'][:20] + '\n'
report += 'Больше всего CPU использует: ' + str(max_cpu_user['id'])[:20] + '\n'

print(report)
with open(datetime.strftime(datetime.now(), '%d-%m-%Y-%H_%M-scan.txt'), 'wb') as file:
    file.write(report.encode('utf-8'))
