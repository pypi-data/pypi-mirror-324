#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk,filedialog,messagebox as msg
import os,zipfile
import shutil as sh
from threading import Thread
import time
import json
import webbrowser
__version__ = "1.00"


class AorUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        self.root = tk.Tk(master)
        self.root.geometry("413x200")

        self.main_w = self.root.winfo_reqwidth()
        self.main_h = self.root.winfo_reqheight()
        self.center()

        self.root.resizable(False, False)
        self.root.title("All Of Resources {} - Minecraft 资源提取器".format(__version__))
        self.mcdir_t = ttk.Label(self.root, name="mcdir_t")
        self.mcdir_t.configure(text='选择.minecraft目录: ')
        self.mcdir_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=8)
        self.mcdir = ttk.Entry(self.root, name="mcdir")
        self.minecraftdir = tk.StringVar()
        self.minecraftdir_old = tk.StringVar()
        self.mcdir.configure(textvariable=self.minecraftdir)
        self.mcdir.bind("<KeyRelease>", self.mcver_update)
        self.mcdir.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            rely=0.0,
            width=248,
            x=124,
            y=8)
        self.mcdir_browse = ttk.Button(self.root, name="mcdir_browse")
        self.mcdir_browse.configure(text='...')
        self.mcdir_browse.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=25,
            x=376,
            y=8)
        self.mcdir_browse.configure(command=self.select_minecraft)
        self.mcver_t = ttk.Label(self.root, name="mcver_t")
        self.mcver_t.configure(text='选择版本: ')
        self.mcver_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=40)
        self.mcver = ttk.Combobox(self.root, name="mcver", state="readonly")
        self.mcversion = tk.StringVar()
        self.mcver.configure(textvariable=self.mcversion)
        self.mcver.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=277,
            x=124,
            y=40)
        self.extract_t = ttk.Label(self.root, name="extract_t")
        self.extract_t.configure(text='解压路径: ')
        self.extract_t.place(anchor="nw", relx=0.0, rely=0.0, x=8, y=70)
        self.extractdir = tk.StringVar()
        self.extract = ttk.Entry(self.root, name="extract", textvariable=self.extractdir)
        self.extract.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=248,
            x=124,
            y=70)
        self.extract_browse = ttk.Button(self.root, name="extract_browse")
        self.extract_browse.configure(text='...')
        self.extract_browse.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=25,
            x=376,
            y=70)
        self.extract_browse.configure(command=self.select_extract)
        self.content = ttk.Label(self.root, text="All Of Resources By SystemFileB\n给个Star awa\n\n注意：解压路径需要使用空文件夹")
        self.content.place(anchor="nw", x=8, y=95)
        self.progress = ttk.Progressbar(self.root, name="progress")
        self.prog = tk.IntVar()
        self.progress.configure(orient="horizontal", variable=self.prog, maximum=2000)
        self.progress.place(
            anchor="nw",
            height=22,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.0,
            width=281,
            x=8,
            y=168)
        self.start_b = ttk.Button(self.root, name="start_b")
        self.start_b.configure(text='开始',state="disabled")
        self.start_b.place(anchor="nw", height=22, width=50, x=355, y=168)
        self.start_b.configure(command=self.start)
        self.about_b = ttk.Button(self.root, name="about_b")
        self.about_b.configure(text='关于')
        self.about_b.place(anchor="nw", height=22, width=50, x=297, y=168)
        self.about_b.configure(command=self.about)

    def center(self):
        wm_min = self.root.wm_minsize()
        wm_max = self.root.wm_maxsize()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        """ `winfo_width` / `winfo_height` at this point return `geometry` size if set. """
        x_min = min(screen_w, wm_max[0],
                    max(self.main_w, wm_min[0],
                        413,
                        self.root.winfo_reqwidth()))
        y_min = min(screen_h, wm_max[1],
                    max(self.main_h, wm_min[1],
                        200,
                        self.root.winfo_reqheight()))
        x = screen_w - x_min
        y = screen_h - y_min
        self.root.geometry(f"{x_min}x{y_min}+{x // 2}+{y // 2}")

    def run(self):
        self.root.mainloop()

    def select_minecraft(self):
        dir=filedialog.askdirectory(title="选择.minecraft目录")
        if dir:
            self.minecraftdir.set(dir)
            self.mcver_update()

    def mcver_update(self,e=None):
        if os.path.exists(self.minecraftdir.get()) and self.minecraftdir.get().endswith(".minecraft"):
            if self.minecraftdir.get() != self.minecraftdir_old.get():
                self.mcver.configure(values=os.listdir(os.path.join(self.minecraftdir.get(),"versions")))
                self.mcver.current(0)
            self.minecraftdir_old.set(self.minecraftdir.get())
        if os.path.exists(self.extractdir.get()) and self.mcversion.get() and os.listdir(self.extractdir.get())==[]:
            self.start_b.configure(state="normal")
            self.content.configure(text="等待任务开始...")

    def select_extract(self):
        dir=filedialog.askdirectory(title="选择解压路径")
        if dir:
            self.extractdir.set(dir)
            self.mcver_update()

    def start(self):
        self.start_b.configure(state="disabled")
        self.root.protocol("WM_DELETE_WINDOW", self.donotclose)
        Thread(target=self.task, args=(self.mcversion.get(), self.extractdir.get())).start()

    def task(self, version, path):
        self.content.configure(text="Step 0: 确保版本完整...")
        jarPath=os.path.join(self.minecraftdir.get(), "versions", version, version + ".jar")
        jsonPath=os.path.join(self.minecraftdir.get(), "versions", version, version + ".json")
        with open(os.path.join(self.minecraftdir.get(), "versions", version, version + ".json"),"r",encoding="utf-8") as f:
            version_json = json.load(f)
            f.close()
        assetIndexPath=os.path.join(self.minecraftdir.get(), "assets/indexes", version_json["assetIndex"]["id"] + ".json")
        if os.path.exists(jarPath) and os.path.exists(jsonPath) and os.path.exists(assetIndexPath):
            if os.path.exists(jarPath) and os.path.exists(jsonPath) and os.path.exists(assetIndexPath):
                step1="Step 1: 解压{}.jar\n".format(version)
                self.content.configure(text=step1)
                with zipfile.ZipFile(os.path.join(self.minecraftdir.get(), "versions", version, version + ".jar")) as jar:
                    files = [f for f in jar.namelist() if f.startswith("assets/") or f.startswith("data/")]
                    progress = 0
                    files_len = len(files)
                    self.content.configure(text=step1+"0% ({}/{})".format(progress, files_len))
                    for file in files:
                        jar.extract(file, path)
                        progress+=1
                        self.prog.set((progress/files_len)*1000)
                        self.content.configure(text=step1+"{}% ({}/{})".format(round((progress/files_len)*100), progress, files_len))
                time.sleep(0.5)


            time.sleep(0.5)
            self.step2="Step 2: 根据 {} 复制文件\n".format(version_json["assetIndex"]["id"] + ".json")
            cpu_count = os.cpu_count()
            self.content.configure(text=self.step2+"获取文件列表...")
            with open(assetIndexPath,"r",encoding="utf-8") as f:
                self.assets_assetIndex_json = json.load(f)
                f.close()
            assets = self.assets_assetIndex_json["objects"].keys()
            assets_threads = []
            self.assets_length = len(assets)
            self.assets_count = 0

            # 计算每个线程应该处理的元素数量
            elements_per_thread = self.assets_length // cpu_count
            # 计算剩余的元素数量
            remaining_elements = self.assets_length % cpu_count

            for i in range(cpu_count):
                # 计算当前线程应该处理的元素范围
                start_index = i * elements_per_thread
                end_index = start_index + elements_per_thread + (1 if i == cpu_count - 1 else 0) * remaining_elements
                # 获取当前线程应该处理的子列表
                sublist = list(assets)[start_index:end_index]
                # 创建并启动线程
                thread = Thread(target=self.copy_assets, args=(sublist, path))
                thread.start()
                assets_threads.append(thread)

            while any(thread.is_alive() for thread in assets_threads):
                time.sleep(0.1)
            time.sleep(0.5)
            self.content.configure(text="All Of Resources By SystemFileB\n给个Star awa")
            msg.showinfo("All Of Resources", "任务完成！")
            self.prog.set(0)
        else:
            self.content.configure(text="Step 0: 确保版本完整...\n\n错误：版本文件缺失\n请你补全版本文件或启动一次游戏")
            msg.showerror("All Of Resources", "版本文件缺失！\n请你补全版本文件或启动一次游戏")
        

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.mcver_update()

    def advcopy(self,source_file, destination_file):
        # 获取目标文件的目录路径
        destination_directory = os.path.dirname(destination_file)
        # 检查目标目录是否存在，如果不存在则创建它
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        
        # 复制文件
        sh.copy(source_file, destination_file)

    def copy_assets(self, keys, path):
        for asset in keys:
            fileHash = self.assets_assetIndex_json["objects"][asset]["hash"]
            filePath = os.path.join(self.minecraftdir.get(), "assets", "objects", fileHash[0:2], fileHash)
            self.advcopy(filePath, os.path.join(path, "assets", asset))
            self.assets_count+=1
            self.prog.set(1000+(self.assets_count/self.assets_length)*1000)
            self.content.configure(text="{}{}% ({}/{})".format(self.step2, round((self.assets_count/self.assets_length)*100), self.assets_count, self.assets_length))

    def donotclose(self,e=None):
        pass


    def about(self):
        if msg.askyesno("All Of Resources", "All Of Resources By SystemFileB\n给个Star awa\n\n是否进入项目的github？"):
            webbrowser.open("https://github.com/SystemFileB/all-of-resources")

def main():
    app = AorUI()
    app.run()
if __name__ == "__main__":
    main()