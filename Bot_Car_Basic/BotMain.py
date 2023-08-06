import webbrowser
import serial

from tkinter import *
import tkinter as tk

import BotOBDIIcmd as cmd
from CA_Parametter import color
from CA_Parametter import text
from CA_Parametter import size
from CA_Parametter import string_handling
#Thư viện xử lí trợ lý đơn giản
import datetime
import time
import requests
import wikipedia
wikipedia.set_lang('vi')
from CA_Speak import play
from CA_Hear import get_text
from CA_Hear import hear
from geopy.distance import geodesic
from urllib.parse import urlencode

# tạo một danh sách các tham số đầu vào
PID_mode1 = [13, 12, 4, 5, 15, 70, 11, 31, 17]
data = cmd.Mode_1(PID_mode1)
#tạo danh sách các giá trị main nhận về từ OpenWeathermap
list_weather = ['Clear','Clouds','Rain','Drizzle','Thunderstorm','Snow','Mist','Fog','Haze','Smoke']
list_description = ['clear sky','few clouds','scattered clouds','broken clouds','overcast clouds']
#Lấy giá trị từ GPS thông qua cổng usb
ser = serial.Serial('/dev/ttyACM0',9600,timeout = 5)

#Lấy vĩ độ và kinh độ hiện tại
def latitude_longitude():
    while 1:
        while ser.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        line = ser.readline().decode("utf-8") # Read the entire string
        lines = line.split(",")
        if lines[0][2:] == 'RMC':
            #print(lines)
            latitude_str = lines[3]  # Vĩ độ
            longitude_str = lines[5]  # Kinh độ
                
            latitude_degrees = int(latitude_str[:2])  # Độ
            latitude_minutes = float(latitude_str[2:])  # Phút thập phân

            longitude_degrees = int(longitude_str[:3])  # Độ
            longitude_minutes = float(longitude_str[3:])  # Phút thập phân
                
            latitude = latitude_degrees + latitude_minutes / 60.0
            longitude = longitude_degrees + longitude_minutes / 60.0
        
            return latitude,longitude
            break

#Kết nối với OpenStreetMap lấy thông tin địa chỉ
def Location_name():
    temp = latitude_longitude()
    latitude = temp[0]
    longitude = temp[1]
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    data = response.json()

    if "display_name" in data:
        location_name = data["display_name"]
        #print("Tên địa danh:", location_name)
        return location_name
    else:
        #print("Không tìm thấy thông tin địa danh")
        return "Không tìm thấy thông tin địa danh"

#Trả về mô tả về thời tiết
def description_weather(wthr):
    if (wthr[0]['main'] == list_weather[0]):
        if (wthr[0]["description"] == list_description[0]):
            return 'Hôm nay trời rất đẹp, quang đãng và không mây'
        else:
            return 'Trời quang đãng, không mây'
    elif (wthr[0]['main'] == list_weather[1]):
        if (wthr[0]["description"] == list_description[1]):
            return 'Thời tiết khá ổn định, một vài đám mây nhưng không ảnh hưởng nhiều'
        elif (wthr[0]["description"] == list_description[2]):
            return 'Thời tiết có khả năng mưa rải rác, hãy chú ý quan sát khi tham gia giao thông khi trời có mưa'
        elif (wthr[0]["description"] == list_description[3]):
            return 'Có một số mây tan rã trên bầu trời, tạo nên một hiệu ứng hài hòa giữa ánh sáng và bóng mây'
        else:
            return 'Thời tiết hôm nay có đám mây đen đặc phủ kín bầu trời, tạo nên một cảm giác âm u.'
    elif (wthr[0]['main'] == list_weather[2]):
        if ('light' in wthr[0]["description"]):
            return 'Tại đây hiện đang có mưa nhỏ, không ảnh hưởng nhiều nhưng hãy chú ý khi di chuyển'
        elif('heavy' in wthr[0]["description"]):
            return 'Tại đây đang có mưa lớn, cẩn thận khi di chuyển tại khu vực này'
        else:
            return 'Tại đây có mưa nhưng không lớn, xin hãy chú ý an toàn khi di chuyển'
    elif (wthr[0]['main'] == list_weather[3]):
        return 'Hiện đang có mưa phùn, hay mang theo ô khi ra ngoài'
    elif (wthr[0]['main'] == list_weather[4]):
        return 'Đang có bão sấm chớp xảy ra tại đây, hay di chuyển đến nơi an toàn hoặc nhanh chóng về nhà'
    elif (wthr[0]['main'] == list_weather[5]):
        if ('light' in wthr[0]["description"]):
            return 'Tại đây hiện đang có tuyết rơi vừa, không ảnh hưởng nhiều nhưng hãy chú ý khi di chuyển'
        elif('heavy' in wthr[0]["description"]):
            return 'Tại đây đang có tuyết rơi dày đặc, cẩn thận khi di chuyển tại khu vực này'
        else:
            return 'Tại đây có tuyết rơi, xin hãy chú ý an toàn khi di chuyển'
    elif (wthr[0]['main'] == list_weather[6]):
        return 'Đang có sương mù, hãy cẩn thận khi tham gia giao thông tại đây'
    elif (wthr[0]['main'] == list_weather[7]):
        return ' Sương mù đang dày đặc, hay di chuyển chậm và bật đèn pha khi di chuyển tại đây'
    elif (wthr[0]['main'] == list_weather[8]):
        return 'Đang có sương mù mờ xuất hiện tại đây, hãy di chuyển cẩn thận khi đi vào khu vực này'
    elif (wthr[0]['main'] == list_weather[9]):
        return 'Mức độ khói bụi tại đây lớn, hay chuẩn bị kỹ trước khi di chuyển đến để bảo vệ sức khoẻ và an toàn khi tham gia giao thông '

