#chuyển đổi kiểu giá trị
def string_handling(string_input, num):
    split_unit = [' kph',' revolutions_per_minute',' percent', ' degC', ' degC',' degC',' kilopascal',' second',' percent']
    unit_convert = ['Km/h','RPM','%', '°C','°C', '°C','kPa','s', '%']
    num_split = string_input.split(split_unit[num])
    fl = float(num_split[0])
    num_round = round(fl,2)
    data = f"{num_round} {unit_convert[num]}"
    return data


class color():
    background = '#59F09B'
    frame = '#168A7C'
    connect_fail = '#bf381d'
    connect_success = '#0A8A4E'
    font = 'white'


class size():
    Frame_width = 770
    cbdata_width = 30
    tree_01 = 220
    tree_02 = 540
    data_show = 17
    btn = 14
    result = 30


class text():
    title = 'TRỢ LÝ ẢO XE HƠI'
    box1_title = 'Thông tin'
    box2_title = 'Trợ lí ảo'
    box3_title = 'Chuẩn đoán lỗi'
    box4_title = ''
    box5_title = 'Tên sinh viên thực hiện đề tài'
    nameCB = " Yêu cầu của bạn: "
    c0 = 'Tốc độ xe:'
    c1 = 'Vòng tua máy:'
    c2 = 'Tải động cơ:'
    c3 = 'Nhiệt độ nước làm mát:'
    c4 = 'Nhiệt độ khí nạp:'
    c5 = 'Nhiệt độ môi trường:'
    c6 = 'Áp suất đường ống nạp:'
    c7 = 'Thời gian chạy động cơ:'
    c8 = 'Vị trí bướm ga:'
    null = 'Null'

if __name__ == '__main__':

    print(string_handling(str("0.0 revolutions_per_minute"), 1))
