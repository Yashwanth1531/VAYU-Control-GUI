import tkinter as tk
from tkinter import Label, Button, Entry
import serial
from tkinter import messagebox

import serial
import serial.tools.list_ports as ports

class RootGUI():
    def __init__(self):
        self.root = tk.Tk();                        # root is the instance of the class Tk
        self.root.title("VAYU-I GUI");              # root.title defines the title of the application
        self.root.geometry("635x420");              # root.geometry defines the default size of the application
        self.root.config(bg="white");               # root.config defines the backgroud color of the application

class ArduinoController():
    def __init__(self):
        self.COM_lists = [];

    def getCOMlist(self):
        portList = list(ports.comports());
        ## Considering only the fist words: which has the COM-ID
        self.COM_lists = [com[0] for com in portList];
    
    def SerialOpen(self, gui):
        ## gui: Basically is the instance of the COMGUI
        ## When estabilishing serial connection, the serial port could be busy.
        ## is_open is a method in the class serial.Serial() that returns bool-type for status of serial-port open/not-open.
    
        try:
            self.serial_handle.is_open;
        except:
            ## click_COM.get() and click_baud.get()-->Returns the tk.StringVar(), 
            ## which is a handel that stores the selection from drop-down.
            Port_Connected = gui.clicked_COM.get();
            Baud_Selected  = gui.clicked_baud.get();
            ## Using serial.Serial(port,baudrate,timeout) command for opening connection.
            self.serial_handle = serial.Serial();
            self.serial_handle.port     = Port_Connected;
            self.serial_handle.baudrate = Baud_Selected;
            self.serial_handle.timeout  = 1;         # 100ms
            
        try:
            ## CaseA: if the Port is already busy, then the status is updated to "True" without connecting.
            ## CaseB: if the Port is not busy, then the status is updated to "True" after connecting to the port.
            if self.serial_handle.is_open:
                self.serial_handle.status = "True";
            else:
                Port_Connected = gui.clicked_COM.get();
                Baud_Selected  = gui.clicked_baud.get();
                self.serial_handle = serial.Serial();
                self.serial_handle.port     = Port_Connected;
                self.serial_handle.baudrate = Baud_Selected;
                self.serial_handle.timeout  = 1;         # 1000ms
                self.serial_handle.open();
                self.serial_handle.status = "True";
        ## Exception to our try is: The status check for a port either failed or the connection attempt failed.
        ## Hence, the status of the Port if it is open: "False".
        except:
            # self.serial_handle = serial.Serial();
            self.serial_handle.status = "False";
            
    def SerialClose(self):
        try:
            self.serial_handle.is_open;
            self.serial_handle.close();
            self.serial_handle.status = "False";
        
        except:
            self.serial_handle.status = "False";
    
    def send_command(self, command):
        self.serial_handle.write(command.encode("utf-8"));


