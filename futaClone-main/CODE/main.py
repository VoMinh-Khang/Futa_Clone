from apps.views import app

def main():
    app.run(debug=True, port=8000)
    
if __name__ == '__main__':
    main()