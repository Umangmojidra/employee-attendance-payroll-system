import mysql.connector
from decimal import Decimal
from datetime import datetime,time
from tabulate import tabulate
import csv

conn =mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "eap"
    )

mycursor = conn.cursor()

def add_employee():

    e_name = input("Enter the Employee Name :")
    dep_id = int(input("Enter department ID :"))
    city = input("Enter the City :")
    mobile = int(input("Enter mobile number :"))
    email = input("Enter email :")
    salary = Decimal(input("Enter salary :"))
    blood_group = input("Enter the Blood group :")


    query = "INSERT INTO employees (e_name,dep_id,mobile,email,city,blood_group,salary) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    values = (e_name ,dep_id, mobile , email,city,blood_group,salary)
    mycursor.execute(query, values)
    conn.commit()
    e_id = mycursor.lastrowid
    print(f" Employee Addeed successfully! Employee Id: {e_id}")
    conn.commit()

def view_all_employees():
    query = "SELECT * FROM employees"
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    print(tabulate(result, headers=columns, tablefmt="fancy_grid"))

def update_employee_details():
    e_id = int(input("Enter Employee id to Upadte : "))
    mycursor.execute("SELECT e_id FROM employees WHERE e_id = %s", (e_id,))
    result = mycursor.fetchone()


    if result is None:
        print("Employee not found!")
        return
    
    e_name = input("Enter the Employee Name :")
    dep_id = int(input("Enter department ID :"))
    city = input("Enter the City :")
    mobile = int(input("Enter mobile number :"))
    email = input("Enter email :")
    salary = Decimal(input("Enter salary :"))
    blood_group = input("Enter the Blood group :")
    
    query1 = " UPDATE employees SET e_name = %s, dep_id = %s ,mobile = %s, email = %s, city = %s, blood_group = %s, salary = %s WHERE e_id = %s"
    values = (e_name, dep_id,mobile, email, city,blood_group,salary,e_id)
    mycursor.execute(query1,values)
    conn.commit()
    print("Data Updated")

def attendance_reminder():
    query = "SELECT e.e_id, e.e_name FROM employees e LEFT JOIN attendance a ON e.e_id = a.e_id AND a.login_date = CURDATE() WHERE a.e_id IS NULL;"
    mycursor.execute(query)
    missing = mycursor.fetchall()
    if missing:
        print("\n Reminder: Some employees have not marked attendance today!")
        print("Employees pending attendance:")
        for emp in missing:
            print(f" - {emp[0]} | {emp[1]}")
    else:
        print("\n All employees have marked attendance today!")

def generate_payroll():
    e_id = int(input("Enter Employee id : "))
    mycursor.execute("SELECT e_id,salary FROM employees WHERE e_id = %s", (e_id,))
    result = mycursor.fetchone()
    base_salary = result[1]
    dep_id = int(input("Enter Department Id : "))
    per_bonus = Decimal(input("Enter perfomance bonus : "))
    pro_fund = Decimal(input("Enter Provident fund amount  :"))
    tax = Decimal(input("Enter tax in percentage :"))

    if result is None:
        print("Employee not found!")
        return
    query = '''
    SELECT
    e_id,
    MONTH(login_date) AS month,
    sum(status = 'Half_Day') AS half_days,
    sum(status = 'Present') AS full_days,
    sum(status = 'Work_from_home') AS wfh_days,
    sum(status = 'Absent') AS absents,
    sum(penalty = 1 ) AS total_penalty,
    sum(overtime) AS total_overtime
FROM attendance
WHERE e_id = %s
GROUP BY e_id, MONTH(login_date)
ORDER BY month;
    '''
    mycursor.execute(query,(e_id,))
    result = mycursor.fetchone()
    month = result[1]
    half_days = result[2]
    full_days = result[3]
    wfhs = result[4]
    absents =result[5]
    total_penalty = result[6]
    total_overtime = result[7]
    per_day_salary = base_salary / 30
    pro_rated_sal = Decimal(full_days * per_day_salary) + (wfhs * per_day_salary) + (half_days * (per_day_salary /2)) + (total_overtime * 200) + per_bonus - pro_fund - (total_penalty*50)
    pro_rated_sal_tax = pro_rated_sal * (tax/100)
    pro_rated_sal = pro_rated_sal - pro_rated_sal_tax
    

    query = "INSERT INTO payroll (e_id,dep_id,half_days,full_days,wfhs,absents,month,per_bonus,total_overtime,total_penalty,pro_rated_sal,tax_amount,pro_fund) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (e_id,dep_id,half_days,full_days,wfhs,absents,month,per_bonus,total_overtime,total_penalty,pro_rated_sal,pro_rated_sal_tax,pro_fund)
    mycursor.execute(query, values)

    conn.commit()
    e_id = mycursor.lastrowid
    print(f" Employee Addeed successfully!...")
    conn.commit()

