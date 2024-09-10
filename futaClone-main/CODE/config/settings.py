from pymongo import MongoClient
from neo4j import GraphDatabase


# Thiết lập kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['futabus']

# Thiết lập kết nối đến Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
database = "futabus"  # Tên cơ sở dữ liệu cụ thể bạn muốn kết nối

def run_query(query):
    try:
        with GraphDatabase.driver(uri, auth=(username, password), database=database) as driver:
            with driver.session() as session:
                result = session.run(query)
                # Trả về kết quả dưới dạng danh sách các giá trị
                return [record[0] for record in result]  # Lấy giá trị đầu tiên từ mỗi bản ghi
        print("Kết nối thành công!")
    except Exception as e:
        print("Đã xảy ra lỗi khi kết nối:", e)


