import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.font as tkFont
import cv2
import subprocess
import os

class MediaViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detector")

        self.canvas = tk.Canvas(root, width=900, height=500,bg="#669999")
        self.canvas.pack()

############################################
        def on_hover(event):
            event.widget['background'] = 'lightblue'
        def on_leave(event):
            event.widget['background'] = 'SystemButtonFace'
##############################################

        ft = tkFont.Font(family='Helvetica', size=10)
        self.load_button = tk.Button(root, text="Load Media", command=self.load_media, font=ft,  justify="center")
        self.load_button.place(x=200, y=370, width=100, height=25)
        self.load_button.bind("<Enter>", on_hover)
        self.load_button.bind("<Leave>", on_leave)

        self.convert_button = tk.Button(root, text="Process File",font=ft)
        self.convert_button.place(x=385, y=450, width=130, height=25)
        self.convert_button.bind('<Button-1>', self.weapon_detect) 
        self.convert_button.bind('<Button-3>', self.object_detect) 
        self.convert_button.bind("<Enter>", on_hover)
        self.convert_button.bind("<Leave>", on_leave)
                
        self.run_camera_button = tk.Button(root, text="Run Camera Detection",font=ft)
        self.run_camera_button.place(x=350, y=420, width=200, height=25)
        self.run_camera_button.bind('<Button-1>', self.run_camera_detection_weapon) 
        self.run_camera_button.bind('<Button-3>', self.run_camera_detection_object)
        self.run_camera_button.bind("<Enter>", on_hover)
        self.run_camera_button.bind("<Leave>", on_leave) 

        self.file_path = None

        self.input_title_label = tk.Label(root, text="Input", font=('Helvetica', 12, 'bold'))
        self.input_title_label.place(x=210, y=10)  

        self.output_title_label = tk.Label(root, text="Output", font=('Helvetica', 12, 'bold'))
        self.output_title_label.place(x=600, y=10)  

        self.original_canvas = tk.Canvas(root, width=400, height=300,bg="#669999")
        self.original_canvas.place(x=50, y=50)

        self.processed_canvas = tk.Canvas(root, width=400, height=300,bg="#669999")
        self.processed_canvas.place(x=450, y=50)

    def load_media(self):
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            if self.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.show_image(self.file_path, self.original_canvas)
            elif self.file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                self.show_video(self.file_path)
            else:
                print("Unsupported file format.")

    def show_image(self, file_path, canvas):
        image = Image.open(file_path)
        image = image.resize((400, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        ###############
        canvas.delete("all")
        ###############
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

    def show_video(self, file_path):
        while True:
            cap = cv2.VideoCapture(file_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (400, 300))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)

                ###################
                self.original_canvas.delete("all")
                #####################
                self.original_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.original_canvas.image = photo
                self.root.update_idletasks()
                self.root.update()
            cap.release()

    def show_image_process(self, file_path):
        self.show_image(file_path, self.processed_canvas)

    def show_video_process(self, file_path):
        while True:
            cap = cv2.VideoCapture(file_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (400, 300))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)

                ###################
                self.processed_canvas.delete("all")
                #####################
                self.processed_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.processed_canvas.image = photo
                self.root.update_idletasks()
                self.root.update()
            cap.release()


    def weapon_detect(self,event):
        if not self.file_path:
            print("Please load a media file first.")
            return

        filePath = self.file_path
        fileName= os.path.basename(filePath)
        command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best.pt --conf 0.3 --exist-ok --source {self.file_path}"
        subprocess.run(command, shell=True)
        print("Process COMPLETE")
        output_file_path = f"runs/detect/exp/{fileName}"  
        if self.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.show_image_process(output_file_path)
        elif self.file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.show_video_process(output_file_path)
    
    def object_detect(self,event):
        if not self.file_path:
            print("Please load a media file first.")
            return
        filePath = self.file_path
        fileName= os.path.basename(filePath)
        command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\last_traffic.pt --conf 0.3 --exist-ok --source {self.file_path}"
        # command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best5mGitDuongcongnha.pt --conf 0.3 --exist-ok --source {self.file_path}"
        # command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best5sGitDuongcongnha.pt --conf 0.3 --exist-ok --source {self.file_path}"
        subprocess.run(command, shell=True)
        print("Process COMPLETE")
        output_file_path = f"runs/detect/exp/{fileName}"  
        if self.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.show_image_process(output_file_path)
        elif self.file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.show_video_process(output_file_path)

    def run_camera_detection_weapon(self,event):
        command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best.pt --conf 0.3 --exist-ok --source 0"
        subprocess.run(command, shell=True)

    def run_camera_detection_object(self,event):
        command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\last_traffic.pt --conf 0.3 --exist-ok --source 0"
        # command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best5mGitDuongcongnha.pt --conf 0.3 --exist-ok --source 0"
        # command = f"python detect.py --weights runs\\train\yolov5s_results\weights\\best5sGitDuongcongnha.pt --conf 0.3 --exist-ok --source 0"
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaViewerApp(root)
    root.mainloop()
