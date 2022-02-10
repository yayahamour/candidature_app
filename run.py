from App import app, models
import os

if __name__ == '__main__':
    models.init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(port = port,host = '0.0.0.0')