import csv
import os


def run_jmeter(caseName, num_threads, ramp_time, duration):
    this_dir = os.getcwd()
    new_scripts_jmx = os.path.join("scripts",f"{caseName}_{num_threads}_{ramp_time}_{duration}"+".jmx")
    new_scripts_jtl = os.path.join("jtl",f"{caseName}_{num_threads}_{ramp_time}_{duration}"+".jtl")
    new_scripts_report = os.path.join("report", f"{caseName}_{num_threads}_{ramp_time}_{duration}")

    if not os.path.exists("scripts"):
        os.mkdir("scripts")
    if not os.path.exists("jtl"):
        os.mkdir("jtl")
    if not os.path.exists("report"):
        os.mkdir("report")

    ord_scripts = os.path.join(this_dir,caseName+".jmx")
    with open(new_scripts_jmx,mode="w") as f:
        with open(ord_scripts,mode="r",encoding="utf-8") as ff:
            for i in ff.readlines():
                f.write(i.replace('num_threads">num_threads</stringProp>', 'num_threads">%s</stringProp>' % num_threads)  # 替换并发数
                    .replace('ramp_time">ramp_time</stringProp>', 'ramp_time">%s</stringProp>' % ramp_time)  # 替换步长
                    .replace('scheduler">false</boolProp>', 'scheduler">true</boolProp>')  # 勾选通过时间判断结束
                    .replace('duration">duration</stringProp>', 'duration">%s</stringProp>' % duration)  # 替换执行时间
                    .replace('name="LoopController.loops">1</stringProp>',
                            'name="LoopController.loops">-1</stringProp>'))


    os.system(f"jmeter -n -t {new_scripts_jmx} -l {new_scripts_jtl} -e -o {new_scripts_report}")

def csv_reader(path):
    with open(path,"r") as f:
        data = csv.reader(f)
        for i in data:
            run_jmeter(*i)

if __name__ == "__main__":
    csv_reader("./load.csv")
