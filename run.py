# from app import create_appss

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

import traceback

try:
    from app import create_app
    app = create_app()
except Exception as e:
    print("❌ Error al iniciar la app:")
    traceback.print_exc()
    raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
