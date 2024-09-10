from config.settings import db
from config.settings import run_query
from datetime import datetime

def get_next_chuyenxe_id():
    query = """
        MATCH (c:CHUYENXE)
        RETURN COUNT(c)
        """
    result = run_query(query)
    count = result[0]  
    next_id = count + 1 
    return next_id

def count_selected_seats(selectedSeats):
    count = 0
    for seat in selectedSeats:
        if isinstance(seat, list):
            count += len(seat)
        else:
            count += 1
    return count

def convert_price_to_int(price_str):
    # Xóa dấu chấm (nếu có) và chuyển đổi thành số nguyên
    return int(price_str.replace('.', ''))

class user_controller():
    def check_login(self, email, password):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có email và password như đã nhập
        user = users_collection.find_one({"Email": email, "Password": password})
        return user
    
    def get_all_users(self): # lấy tất cả thông tin của user
        users_collection = db['NGUOIDUNG']
        users = users_collection.find()
        return users
    
    def get_user_by_phone(self, sdt):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có số điện thoại như đã nhập
        user = users_collection.find_one({"SDT": sdt})
        return user
    
    def get_user_by_phone2(self, sdt):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có số điện thoại như đã nhập
        user = users_collection.find_one({"SDT": sdt})

        # Loại bỏ trường _id nếu tồn tại
        if user and '_id' in user:
            del user['_id']
        
        return user
    
    def get_user_by_email_password(self, email, password):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có email và password như đã nhập
        user = users_collection.find_one({"Email": email, "Password": password})
        return user
    
    def get_balance_by_phone(self, phone):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có số điện thoại như đã nhập
        user = users_collection.find_one({"SDT": phone})
        if user:
            return user.get("balance", 0)  # Trả về số dư hoặc mặc định là 0 nếu không tìm thấy
        else:
            return 0  # Trả về 0 nếu không tìm thấy người dùng
        
    def update_balance(self, phone, amount):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có số điện thoại như đã nhập
        user = users_collection.find_one({"SDT": phone})
        if user:
            users_collection.update_one({"SDT": phone}, {"$set": {"balance": amount}})
        else:
            return None
        
    def get_stk_by_phone(self, phone):
        users_collection = db['NGUOIDUNG']
        # Tìm người dùng có số điện thoại như đã nhập và lấy STK
        user = users_collection.find_one({"SDT": phone})
        if user:
            return user.get("STK", None)
        else:
            return None
        
    def update_user(self, sdt, email, username, ho_va_ten, password, ngay_sinh, balance):
        users_collection = db['NGUOIDUNG']
        # Tìm và cập nhật thông tin người dùng có số điện thoại (SDT) như đã nhập
        result = users_collection.update_one(
            {"SDT": sdt},
            {
                "$set": {
                    "Email": email,
                    "Username": username,
                    "HoVaTen": ho_va_ten,
                    "Password": password,
                    "NgaySinh": ngay_sinh,
                    "balance": balance
                }
            }
        )
        return result
    
    def insert_data_user(self, stk, phone, email, username, ho_va_ten, password):
        users_collection = db['NGUOIDUNG']
        # Chèn thông tin người dùng mới vào cơ sở dữ liệu
        result = users_collection.insert_one({
            "STK": stk,
            "SDT": phone,
            "Email": email,
            "Username": username,
            "HoVaTen": ho_va_ten,
            "Password": password,
            "DiaChi": {
                "Duong": "",
                "Phuong": "",
                "Quan": "",
                "ThanhPho": ""
            },
            "NgaySinh": "",
            "GioiTinh": "",
            "Avatar": "",
            "balance": 0
        })
        return result
    
    def delete_data_user(self, SDT):
        users_collection = db['NGUOIDUNG']
        # Xóa người dùng có số tài khoản (STK) như đã nhập
        result = users_collection.delete_one({"SDT": SDT})
        return result


class admin_controller():
    def check_login(self, phone, password):
        users_collection = db['admins']
        admin = users_collection.find_one({"phone": phone, "password": password})
        return admin
    
    def get_admin_by_phone_password(self, phone, password):
        admins_collection = db['admins']
        # Tìm admin có số điện thoại và password như đã nhập
        admin = admins_collection.find_one({"phone": phone, "password": password})
        return admin

