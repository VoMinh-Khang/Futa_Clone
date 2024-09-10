import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps

from apps.controllers import user_controller, buses_controller, admin_controller
from datetime import datetime, timedelta, date

import random
import string

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def convert_date_format(input_date):
    # Chuyển đổi định dạng từ "15-04-2024" thành "15/04/2024"
    formatted_date = datetime.strptime(input_date, "%d-%m-%Y").strftime("%d/%m/%Y")
    return formatted_date

@app.route('/')
def home():
    return render_template('user/pages/home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    controller = user_controller() 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = controller.check_login(email, password) 
        info_user = controller.get_user_by_email_password(email, password)
        if user:
            # Nếu người dùng tồn tại, đăng nhập thành công
            session['logged_in'] = True
            session['phone'] = info_user.get('SDT')
            session['username'] = info_user.get('HoVaTen')

            return redirect(url_for('home'))
        else:
            error_message = "Thông tin không chính xác. Vui lòng thử lại."
            return render_template('user/auth/login.html', error_message=error_message)
    else:
        return render_template('user/auth/login.html')
    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('phone', None)
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('user/auth/signup.html')

@app.route('/profile')
def profile():
    controller = user_controller()
    phone = session.get('phone')
    info_user = controller.get_user_by_phone(phone)
    dia_chi_obj = info_user.get('DiaChi', {})
    dia_chi_str = ', '.join([value for value in dia_chi_obj.values()])

    # Thêm chuỗi Địa chỉ vào thông tin người dùng
    info_user['DiaChiStr'] = dia_chi_str
    return render_template('user/pages/profile.html', info_user = info_user)

def format_currency(amount):
        formatted_amount = '{:,.0f}'.format(amount)
        return formatted_amount.replace(",", ".")
    

@app.route('/futapay')
def futapay():
    phone = session.get('phone')
    controller = user_controller()
    busesController = buses_controller()
    stk = controller.get_stk_by_phone(phone)
    all_donve = busesController.get_donve_by_stk(stk)
    balance = controller.get_balance_by_phone(phone)
    formatted_balance = format_currency(balance)
    
    formatted_donve_list = []
    for donve in all_donve:
        ngay_tao = donve['NgayTao'].strftime('%d-%m-%Y')
        gio_tao_temp = donve['GioTao']
        gio_tao_str = f"{gio_tao_temp.hour:02}:{gio_tao_temp.minute:02}:{gio_tao_temp.second:02}"
        formatted_donve = {
            'Madon': donve['Madon'],
            'TongGia': donve['TongGia'],
            'NgayTao': ngay_tao,
            'GioTao': gio_tao_str,
            'MaChuyen': donve['MaChuyen']
        }
        formatted_donve_list.append(formatted_donve)

    return render_template('user/pages/futapay.html', balance=formatted_balance, all_donve=formatted_donve_list)

@app.route('/history')
def history():
    phone = session.get('phone')
    controller = user_controller()
    busesController = buses_controller()

    stk = controller.get_stk_by_phone(phone) 
    all_donve = busesController.get_donve_by_stk(stk)
    
    formatted_donve_list = []
    for donve in all_donve:
        ngay_tao = donve['NgayTao'].strftime('%d-%m-%Y')
        gio_tao_temp = donve['GioTao']
        gio_tao_str = f"{gio_tao_temp.hour:02}:{gio_tao_temp.minute:02}:{gio_tao_temp.second:02}"
        formatted_donve = {
            'Madon': donve['Madon'],
            'TongGia': donve['TongGia'],
            'NgayTao': ngay_tao,
            'GioTao': gio_tao_str,
            'MaChuyen': donve['MaChuyen']
        }
        formatted_donve_list.append(formatted_donve)
    return render_template('user/pages/history.html', all_donve=formatted_donve_list)

@app.route('/promotion')
def promotion():
    return render_template('user/pages/promotion.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        controller = buses_controller()
        departure = controller.get_departure()
        destination = controller.get_destination()
        
        departure_search = request.form.get('departure')
        destination_search = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        num_tickets = request.form.get('num_tickets')
        
        if departure_date:
            formatted_departure_date = convert_date_format(departure_date)

        if not all([departure_search, destination_search, departure_date, num_tickets]):
            result = controller.get_all_buses()
            return render_template('user/pages/schedule.html', result=result, departure=departure, destination=destination)
        else:
            available_routes = controller.get_available_routes(departure_search, destination_search, formatted_departure_date, num_tickets)
        
        return render_template('user/pages/schedule.html', result=available_routes, departure=departure, destination=destination)
    else:
        controller = buses_controller()
        departure = controller.get_departure()
        destination = controller.get_destination()
        result = controller.get_all_buses()
        return render_template('user/pages/schedule.html', result=result, departure=departure, destination=destination)

@app.route('/trip')
def trip():
    ID_buses = request.args.get('ten_tuyen_xe')
    controller = buses_controller()
    distance = controller.get_distance_by_name(ID_buses)
    travel_time = controller.get_travel_time(ID_buses)
    list_buses = controller.set_ID_buses(ID_buses)
    return render_template('user/pages/trip.html', ID_buses = ID_buses, list_buses = list_buses, distance = distance, travel_time =travel_time)

@app.route('/filter')
def filter_buses():
    controller = buses_controller()
    selected_time = request.args.get('time')
    name = request.args.get('name')
    selected_type = request.args.get('type')
    start_time = end_time = None 
    
    if selected_time == 'sangSom':
        start_time = '00:00'
        end_time = '06:00'
        
    elif selected_time == 'buoiSang':
        start_time = '06:00'
        end_time = '12:00'
        
    elif selected_time == 'buoiChieu':
        start_time = '12:00'
        end_time = '18:00'

    elif selected_time == 'sangToi':
        start_time = '18:00'
        end_time = '24:00'
    else:
        start_time = '00:00'
        end_time = '24:00'
        
    if selected_type != '0':
        # print("selected_type", selected_type)
        # print("start_time", start_time)
        # print("end_time", end_time)
        # print("name", name)
        list_buses = controller.get_all_list_buses(start_time, end_time, name, selected_type)    
    else:
        # print("start_time", start_time)
        # print("end_time", end_time)
        # print("name", name)
        list_buses = controller.get_all_list_buses(start_time, end_time, name)

        # print("list_buses", list_buses)
    filtered_buses = list_buses
    return jsonify(filtered_buses=filtered_buses)


@app.route('/booking')
def booking():
    ma_chuyen = request.args.get('ma_chuyen')
    phone = session.get('phone')
    
    controller = buses_controller()
    usercontroller = user_controller()
    
    bus_info = controller.get_bus_by_id(ma_chuyen)
    seats = controller.get_seat_id(ma_chuyen)
    seat_numbers = [item for sublist in seats for item in sublist]
    price = controller.get_price(ma_chuyen)
    vehicle_type = controller.get_vehicle_type(ma_chuyen)
    balance = usercontroller.get_balance_by_phone(phone)
    formatted_balance = format_currency(balance)
    diadiemdi = controller.get_diadiemdi(ma_chuyen)
    diadiemden = controller.get_diadiemden(ma_chuyen)

    ten_chuyen_xe = bus_info['TenChuyenXe']
    gio_khoi_hanh = bus_info['GioKhoiHanh']
    gio_den = bus_info['GioDen']
    loai_xe = bus_info['LoaiXe']
    so_luong_ghe_trong = bus_info['SoLuongGheTrong']
    dia_diem_di = bus_info['DiaDiemDi']
    dia_diem_den = bus_info['DiaDiemDen']
    gia = bus_info['Gia']
    ngay_di = bus_info['NgayDi']
    
    ngay_di = datetime.strptime(ngay_di, '%d/%m/%Y')
    ngay_di_formatted = ngay_di.strftime('%d/%m')
    
    gio_khoi_hanh_t = datetime.strptime(gio_khoi_hanh, '%H:%M')
    gio_den_t = datetime.strptime(gio_den, '%H:%M')
    
    thoi_gian_chuyen_xe = gio_den_t - gio_khoi_hanh_t
    
    if thoi_gian_chuyen_xe.days < 0:
        ngay_di += timedelta(days=1)
        
    ngay_den = ngay_di.strftime('%d/%m')
    
    thoi_gian_chuyen_xe_formatted = str(thoi_gian_chuyen_xe // timedelta(hours=1)) + ':' + str((thoi_gian_chuyen_xe % timedelta(hours=1)).seconds // 60).zfill(2)

    return render_template('user/pages/booking.html', gio_khoi_hanh=gio_khoi_hanh, gio_den=gio_den, 
                           loai_xe=loai_xe, so_luong_ghe_trong=so_luong_ghe_trong, 
                           dia_diem_di=dia_diem_di, dia_diem_den=dia_diem_den,
                           gia=gia, ngay_di=ngay_di_formatted, 
                           thoi_gian_chuyen_xe = thoi_gian_chuyen_xe_formatted, ngay_den=ngay_den,
                           ten_chuyen_xe=ten_chuyen_xe, seat_numbers=seat_numbers, price=price, 
                           vehicle_type=vehicle_type, formatted_balance = formatted_balance,
                           diadiemdi=diadiemdi, diadiemden=diadiemden,
                           ma_chuyen=ma_chuyen)
    
@app.route('/pay')
def pay():
    ma_chuyen = request.args.get('ma_chuyen')
    phone = session.get('phone')
    controller = buses_controller()
    bus_info = controller.get_bus_by_id(ma_chuyen)
    
    ngay_di = bus_info['NgayDi']
    gio_khoi_hanh = bus_info['GioKhoiHanh']
    
    tenchuyenxe = controller.get_ten_chuyen_xe(ma_chuyen)
    diadiemdi = controller.get_diadiemdi(ma_chuyen)
    diadiemden = controller.get_diadiemden(ma_chuyen)
    
    selected_seat = request.args.get('selected_seat')
    selected_seat_list = selected_seat.split(', ')
    number_of_seats = len(selected_seat_list)
    total_price = request.args.get('total_price')
    total_price_int = int(total_price.replace('.', '').replace('đ', ''))
    customer_name = request.args.get('customer_name')
    customer_phone = request.args.get('customer_phone')
    customer_email = request.args.get('customer_email')
    # Bây giờ bạn có thể truyền các giá trị này tới template pay.html
    return render_template('user/pages/pay.html',ma_chuyen=ma_chuyen, selected_seat_list=selected_seat_list, 
                           total_price=total_price, customer_name=customer_name, 
                           customer_phone=customer_phone, customer_email=customer_email,
                           selectedlength=number_of_seats, tenchuyenxe=tenchuyenxe,
                           diadiemdi=diadiemdi, diadiemden=diadiemden,
                           ngay_di=ngay_di, gio_khoi_hanh=gio_khoi_hanh)

def generate_random_madon():
    # Tạo mã đơn vé ngẫu nhiên gồm 'DV' và 8 ký tự số ngẫu nhiên
    random_digits = ''.join(random.choices(string.digits, k=8))
    return 'DV' + random_digits

@app.route('/confirm_payment')
def confirm_payment():
    phone = session.get('phone')
    madon = generate_random_madon()
    ma_chuyen = request.args.get('ma_chuyen')
    customer_name = request.args.get('customer_name')
    customer_email = request.args.get('customer_email')
    customer_phone = request.args.get('customer_phone')
    tenchuyenxe = request.args.get('tenchuyenxe')
    gio_khoi_hanh = request.args.get('gio_khoi_hanh')
    ngay_di = request.args.get('ngay_di')
    selected_seat_list = request.args.get('selected_seat_list').split(', ')
    diadiemdi = request.args.get('diadiemdi')
    total_price = request.args.get('total_price')
    number_of_seats = len(selected_seat_list)
    ticket_price = float(total_price.replace(".", "").replace("đ", "")) / number_of_seats
    formatted_ticket_price = "{:,.0f}".format(ticket_price).replace(",", ".") + "đ"
    controller = buses_controller()
    usercontroller = user_controller()
    stk = usercontroller.get_stk_by_phone(phone)

    balance_by_phone = usercontroller.get_balance_by_phone(phone)
    total_price_fomat = int(total_price.replace(".", "").replace("đ", ""))   
    sum_price = int(balance_by_phone - total_price_fomat)

    update_balance = usercontroller.update_balance(phone, sum_price)
    
    if update_balance is not None:
       print("Thành công")
    else:
        print("Thất bại")
    
    result = controller.insert_donve(madon, customer_phone, stk, ma_chuyen, selected_seat_list, total_price_fomat)

    result_update = controller.update_soluongghetrong_ma_chuyen(ma_chuyen)


    return render_template('user/pages/confirm_payment.html', 
                           customer_name=customer_name,
                           customer_email=customer_email,
                           customer_phone=customer_phone,
                           tenchuyenxe=tenchuyenxe,
                           gio_khoi_hanh=gio_khoi_hanh,
                           ngay_di=ngay_di,
                           selected_seat_list=selected_seat_list,
                           diadiemdi=diadiemdi,
                           total_price=total_price, madon=madon,
                           formatted_ticket_price=formatted_ticket_price)


@app.route('/contact')
def contact():
    return render_template('user/pages/contact.html')

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            return redirect(url_for('login_admin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_login_required
def home_admin():
    controller = user_controller()
    users = controller.get_all_users()
    return render_template('admin/pages/home.html', users=users)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':

        phone = request.form['phone']
        password = request.form['password']

        controller = admin_controller()
        admin = controller.check_login(phone, password)
        info_admin = controller.get_admin_by_phone_password(phone, password)
        if admin:
            session['admin_logged_in'] = True
            session['phone'] = info_admin.get('phone')
            session['fullName'] = info_admin.get('fullName')
            return redirect(url_for('home_admin'))
        else:
            error_message = "Thông tin không chính xác. Vui lòng thử lại."
            return render_template('admin/pages/login.html', error_message=error_message)
    else:
        return render_template('admin/pages/login.html')
    
@app.route('/logout_admin')
def logout_admin():
    session.pop('admin_logged_in', None)
    session.pop('phone', None)
    session.pop('fullName', None)
    # Chuyển hướng về trang đăng nhập admin
    return redirect(url_for('login_admin'))
     
@app.route('/update_data_user', methods=['GET'])
def update_data_user():
    phone = request.args.get('phone')
    controller = user_controller()
    info = controller.get_user_by_phone2(phone)
    return jsonify(info)

@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    sdt = data['sdt']
    email = data['email']
    username = data['username']
    ho_va_ten = data['ho_va_ten']
    password = data['password']
    ngay_sinh = data['ngay_sinh']
    balance = int(data['balance'])
    
    controller = user_controller()
    result = controller.update_user(sdt, email, username, ho_va_ten, password, ngay_sinh, balance)
    print(result)
    
    if result.modified_count > 0:  # Kiểm tra xem có dữ liệu nào được cập nhật không
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Không thể cập nhật dữ liệu'})
    
@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.json
    stk = data['stk']
    phone = data['phone']
    email = data['email']
    username = data['username']
    ho_va_ten = data['ho_va_ten']
    password = data['password']

    controller = user_controller()  # Initialize user controller
    result = controller.insert_data_user(stk, phone, email, username, ho_va_ten, password)  # Call method to insert user

    if result.inserted_id:  # Check if user was successfully inserted
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Không thể thêm dữ liệu người dùng'})

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    sdt = data['sdt']

    # Gọi phương thức xóa người dùng từ controller
    controller = user_controller()
    result = controller.delete_data_user(sdt)

    if result.deleted_count > 0:  # Kiểm tra xem có người dùng nào đã bị xóa không
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Không thể xóa người dùng'})
    

@app.route('/admin_ticket')
def admin_ticket():
    controller = buses_controller()
    donve = controller.get_all_donve()
    return render_template('admin/pages/ticket.html', donve=donve)

@app.route('/update_data_donve', methods=['POST'])
def update_data_donve():
    madon = request.args.get('madon')
    controller = buses_controller()
    info = controller.get_donve_by_madon(madon)
    
    # Convert Neo4j Time object to string in ISO format
    formatted_info = []
    for node in info:
        node_dict = dict(node)
        # Convert Neo4j Time objects to ISO-formatted strings
        node_dict['GioTao'] = node_dict['GioTao'].iso_format()
        node_dict['NgayTao'] = node_dict['NgayTao'].iso_format()
        formatted_info.append(node_dict)
    
    # Return JSON response
    return jsonify(formatted_info)

@app.route('/update_donve', methods=['POST'])
def update_donve():
    controller = buses_controller()
    
    data = request.json
    madon = data['madon']
    sdt = data['sdt']
    machuyen = data['machuyen']
    ghe = data['ghe']
    check_ghe = controller.check_existing_seats(ghe, machuyen, madon)

    if check_ghe == 0:
        result = controller.update_donve_by_madon(sdt, madon, machuyen, ghe)
        return jsonify({'success': True})
    else:
        return jsonify({'ghe': check_ghe})
    
@app.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.json
    madon = generate_random_madon()
    stk = data.get('stk')
    phone = data.get('phone')
    machuyen = data.get('machuyen')
    ghe = data.get('ghe')

    # Thực hiện thêm dữ liệu vào cơ sở dữ liệu ở đây
    controller = buses_controller()
    check = controller.check_existing_seats_in_route(machuyen, ghe)
    if check == False:
        tong_gia = controller.calculate_total_price(machuyen, ghe)
        result = controller.insert_donve(madon, phone, stk, machuyen, ghe, tong_gia)
        return jsonify({'success': True})

    else:
        return jsonify({'error': 'Ghế đã tồn tại trong chuyến xe'})

@app.route('/delete_donve', methods=['DELETE'])
def delete_donve():
    data = request.json
    madon = data['madon']

    # Gọi phương thức xóa người dùng từ controller
    controller = buses_controller()
    result = controller.delete_data_donve(madon)

    return jsonify({'success': True})

@app.route('/admin_schedule')
def admin_schedule():
    controller = buses_controller()
    tuyenxe = controller.get_all_tuyenxe()
    return render_template('admin/pages/schedule.html', tuyenxe=tuyenxe)

@app.route('/insert_tuyenxe', methods=['POST'])
def insert_tuyenxe():
    data = request.json
    tenchuyenxe = data.get('tenchuyenxe')
    diadiemdi = data.get('diadiemdi')
    diadiemden = data.get('diadiemden')
    quangduong = data.get('quangduong')
    time = data.get('time')
    controller = buses_controller() 
    result = controller.insert_tuyenxe(tenchuyenxe, diadiemdi, diadiemden, quangduong, time)
    return jsonify({'success': True})

@app.route('/admin_trip')
def admin_trip():
    controller = buses_controller()

    tentuyenxe = controller.get_all_tentuyenxe()
    
    chuyenxe = controller.get_all_chuyenxe()
    return render_template('admin/pages/trip.html', chuyenxe=chuyenxe, tentuyenxe=tentuyenxe)

@app.route('/update_data_chuyenxe', methods=['POST'])
def update_data_chuyenxe():
    machuyen = request.args.get('machuyen')
    controller = buses_controller()
    info = controller.get_chuyenxe_by_machuyen(machuyen)
    
    # Convert Neo4j Time object to string in ISO format
    formatted_info = []
    for node in info:
        node_dict = dict(node)
        formatted_info.append(node_dict)
    
    # Return JSON response
    return jsonify(formatted_info)

@app.route('/update_chuyenxe', methods=['POST'])
def update_chuyenxe():
    controller = buses_controller()

    data = request.json
    machuyen = data['machuyen']
    diadiemdi = data['diadiemdi']
    diadiemden = data['diadiemden']
    giokhoihanh = data['giokhoihanh']
    gioden = data['gioden']
    ngaydi = data['ngaydi']
    gia = data['gia']

    result = controller.update_chuyenxe_by_machuyen(machuyen, diadiemdi, diadiemden, giokhoihanh, gioden, ngaydi, gia)
    print(result)
    
    return jsonify({'success': True})

@app.route('/insert_chuyenxe', methods=['POST'])
def insert_chuyenxe():
    data = request.json

    tenchuyen = data.get('tenchuyen')
    loaixe = data.get('loaixe')
    diadiemdi = data.get('diadiemdi')
    diadiemden = data.get('diadiemden')
    giokhoihanh = data.get('giokhoihanh')
    gioden = data.get('gioden')
    ngaydi = data.get('ngaydi')
    gia = data.get('gia')

    controller = buses_controller() 
    # Chèn dữ liệu vào cơ sở dữ liệu
    result = controller.insert_data_chuyenxe(tenchuyen, loaixe, diadiemdi, diadiemden, giokhoihanh, gioden, ngaydi, gia)
    
    # Trả về phản hồi dưới dạng JSON
    return jsonify({'success': True})

@app.route('/delete_chuyenxe', methods=['DELETE'])
def delete_chuyenxe():
    data = request.json
    machuyen = data['machuyen']

    # Gọi phương thức xóa người dùng từ controller
    controller = buses_controller()
    result = controller.delete_chuyenxe(machuyen)

    return jsonify({'success': True})