def generate_payment_slip():
    try:
        e_id = int(input("Enter Employee ID: "))

        query = """
        SELECT 
            e.e_name,
            p.month,
            p.full_days,
            p.half_days,
            p.wfhs,
            p.absents,
            p.pro_rated_sal,
            p.per_bonus,
            p.tax_amount,
            p.pro_fund
        FROM payroll p
        JOIN employees e ON p.e_id = e.e_id
        WHERE p.e_id = %s
        ORDER BY p.month DESC
        LIMIT 1;
        """
        mycursor.execute(query, (e_id,))
        result = mycursor.fetchone()

        if not result:
            print("Payroll record not found!")
            return

        e_name, month, full_days, half_days, wfhs, absents, pro_rated_sal, bonus, tax, pf = result

        net_pay = pro_rated_sal + bonus - (tax + pf)

        # Print simple salary slip
        print("\n" + "="*50)
        print(f"{'COMPANY Payment Slip. LTD.':^50}")
        print("="*50)
        print(f"Employee Name : {e_name}")
        print(f"Month         : {month} / 2025")
        print("-"*50)
        print("Attendance:")
        print(f" Full Days  : {full_days}")
        print(f" Half Days  : {half_days}")
        print(f" WFH Days   : {wfhs}")
        print(f" Absents    : {absents}")
        print("-"*50)
        print("Salary:")
        print(f" Pro-Rated Salary : ₹{pro_rated_sal:.2f}")
        print(f" Bonus            : ₹{bonus:.2f}")
        print(f" Tax              : ₹{tax:.2f}")
        print(f" Provident Fund   : ₹{pf:.2f}")
        print(f" Net Pay          : ₹{net_pay:.2f}")
        print("="*50 + "\n")
    except ValueError:
        print("Invalid Employee ID!")

def delete_Employee():
    e_id = int(input("Enter Employee id to delete employee info: "))
    mycursor.execute("SELECT e_id FROM employees WHERE e_id = %s", (e_id,))
    result = mycursor.fetchone()

    if result is None:
        print("Employee not found!")
        return

    confirm = input("Are you sure you want to delete this employee and all related data? (yes/no): ").lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    # Delete related records first
    mycursor.execute("DELETE FROM employees WHERE e_id = %s", (e_id,))

    conn.commit()
    print("Employee and all related records deleted successfully.")

def department_payroll_summary():

    query = """SELECT 
        p.dep_id,
        d.dep_name,
        COUNT(DISTINCT p.e_id) AS total_employees,
        SUM(p.pro_rated_sal + p.per_bonus - (p.tax_amount + p.pro_fund)) AS total_net_pay,
        AVG(p.pro_rated_sal + p.per_bonus - (p.tax_amount + p.pro_fund)) AS avg_net_salary,
        SUM(p.total_overtime) AS total_overtime,
        SUM(p.absents) AS total_absents
    FROM payroll p
    JOIN departments d ON p.dep_id = d.dep_id
    GROUP BY p.dep_id, d.dep_name
    ORDER BY total_net_pay DESC;
    """

    mycursor.execute(query)
    result = mycursor.fetchall()

    columns = [desc[0] for desc in mycursor.description]

    filename = "department_payroll_surmmary.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  
        writer.writerows(result)
    print("CSV file created successfully")

def manager():
    while True:
        print("=" * 30)
        print("--------MANAGER MENU--------")
        print("=" * 30)
        print("---- Enter Choice ----")
        print("1. Add Employee ")
        print("2. View all employees")
        print("3. Update employee details ")
        print("4. Attendance Reminder")
        print("5. Generate Payroll")
        print("6. Generate Payment Slip") 
        print("7. Department payroll surmmary")
        print("8. Delete Employee Details")
        print("9. Exit ")
        print("=" * 30)

        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            view_all_employees()
        elif choice == '3':
            update_employee_details()
        elif choice == '4':
            attendance_reminder()
        elif choice == '5':
            generate_payroll()
        elif choice == '6':
            generate_payment_slip()
        elif choice == '7':
            department_payroll_summary()
        elif choice == '8':
            delete_Employee()
        elif choice == '9':
            print("Thank you")
            break
        else:
            print("Invalid choice. Please try again.")

def attendance():
    #Input 
    e_id = int(input("Enter Employee ID: "))
    dep_id = int(input("Enter department ID: "))

    #Validation
    query ="SELECT e_id FROM employees WHERE e_id = %s"
    mycursor.execute(query, (e_id,))
    result = mycursor.fetchone()

    #Attendance status
    status = ""
    if result is None:
        print("Account not found!")
        return
    else :
        while True:
            print("=" * 20)
            print("---SELECT STATUS---")
            print("=" * 20)
            print("1. Present ")
            print("2. Absent ")
            print("3. Half-Day ")
            print("4. Work from home ")

            choice = input("Enter Choice: ")
            if choice == '1':
                status = "Present"
                break
            elif choice == '2':
                status = "Absent"
                break
            elif choice == '3':
                status = "Half_Day"
                break
            elif choice == '4':
                status = "Work_from_home"
                break
        print("Status:",status)
    #Time and Date 
    login_date = datetime.now().date()
    login_time = datetime.now().time()
    threshold = time(10, 30, 0)
    # login_time = time(12,0,0)
    # print(login_time)

    #penalty 
    penalty = 0
    if status != "Absent":
        if login_time > threshold:
            penalty = 1
            print("You are late today")

    query = """
    INSERT INTO attendance 
    (e_id, login_date, login_time, status, penalty, dep_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (e_id, login_date, login_time,status, penalty, dep_id)
    mycursor.execute(query, values)
    conn.commit()

    print("Record saved successfully!")

def login():
    print("=" * 30)
    print("-----MANAGER LOGIN PAGE-----")
    print("=" * 30)
    m_id = input("Enter your Id: ")
    pin = int(input("Enter your pin: "))

    query = "SELECT m_name , pin FROM manager WHERE m_id = %s"
    mycursor.execute(query, (m_id,))
    result = mycursor.fetchone()
    if result[1] == pin:
        print("HI",result[0],"....!")
        manager()
        return
    else:
        print("invalid log in details")

def main():
    while True:
        print("=" * 30)
        print("----------Welcome------------")
        print("=" * 30)
        print("---- Enter Choice ----")
        print("1. Mark Attendance  ")
        print("2. Manager login")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            attendance()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Have a nice day ")
            break

main()
mycursor.close()
conn.close()