class buses_controller():  
    def get_all_buses(self):
        query = """
        MATCH (t:TUYENXE)
        RETURN t
        ORDER BY t.TenTuyenXe
        """
        result = run_query(query)
        return result
    
    def get_departure(self):
        query = """
        MATCH (n:TUYENXE)
        RETURN DISTINCT n.DiaDiemDi
        """
        result = run_query(query)
        return result
    
    def get_destination(self):
        query = """
        MATCH (n:TUYENXE)
        RETURN DISTINCT n.DiaDiemDen
        """
        result = run_query(query)
        return result
    
    def set_ID_buses(self, ten_chuyen_xe):
        query = f"""
        MATCH (c:CHUYENXE{{TenChuyenXe: '{ten_chuyen_xe}'}})
        RETURN c
        """
        result = run_query(query)
        return result
    
    def get_distance_by_name(self, ten_chuyen_xe):
        query = f"""
        MATCH (t:TUYENXE{{TenTuyenXe: '{ten_chuyen_xe}'}})
        RETURN t.QuangDuong
        """
        result = run_query(query)
        return result[0]
    
    def get_travel_time(self, ten_chuyen_xe):
        query = f"""
        MATCH (t:TUYENXE{{TenTuyenXe: '{ten_chuyen_xe}'}})
        RETURN t.ThoiGianHanhTrinh
        """
        result = run_query(query)
        return result[0]
    
    def get_available_routes(self, departure, destination, departure_date, num_tickets):
        query = f"""
        MATCH (cx:CHUYENXE)-[:THUOC]->(tx:TUYENXE)
        WHERE tx.DiaDiemDi = '{departure}' AND tx.DiaDiemDen = '{destination}'
        AND cx.NgayDi = '{departure_date}'
        AND cx.SoLuongGheTrong >= {num_tickets}
        RETURN DISTINCT tx
        """
        result = run_query(query)
        return result
    
    def get_all_list_buses(self, start_time, end_time, name, car_type=None):
        if car_type:
            query = f"""
            MATCH (cx:CHUYENXE)
            WHERE cx.GioKhoiHanh >= '{start_time}' AND cx.GioKhoiHanh < '{end_time}'
            AND cx.TenChuyenXe = '{name}'
            AND cx.LoaiXe = '{car_type}'
            RETURN cx
            """
        else:
            query = f"""
            MATCH (cx:CHUYENXE)
            WHERE cx.GioKhoiHanh >= '{start_time}' AND cx.GioKhoiHanh < '{end_time}'
            AND cx.TenChuyenXe = '{name}'
            RETURN cx
            """
        result = run_query(query)
        list_buses = [dict(node) for node in result]
        return list_buses
    
    def get_bus_by_id(self, ma_chuyen):
        query = f"""
            MATCH (n:CHUYENXE{{MaChuyen: '{ma_chuyen}'}})
            RETURN n
            """
        result = run_query(query)
        return result[0]
    
    def get_seat_id(self, ma_chuyen):
        query = f"""
        MATCH (dv:DONVE {{MaChuyen: '{ma_chuyen}'}})
        RETURN dv.Ghe
        """
        result = run_query(query)
        return result
    
    def get_price(self, ma_chuyen):
        query = f"""
                MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            RETURN cx.Gia
            """
        result = run_query(query)
        return result[0]
    
    def get_vehicle_type(self, ma_chuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            RETURN cx.LoaiXe
        """
        result = run_query(query)
        return result[0]
    
    def get_diadiemdi(self, ma_chuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            RETURN cx.DiaDiemDi 
        """
        result = run_query(query)
        return result[0]
    
    def get_diadiemden(self, ma_chuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            RETURN cx.DiaDiemDen
        """
        result = run_query(query)
        return result[0]

    def get_ten_chuyen_xe(self, ma_chuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            RETURN cx.TenChuyenXe
        """
        result = run_query(query)
        return result[0]
    
    def insert_donve(self, madon, SDT, STK, MaChuyen, Ghe, tong_gia):
        query = f"""
            CREATE (DV:DONVE{{
                Madon: '{madon}',
                SDT: '{SDT}',
                STK: '{STK}',
                MaChuyen: '{MaChuyen}',
                Ghe: {Ghe},
                TongGia: {tong_gia},
                NgayTao: date("{datetime.now().strftime('%Y-%m-%d')}"),
                GioTao: time("{datetime.now().strftime('%H:%M:%S')}")
            }})
        """
        run_query(query)
        
    def update_soluongghetrong_ma_chuyen(self, ma_chuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{ma_chuyen}'}})
            MATCH (dv:DONVE {{MaChuyen: '{ma_chuyen}'}})
            WITH cx, SUM(SIZE(dv.Ghe)) AS SoVeDaDat
            SET cx.SoLuongGheTrong = cx.SoLuongGhe - SoVeDaDat
        """
        run_query(query)
        
    def get_donve_by_stk(self, stk):
        query = f"""
            MATCH (dv:DONVE {{STK: '{stk}'}})
            RETURN dv;
        """
        result = run_query(query)
        return result
    
    def get_all_donve(self):
        query = """
            MATCH (dv:DONVE)
            RETURN dv;
        """
        result = run_query(query)
        return result
    
    def get_donve_by_madon(self, madon):
        query = f"""
            MATCH (dv:DONVE {{Madon: '{madon}'}})
            RETURN dv;
        """
        result = run_query(query)
        return result
    
    def update_donve_by_madon(self, sdt, madon, machuyen, ghe):
        query = f"""
            MATCH (dv:DONVE {{Madon: '{madon}'}})
            SET dv.SDT = '{sdt}',
                dv.MaChuyen = '{machuyen}',
                dv.Ghe = {ghe}
            RETURN dv;
        """
        result = run_query(query)
        return result
    
    def check_existing_seats(self, ghe, machuyen, madon):
        query = f"""
            MATCH (dv:DONVE {{MaChuyen: '{machuyen}'}})
            WHERE ANY(gh IN {ghe} WHERE gh IN dv.Ghe) AND (dv.Madon <> '{madon}')
            RETURN DISTINCT dv.Ghe;
        """
        result = run_query(query)
        if not result:
            return 0
        else:
            return result
        
    def check_existing_seats_in_route(self, machuyen, ghe):
        query = f"""
            MATCH (dv:DONVE {{MaChuyen: '{machuyen}'}})
            WHERE ALL(gh IN {ghe} WHERE gh IN dv.Ghe)
            RETURN DISTINCT dv.Ghe;
        """
        result = run_query(query)
        if not result:
            return False
        else:
            return True
        
    def calculate_total_price(self, machuyen, selectedSeats):
        # Lấy giá của mã chuyến
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{machuyen}'}})
            RETURN cx.Gia;
        """
        result = run_query(query)
        if not result or len(result) == 0:
                return "Mã chuyến không tồn tại hoặc không có giá được cập nhật."
        gia = result[0]
        total_price = len(selectedSeats) * convert_price_to_int(gia)
        return total_price
    
    def delete_data_donve(self, madon):
        query = f"""
            MATCH (dv:DONVE {{Madon: '{madon}'}})
            DELETE dv;
        """
        result = run_query(query)
        return result
    
    def get_all_tuyenxe(self):
        query = """
            MATCH (tx:TUYENXE)
            RETURN tx;
        """
        result = run_query(query)
        return result
    
    def insert_tuyenxe(self, tenchuyenxe, diadiemdi, diadiemden, quangduong, time):
        query = f"""
            CREATE (tx:TUYENXE{{
                TenTuyenXe: '{tenchuyenxe}',
                DiaDiemDi: '{diadiemdi}',
                DiaDiemDen: '{diadiemden}',
                QuangDuong: '{quangduong}',
                ThoiGianHanhTrinh: '{time}'
            }})
        """
        result = run_query(query)
        return result
    
    def get_all_chuyenxe(self):
        query = """
            MATCH (cx:CHUYENXE)
            RETURN cx;
        """
        result = run_query(query)
        return result
    
    def get_chuyenxe_by_machuyen(self, machuyen):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{machuyen}'}})
            RETURN cx;
        """
        result = run_query(query)
        return result
    
    def update_chuyenxe_by_machuyen(self, machuyen, diadiemdi, diadiemden, giokhoihanh, gioden, ngaydi, gia):
        query = f"""
            MATCH (cx:CHUYENXE {{MaChuyen: '{machuyen}'}})
            SET cx.DiaDiemDi = '{diadiemdi}',
                cx.DiaDiemDen = '{diadiemden}',
                cx.GioKhoiHanh = '{giokhoihanh}',
                cx.GioDen = '{gioden}',
                cx.NgayDi = '{ngaydi}',
                cx.Gia = '{gia}'
            RETURN cx;
        """
        result = run_query(query)
        return result

    def get_all_tentuyenxe(self):
        query = """
            MATCH (tx:TUYENXE)
            RETURN tx
        """
        result = run_query(query)
        return result

    def insert_data_chuyenxe(self, tenchuyen, loaixe, diadiemdi, diadiemden, giokhoihanh, gioden, ngaydi, gia):
        next_id = get_next_chuyenxe_id()
        ma_chuyen = f"CX{next_id:03d}"

        if loaixe == 'Limousine':
            so_luong_ghe = 34
        elif loaixe == 'Giường':
            so_luong_ghe = 40
        else:
            so_luong_ghe = None

        query = f"""
        CREATE (cx:CHUYENXE{{
            MaChuyen: '{ma_chuyen}',
            TenChuyenXe: '{tenchuyen}',
            DiaDiemDi: '{diadiemdi}',
            DiaDiemDen: '{diadiemden}',
            LoaiXe: '{loaixe}',
            SoLuongGhe: '{so_luong_ghe}',
            SoLuongGheTrong: '{so_luong_ghe}',
            GioKhoiHanh: '{giokhoihanh}',
            GioDen: '{gioden}',
            NgayDi: '{ngaydi}',
            Gia: '{gia}'
        }})
        """
        result = run_query(query)
        return result

    def delete_chuyenxe(self, machuyen):
        query = f"""
        MATCH (c:CHUYENXE {{ MaChuyen: '{machuyen}' }})
        DELETE c
        """
        result = run_query(query)
        return result