#Trả về toạ độ của 1 địa điểm
def geocode(location):
    from geopy.geocoders import Nominatim
    # Sử dụng geolocator để tìm kiếm tọa độ của địa điểm
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location)
    # Trả về tọa độ của địa điểm
    return (location.latitude, location.longitude)

#Tạo url dẫn đường từ 2 địa điểm
def create_directions_url(origin, destination):
    base_url = "https://www.google.com/maps/dir/?"
    query_params = {
        "api": "1",
        "origin": origin,
        "destination": destination
    }
    directions_url = base_url + urlencode(query_params)
    return directions_url

#Chào hỏi cơ bản
def greeting():
    day_time = int(time.strftime('%H'))
    if day_time < 12:
        return "Chào buổi sáng. Chúc một ngày mới tốt lành"
    elif 12 <= day_time < 18:
        return "Chào buổi chiều. Chiều nay bạn định làm gì"
    else:
        return "Chào buổi tối, bạn đã ăn tối chưa"

def Route_TwoLocation():
    text1= hear("xuất phát từ")
    text2= hear("nơi đến")
    url_web= create_directions_url(text1,text2)
    play("Đây là kết quả chỉ đường từ {} đến {}".format(text1,text2))
    webbrowser.open(url_web)
def Route_ToLocation():
    text1= Location_name()
    text2= hear("đến")
    url_web= create_directions_url(text1,text2)
    play("Đây là kết quả chỉ đường từ {one} đến {two}".format(one=text1,two=text2))
    webbrowser.open(url_web)
def Routes():
    text = hear("Bạn muốn bắt đầu từ đây hay nơi khác")
    if ("đây" in text) and ("từ" in text):
        Route_ToLocation()
    elif ("khác" in text):
        Route_TwoLocation()
    else:
        play("Xin hãy thực hiện lại yêu cầu")

