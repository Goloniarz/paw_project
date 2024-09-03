import psycopg2

db_name = "new_db_name"
user = "new_user"
password = "new_password"
host = "localhost"
port = "5432"

try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    print(f"Connected to database '{db_name}' as '{user}'.")

    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'Car'
        );
    """)
    exists = cursor.fetchone()[0]

    if not exists:
        cursor.execute("""
            CREATE TABLE Car (
                id SERIAL PRIMARY KEY,
                brand VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                price FLOAT NOT NULL,
                power INT NOT NULL,
                color VARCHAR(20) NOT NULL
            )
        """)
        print("Table 'Car' created.")

    sample_cars = [
        ('BMW', 'M3', 75000, 430, 'Black'),
        ('Audi', 'A4', 45000, 300, 'White'),
        ('Mercedes', 'C-Class', 55000, 350, 'Silver'),
        ('BMW', 'X5', 80000, 450, 'Blue'),
        ('Audi', 'Q7', 85000, 500, 'Grey'),
        ('Mercedes', 'GLE', 90000, 520, 'Black'),
        ('BMW', 'Z4', 65000, 400, 'Red'),
        ('Audi', 'TT', 70000, 420, 'Yellow'),
        ('Mercedes', 'E-Class', 60000, 380, 'Blue'),
        ('BMW', '5 Series', 70000, 440, 'Black'),
        ('Audi', 'S6', 75000, 450, 'White'),
        ('Mercedes', 'S-Class', 100000, 620, 'Silver'),
        ('BMW', 'i8', 150000, 570, 'Green'),
        ('Audi', 'R8', 160000, 610, 'Red'),
        ('Mercedes', 'G-Class', 200000, 700, 'Black'),
        ('BMW', 'M5', 85000, 600, 'White'),
        ('Audi', 'A6', 55000, 330, 'Silver'),
        ('Mercedes', 'GLA', 45000, 250, 'Blue'),
        ('BMW', 'X3', 65000, 350, 'Grey'),
        ('Audi', 'Q5', 70000, 400, 'Black')
    ]

    insert_query = """
        INSERT INTO Car (brand, model, price, power, color)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, sample_cars)

    conn.commit()

    print("Data added to table 'Car'.")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error while connecting to database: {e}")