class GUI():
    def __init__(self, root):
        super().__init__();
        self.root = root;

        self.arduino = ArduinoController();

        self.create_connect_frame();
        self.create_quick_frame();
        self.create_Motor_select_frame();
        self.create_speed_set_frame();
    
    def create_connect_frame(self):
        self.connect_frame = tk.LabelFrame(self.root,text="COM Manager", padx=5, pady=5, fg="gray", bg="white");
        self.label_COM  = tk.Label(self.connect_frame, text="Available Port(s): ", fg="black", bg="white",width=15, anchor="w");
        self.label_baud   = tk.Label(self.connect_frame, text="Baud Rate: ", bg="white", fg="black", width=15, anchor="w");
    
        self.COMOptionMenu();
        self.BaudOptionMenu();
        self.btn_Refresh = tk.Button(self.connect_frame,text="Refresh",width=10,command=self.COM_Refresh);
        self.btn_Connect = tk.Button(self.connect_frame,text="Connect",width=10,state="disable",command=self.serial_connect);
        self.connect_frame.grid(row=0,column=0, rowspan=3,columnspan=3, padx=5,pady=5);
        ## LABELS                               ## DROP-DOWNS                           ## BUTTONS
        self.label_COM.grid(column=1,  row=1);  self.drop_COM.grid(column=2, row=1);    self.btn_Refresh.grid(column=3, row=1);
        self.label_baud.grid(column=1, row=2);  self.drop_baud.grid(column=2, row=2);   self.btn_Connect.grid(column=3, row=2);

    def COMOptionMenu(self):
        """
        Method that defines the COM port dorp-down menu in the COMGUI frame.
        """
        self.arduino.getCOMlist();
        self.clicked_COM = tk.StringVar();
        # The first string "-" is set as default untill option is clicked in the drop-down.
        self.clicked_COM.set("-"); 
        self.drop_COM = tk.OptionMenu(self.connect_frame, self.clicked_COM, *self.arduino.COM_lists, command=self.select_ctrl);
        self.drop_COM.config(width=10);
    
    def BaudOptionMenu(self):
        """
        Method that defines the Baud rate dorp-down menu in the COMGUI frame.
        """
        bauds = ["300","600","1200","2400","4800","9600","14400","19200","28800"];
        #3 This acts as handle for stroing the clicked string from the drop-down menu.
        self.clicked_baud = tk.StringVar();
        # The first string "-" is set as default untill option is clicked in the drop-down.
        self.clicked_baud.set("-");
        self.drop_baud = tk.OptionMenu(self.connect_frame, self.clicked_baud, *bauds, command=self.select_ctrl);
        self.drop_baud.config(width=10);


    def create_quick_frame(self):
        self.quick_frame    = tk.LabelFrame(self.root, text="Quick Control", padx=5, pady=5, fg="gray", bg="white",font=("Lato",9));
        self.arm_button     = Button(self.quick_frame, text="Arm", height=2, width=15, state="disable", command=self.arm_button_clicked,font=("Lato",9));
        self.Stop_button    = Button(self.quick_frame, text="STOP", height=2, width=15, state="disable", command=self.stop_all_clicked,font=("Lato",9));

        self.quick_frame.grid(row=1, column=3, rowspan=1, columnspan=2, padx=20, pady=5);
        self.arm_button.grid(row=0, column=0);
        self.Stop_button.grid(row=0, column=1);

    def create_Motor_select_frame(self):
        self.Motor_select_frame = tk.LabelFrame(self.root, text="Motor Select", padx=5, pady=5, fg="gray", bg="white",font=("Lato",9));


        self.M0 = Button(self.Motor_select_frame, text="M0", fg="black", height=3, width=10, anchor="center", state="disable", command=self.Motor_selected0,font=("Lato",9,"bold"));
        self.M1 = Button(self.Motor_select_frame, text="M1", fg="black", height=3, width=10, anchor="center", state="disable", command=self.Motor_selected1,font=("Lato",9,"bold"));
        self.M2 = Button(self.Motor_select_frame, text="M2", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M3 = Button(self.Motor_select_frame, text="M3", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M4 = Button(self.Motor_select_frame, text="M4", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M5 = Button(self.Motor_select_frame, text="M5", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M6 = Button(self.Motor_select_frame, text="M6", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M7 = Button(self.Motor_select_frame, text="M7", fg="black", height=3, width=10, anchor="center", state="disable");
        self.M8 = Button(self.Motor_select_frame, text="M8", fg="black", height=3, width=10, anchor="center", state="disable");
        
        self.Motor_select_frame.grid(row=3, column=0, rowspan=3,columnspan=3, padx=20, pady=10);
        self.M0.grid(row=0, column=0, padx=10, pady=10); self.M1.grid(row=0, column=1, padx=10, pady=10); self.M2.grid(row=0, column=3, padx=10, pady=10);
        self.M3.grid(row=1, column=0, padx=10, pady=10); self.M4.grid(row=1, column=1, padx=10, pady=10); self.M5.grid(row=1, column=3, padx=10, pady=10);
        self.M6.grid(row=2, column=0, padx=10, pady=10); self.M7.grid(row=2, column=1, padx=10, pady=10); self.M8.grid(row=2, column=3, padx=10, pady=10);

    def create_speed_set_frame(self):
        self.speed_set_frame = tk.LabelFrame(self.root, text="Speed Select", padx=5, pady=5, fg="gray", bg="white",font=("Lato",9));

        self.m0_value = tk.IntVar(value=0);
        self.m1_value = tk.IntVar(value=0);
   
        self.down_button = Button(self.speed_set_frame, text="▼", fg="black", width=5, anchor="center", state="disabled", command=lambda: self.Plus_Minus_fun(-1),font=("Lato",9));
        self.entry       = Entry(self.speed_set_frame, textvariable=self.m0_value, state='disabled', fg="black",bg="#E6E6E6", justify="center", width=10,font=("Lato",12));              
        self.up_button   = Button(self.speed_set_frame, text="▲", fg="black", width=5, anchor="center", state="disabled", command=lambda: self.Plus_Minus_fun(1),font=("Lato",9));

        self.set_speed_btn = Button(self.speed_set_frame, text="SET", fg="black", height=2, width=10, anchor="center", state="disabled", command=self.update_speed,font=("Lato",9));

        self.speed_set_frame.grid(row=4, column=3, padx=10, pady=10);
        self.down_button.grid(row=0, column=1); self.entry.grid(row=0, column=2, padx=5); self.up_button.grid(row=0, column=3); 
        self.set_speed_btn.grid(row=1, column=2);
    
    #################################################################################################################################################################################################################
    
    def select_ctrl(self,widget):
        """
        Method to keep the connect button disabled untill all the conditions are satisfied.
        """
        # print(f"COM/Baud-rate selected: {self.clicked_COM.get(), self.clicked_baud.get()}");
        ## This requires another argument because the StringVar is also passed.
        ## self.clicked_COM stores the StringVar--> which option was selected. Hence, self.clicked_COM.get() returns the option selected.
        # print(self.clicked_COM.get()); 
        ## CaseA: when either of the selected are "-" --> Both are not selected:
        ## This works because we hard-coded set the default value to "-".
        if "-" in self.clicked_COM.get() or "-" in self.clicked_baud.get():
            self.btn_Connect["state"] = "disable";
        ## CaseA: when both of the drop-down are selected:
        else:
            self.btn_Connect["state"] = "active";
    def COM_Refresh(self):
        """
        Method to destroy COM-Port list and recheck. Also disabling the connect button untill new 
        selection is made.
        """
        # print("COM_Refresh");
        ## DESTROY THE COM WIDGET;
        self.drop_COM.destroy(); self.drop_baud.destroy();
        ## RUN THE COMOptionMenu METHOD AGAIN TO GET REFRESHED COM-PORTS, ALSO RESETS THE DEFAULT UNTILL SELECTION.
        ## ALSO RE-PUBLISH IS REQUIRED
        self.COMOptionMenu(); self.BaudOptionMenu();
        self.drop_COM.grid(column=2, row=1); self.drop_baud.grid(column=2, row=2); # PUBLISH
        ## SIMULATNEOUSLY, THE CONNECT BUTTON NEEDS TO BE DISABLED UNTILL
        ## NEW SELECTION IS MADE! AFTER THE REFRESH. 
        dummy_logic = []; # Passing dummy to disable Connect button
        # Here CaseA is passed as the default value is set again to "-" inside the COMOptionMenu method.
        self.select_ctrl(dummy_logic); 
    
    def serial_connect(self):
        # print(f"Clicked {self.btn_Connect["text"]}");
        ## Calling the serial-initialization function from the Arduino_class
        ## We have access through main-file passing the instance of SerialCtrl as "serial" here.
        ## SerialOpen method has gui as argument, which is the instance of our RootGUI. To access selected options.
        
        
        ## CaseA: if the button was saying "Connect" when clicked.
        ## We are yet to connect!
        if "Connect" in self.btn_Connect["text"]:
            ## Attempt connection:
            self.arduino.SerialOpen(self);
            ## CaseA1: When connection is established.
            if self.arduino.serial_handle.status:
                self.btn_Connect["text"]    = "Disconnect";
                ## Diabling the btns and drop-downs when connected.
                self.btn_Refresh["state"]   = "disable";
                self.drop_COM["state"]      = "disable";
                self.drop_baud["state"]     = "disable";
                self.arm_button["state"]    = "active";
                self.M0["state"]            = "active";
                self.M1["state"]            = "active";
                Info_Message = f"Successfully established UART connection using {self.clicked_COM.get()}";
                messagebox.showinfo(title = "Infromation",
                                    message = Info_Message);
                
            ## CaseA2: When connection was not established. Show an error message.
            else:
                Error_Message = f"Failed to establish UART connection using {self.clicked_COM.get()}";
                messagebox.showerror(title = "Error",
                                     message = Error_Message);
        
        ## CaseA: if the button was saying "Disconnect" when clicked.
        else:
            ## Attempt disconnection:
            self.arduino.SerialClose();
            self.btn_Connect["text"]    = "Connect";
            ## Keeping the btns and drop-downs active after disconnected.
            self.btn_Refresh["state"]   = "active";
            self.drop_COM["state"]      = "active";
            self.drop_baud["state"]     = "active";
            self.arm_button["state"]    = "disable";
            self.M0["state"]            = "disable";
            self.M1["state"]            = "disable";
            Info_Message = f"Successfully disconnected UART connection from {self.clicked_COM.get()}";
            messagebox.showwarning(title ="Warning",
                                message = Info_Message);

    def arm_button_clicked(self):
        self.arduino.send_command("Arm");
        self.arm_button["state"]    = "disable";
        self.M0["state"]            = "active";
        self.M1["state"]            = "active";
        self.Stop_button["state"]   = "active";
        Info_Message = f"Successfully armed and calibrated all the ESCS.\n Kindly wait untill all the ESCs give out confirmation beeps.";
        messagebox.showinfo(title = "Infromation", message = Info_Message);
    
    def stop_all_clicked(self):
        self.Serial_key = "-1,-1,-1";
        # print(f"Serial_key input: {self.Serial_key}");
        self.arduino.send_command(self.Serial_key);
        self.motorValue_list = [self.m0_value.get(), self.m1_value.get()];
        Warning_Message = f"All the motors were fully stopped from\nMax throttle: {max(self.motorValue_list)}%. Ensure that there are no hardware issues because of this action.";
        messagebox.showwarning(title = "Infromation", message = Warning_Message);

    def Plus_Minus_fun(self, increment):
        if self.MotorID_key == "0,0":
            current_value = self.m0_value.get();
            new_value = max(0, min(100, current_value + increment));
            self.m0_value.set(new_value);
        elif self.MotorID_key == "0,1":
            current_value = self.m1_value.get();
            new_value = max(0, min(100, current_value + increment));
            self.m1_value.set(new_value);
        
    
    def Motor_selected0(self):
        self.MotorID_key            = "0,0";
        self.entry["state"]         = "normal";
        self.entry["textvariable"]  = self.m0_value;
        self.M0["state"]            = "disable";
        self.M1["state"]            = "active";
        self.set_speed_btn["state"] = "active";
        self.up_button["state"]     = "active";
        self.down_button["state"]   = "active";
    def Motor_selected1(self):
        self.MotorID_key            = "0,1";
        self.entry["state"]         = "normal";
        self.entry["textvariable"]  = self.m1_value;
        self.M0["state"]            = "active";
        self.M1["state"]            = "disable";
        self.set_speed_btn["state"] = "active";
        self.up_button["state"]     = "active";
        self.down_button["state"]   = "active";

    def update_speed(self):
        if self.MotorID_key == "0,0":
            speed = self.m0_value.get();
        elif self.MotorID_key == "0,1":
            speed = self.m1_value.get();
        
        self.Serial_key = self.MotorID_key + "," + str(speed);
        # print(f"Serial_key input: {self.Serial_key}");
        self.arduino.send_command(self.Serial_key);
    
        
     

if __name__ == "__main__":
    RootGUI();
    ArduinoController();
    GUI();