class GUI():
    def __init__(self, master):
        # Khởi tạo Khung giao diện
        self.master = master
        self.asis_x = (self.master.winfo_screenwidth() / 3.2 - 400)
        self.asis_y = (self.master.winfo_screenheight() / 1.9 - 350)
        self.Size_ui = f"+{int(self.asis_x)}+{int(self.asis_y)}"
        self.master.geometry(self.Size_ui)
        self.master.resizable(width=2000, height=2000)

        self.master.attributes('-fullscreen', True)
        #self.master.attributes("-zoomed", True)  # Tối đa hóa cửa sổ
        self.master.config(bg=color.background)
        self.master.title(text.title)
        #==============================================================================================
        self.Name_Project = Frame(self.master,bg=color.frame)
        self.Name_Project.grid(sticky="nsew")
        self.NP = Label(self.Name_Project,text=text.title,font= ("Arial",32,"bold"),fg="red",bg=color.frame)
        self.NP.config(height=1, anchor=W, width=40, padx=5)
        self.NP.grid(sticky="nsew", pady=5, padx=5)
        self.Name_Project.pack(side=TOP,fill=X, padx=15,pady=15)
        # =============================================================================================
        # Frame trợ lí ảo
        self.car_info = LabelFrame(self.master, padx=100, pady=55,relief="sunken")

        #text yêu cầu:
        self.cb0 = tk.Label(self.car_info, text="Yêu cầu của bạn: ", font=("Arial", 18), borderwidth=1)
        self.cb0.config(height=1, anchor=W, width=20, padx=5)
        self.cb0.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        #Text nói
        self.cb1 = Label(self.car_info, text=" ", font=("Arial", 18), borderwidth=1)
        self.cb1.config(height=1, anchor=W, width=50, padx=5)
        self.cb1.grid(row=0, column=1, sticky=NW, pady=5, padx=5)
        #rỗng
        self.cb2 = Label(self.car_info, text="     ", font=("Arial", 18), borderwidth=1)
        self.cb2.config(height=1, anchor=W, width=10, padx=5)
        self.cb2.grid(row=0, column=2, sticky=NW, pady=5, padx=5)
        #Giá trị
        self.answer_title = Label(self.car_info, text="Kết quả: ", font=("Arial", 18), borderwidth=1)
        self.answer_title.config(height=1, anchor=W, width=20, padx=5)
        self.answer_title.grid(row=1, column=0, sticky=W, pady=5, padx=5)
        #Hiển thị giá trị
        self.answer = Label(self.car_info, text="    ", font=("Arial", 54, "bold"), borderwidth=1)
        self.answer.config(height=1, anchor=W, width=17, padx=5)
        self.answer.grid(row=1, column=1, sticky="nsew", pady=25, padx=5)
        #Rỗng
        self.answer_R = Label(self.car_info, text="   ", font=("Arial", 18, "bold"), borderwidth=1)
        self.answer_R.config(height=1, anchor=W, width=15, padx=5)
        self.answer_R.grid(row=1, column=2, sticky="nsew", pady=25, padx=15)
        #Nút nhấn trợ lí
        self.btn_quest = Button(self.car_info, text="Trợ lý", font=("Arial", 13,"bold"), command=self.process)
        #self.btn_quest = Button(self.car_info, image=self.button_photo, command=self.process)
        self.btn_quest.config(width=15, height=2)
        self.btn_quest.grid(row=2, column=1, pady=20)
        #Tạo bảng
        self.car_info.columnconfigure(0, weight=1)
        self.car_info.columnconfigure(1, weight=1)
        self.car_info.columnconfigure(2, weight=1)
        self.car_info.rowconfigure(0, weight=1)
        self.car_info.rowconfigure(1, weight=1)
        self.car_info.rowconfigure(2, weight=1)
        self.car_info.pack(side=TOP,fill=X, padx=15, pady=15)
        # ==============================================================================================
        self.author_frame = LabelFrame(self.master, text="", font=("Arial", 15, "bold"), bg=color.frame,
                                       pady=5)
        self.authur0 = Label(self.author_frame, text="Tbt", font=("Arial", 15), bg=color.frame)
        self.authur0.grid(row=1, column=0, pady=15)

        self.author_frame.grid_columnconfigure(0, weight=1)
        self.author_frame.grid_columnconfigure(1, weight=1)
        self.author_frame.grid_columnconfigure(2, weight=1)
        self.author_frame.rowconfigure(0, weight=1)
        self.author_frame.rowconfigure(0, weight=1)
        self.author_frame.pack(side=TOP, fill=X, padx=15, pady=15)
    #mở cửa số in tất cả thông tin nhận từ obd II
    def open_new_window(self):
        new_window = tk.Toplevel()
        new_window.title("Thông tin tất cả cảm biến")
        asis_x = (new_window.winfo_screenwidth() / 2 - 400)
        asis_y = (new_window.winfo_screenheight() / 2 - 350)
        Size_ui = f"+{int(asis_x)}+{int(asis_y)}"
        new_window.geometry(Size_ui)
        #Frame hiển thị các giá trị
        frame = LabelFrame(new_window, text="Giá trị cảm biến thu được", padx=10, pady=5)
        #Vận tốc
        c0 = Label(frame, text=f"{text.c0} {text.null}", borderwidth=5, relief="sunken")
        c0.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c0.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        #Tốc độ vòng tua
        c1 = Label(frame, text=f"{text.c1} {text.null}", borderwidth=5, relief="sunken")
        c1.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c1.grid(row=0, column=1, sticky=W, pady=5, padx=5)
        #Tải động cơ/ Công suất
        c2 = Label(frame, text=f"{text.c2} {text.null}", borderwidth=5, relief="sunken")
        c2.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c2.grid(row=0, column=2, sticky=W, pady=5, padx=5)
        #Nhiệt độ nước làm mát
        c3 = Label(frame, text=f"{text.c3} {text.null}", borderwidth=5, relief="sunken")
        c3.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c3.grid(row=1, column=0, sticky=W, pady=5, padx=5)
        #Nhiệt độ khí nạp
        c4 = Label(frame, text=f"{text.c4} {text.null}", borderwidth=5, relief="sunken")
        c4.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c4.grid(row=1, column=1, sticky=W, pady=5, padx=5)
        #Nhiệt độ môi trường
        c5 = Label(frame, text=f"{text.c5} {text.null}", borderwidth=5, relief="sunken")
        c5.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c5.grid(row=1, column=2, sticky=W, pady=5, padx=5)
        #Áp suất khí nạp
        c6 = Label(frame, text=f"{text.c6} {text.null}", borderwidth=5, relief="sunken")
        c6.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c6.grid(row=2, column=0, sticky=W, pady=5, padx=5)
        #Thời gian chạy
        c7 = Label(frame, text=f"{text.c7} {text.null}", borderwidth=5, relief="sunken")
        c7.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c7.grid(row=2, column=1, sticky=W, pady=5, padx=5)
        #Vị trí bướm ga
        c8 = Label(frame, text=f"{text.c8} {text.null}", borderwidth=5, relief="sunken")
        c8.config(height=1, anchor=W, bg=color.connect_fail, fg=color.font, width=size.cbdata_width, padx=5)
        c8.grid(row=2, column=2, sticky=W, pady=5, padx=5)
        #Tạo bảng hiển thị
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        #Khời tạo frame
        frame.pack(side=TOP, fill=X, padx=15)
        #==================================================================
        #Gán các giá trị lên label
        c0.config(text=f"{text.c0} {string_handling(data[0], 0)}")
        c1.config(text=f"{text.c1} {string_handling(data[1], 1)}")
        c2.config(text=f"{text.c2} {string_handling(data[2], 2)}")
        c3.config(text=f"{text.c3} {string_handling(data[3], 3)}")
        c4.config(text=f"{text.c4} {string_handling(data[4], 4)}")
        c5.config(text=f"{text.c5} {string_handling(data[5], 5)}")
        c6.config(text=f"{text.c6} {string_handling(data[6], 6)}")
        c7.config(text=f"{text.c7} {string_handling(data[7], 7)}")
        c8.config(text=f"{text.c8} {string_handling(data[8], 8)}")
    #Trả về thông tin thời tiết và in nhiệt độ độ ẩm lên giao diện tkinter
    def weather(self):
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        location = get_text()
        #location = find_location_name(text)
        print()
        if not location:
            pass
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid="+api_key + "&q=" + location + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_humidity = city_res["humidity"]
            wthr = data["weather"]
            descriptionW = description_weather(wthr)
            content = """
                Dự báo thời tiết tại {location}
                Nhiệt độ trung bình là {temp} độ C
                Độ ẩm là {humidity}%
                {description}.""".format(location=location,temp=current_temperature,humidity=current_humidity,description= descriptionW)
            self.cb1.config(text="Dự báo thời tiết tại {}".format(location.title()))
            self.answer.config(text="[{} độ C: {} %]".format(current_temperature, current_humidity))
            play(content)
            #time.sleep(5)
        else:
            self.answer.config(text="  ")
            self.cb1.config(text="Không tìm thấy {} ".format(location.title()))
            play("Không tìm thấy địa chỉ")
    #Trả về giá trị giờ và in giờ phút giây lên giao diện
    def hour(self):
        currentDateAndTime = datetime.datetime.now()
        text = "Giờ là " + str(
            currentDateAndTime.hour) + " giờ, " + str(currentDateAndTime.minute) + " phút, " + str(
            currentDateAndTime.second) + " giây."
        self.answer.config(text="[ "+str(currentDateAndTime.hour)+": "+str(currentDateAndTime.minute)+": "+str(
            currentDateAndTime.second)+" ]")
        play(text)
    #Trả về giá trị ngày và in ngày tháng năm lên giao diện
    def date(self):
        xtemp = datetime.datetime.now()
        text = "Hôm nay là " + "Ngày " + str(
            xtemp.day) + " tháng " + str(xtemp.month) + " năm " + str(xtemp.year)
        self.answer.config(text= str(xtemp.day)+"/ "+str(xtemp.month)+" /"+str(xtemp.year))
        play(text)
    def process(self):
        text = hear("bạn cần biết vấn đề nào")
        self.cb1.config(text=text)
        if ("có thể làm gì" in text) or ("help" in text):
            play("""tôi có thể: hiển thị tốc độ xe, 
                tốc độ vòng tua, 
                tải động cơ, 
                nhiệt độ nước làm mát, 
                nhiệt độ khí nạp, 
                nhiệt độ môi trường, 
                áp suất khí nạp, 
                thời gian chạy động cơ, 
                vị trí bướm ga.""")
            play("bạn cần biết vấn đề nào")
            self.master.after(500,self.process())
        elif ("giúp" in text):
            play(
                "Tất nhiên, tôi sẽ cố gắng giúp đỡ bạn. Bạn cần giúp đỡ về vấn đề gì? Hãy đặt câu hỏi cụ thể để tôi có thể trợ giúp bạn tốt nhất có thể.")
            #Gọi lại hàm Process sau 0.5s
            self.master.after(500,self.process())
        elif ("cảm ơn" in text) or ("thanks" in text) or ("cám ơn" in text):
            play("Không có gì, nếu bạn cần hỗ trợ thêm, hãy đặt yêu cầu với tôi.")
        elif ("hẹn gặp lại" in text) or ("tạm biệt" in text) or ("tắt" in text) or ("off" in text) or (
                "kết thúc" in text):
            play("Hẹn gặp lại bạn")
            self.master.quit()
        elif ("giờ" in text) or ("thời gian" in text):
            if ("chạy" in text) or ("xe" in text):
                play("thời gian xe chạy là {}".format(string_handling(data[7], 7)))
                self.answer.config(text=string_handling(data[7], 7))
            else:
                self.hour()
        elif ("ngày" in text) or ("tháng" in text) or ("năm" in text):
            self.date()
        elif ("chào" in text) or ("hello" in text):
            play(greeting())
        elif ("thời tiết" in text) or ("dự báo" in text):
            self.weather()
        elif ("biết" in text):
            if ("tốc độ" in text) or ("vận tốc" in text):
                play("vận tốc xe chạy là {}".format(string_handling(data[0], 0)))
                self.answer.config(text=string_handling(data[0], 0))
            elif ("vòng" in text) or ("rpm" in text) or ("tua" in text):
                play("tốc độ vòng tua của xe là {}".format(string_handling(data[1], 1)))
                self.answer.config(text=string_handling(data[1], 1))
            elif ("tải" in text) or ("công suất" in text):
                play("Công suất là {}".format(string_handling(data[2], 2)))
                self.answer.config(text=string_handling(data[2], 2))
            elif "nhiệt độ" in text:
                if ("nước" in text) or ("làm mát" in text):
                    play("nhiệt độ nước làm mát của xe là {}".format(string_handling(data[3], 3)))
                    self.answer.config(text=string_handling(data[3], 3))
                elif ("khí" in text) or ("nạp" in text):
                    play("nhiệt độ khí nạp của xe là {}".format(string_handling(data[4], 4)))
                    self.answer.config(text=string_handling(data[4], 4))
                elif ("môi trường" in text) or ("xe" in text):
                    play("nhiệt độ môi trường trên xe là {}".format(string_handling(data[5], 5)))
                    self.answer.config(text=string_handling(data[5], 5))
            elif "suất" in text:
                if ("ống" in text) or ("nạp" in text):
                    play("áp suất đường ống nạp là {}".format(string_handling(data[6], 6)))
                    self.answer.config(text=string_handling(data[6], 6))
            elif "vị trí" in text:
                if "bướm ga" in text:
                    play("Vị trí bướm ga là {}".format(string_handling(data[8], 8)))
                    self.answer.config(text=string_handling(data[8], 8))
        elif ("tất" in text) and ("cả" in text):
            self.open_new_window()
        elif ("chỉ" in text) and ("đường" in text):
            Routes()
        elif ("ở" in text) and ("đâu" in text):
            play(Location_name())
        else:
            play("tôi chưa hiểu ý bạn, xin hãy lặp lại")
            self.master.after(500,self.process())

def Car_handle():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

def main():
    Car_handle()

        
if __name__ == '__main__':
    main()
