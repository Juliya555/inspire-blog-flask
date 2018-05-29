# Inspire Blog Project
This is an interior design blog for decorating, interior planning or redesigning.
It is built to run in **Python 3** using the **Flask** micro-web framework. Tested for Ubuntu Linux 16.04 LTS.
It uses MySQL database (tested for MySQL 14.14).


# Setup
1. Create virtual enviroment and activate it:
  ```
  python -m venv env_name
  source env_name/bin/activate
  ```
2. Clone the repository:
  ```
  git clone https://github.com/Juliya555/inspire-blog-flask.git
  ```
3. Install all requirements:
  ```
  pip install -r requirements.txt
  ```
4. Create your db. Copy file **'config.ref.py'** to **'config.py'** and change **SQLALCHEMY_DATABASE_URI** according to your database settings. 
5. Create a gmail account for communicating with your visitors. Change **MAIL_USERNAME** and **MAIL_PASSWORD** in **'config.py'** according to your gmail settings.
6. Use **db_dump.sql** file to load structure and data to launch the project.
  ```
  mysql -u root -p -f mysql_db_name < db_dump.sql
  ```

# Run
1. Run the server:
  ```
  python main.py
  ```
2. Open http://127.0.0.1:5000 in your web browser to see the blog.
3. Open http://127.0.0.1:5000/admin in your web browser to see the admin pannel.

# HowTOs
1. Use admin user info to login to admin pannel:
  ```
  Email Address: admin@example.com
  Password: password
  ```
2. MySQL create db dump:
  ```
  mysqldump -u USER -pPASSWORD DATABASE > /path/to/file/dump.sql
  ```
