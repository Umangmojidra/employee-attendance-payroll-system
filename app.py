"""
EAP - Employee & Attendance Portal
Flask Web Application — exactly matched to your eap MySQL schema
Tables: employees, attendance, departments, manager, payroll
"""
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
from decimal import Decimal
from datetime import datetime, time, timedelta
import io, base64
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'eap_secret_xK9_2024')

# ── DB ─────────────────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'root'),
        database=os.environ.get('MYSQL_DB', 'eap'),
        port=int(os.environ.get('MYSQL_PORT', 3306))
    )

# ── DECORATORS ─────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def w(*a, **k):
        if 'user' not in session: return redirect(url_for('login'))
        return f(*a, **k)
    return w

def manager_required(f):
    @wraps(f)
    def w(*a, **k):
        if 'user' not in session: return redirect(url_for('login'))
        if session.get('role') != 'manager':
            flash('Manager access required.', 'danger')
            return redirect(url_for('employee_dashboard'))
        return f(*a, **k)
    return w

# ── CHART HELPERS ──────────────────────────────────────────────
def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=130)
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return img

def style_axes(axlist):
    for ax in axlist:
        ax.set_facecolor('#131f2e')
        ax.tick_params(colors='#7a95b0', labelsize=9)
        ax.xaxis.label.set_color('#7a95b0')
        ax.yaxis.label.set_color('#7a95b0')
        ax.title.set_color('#dde8f4')
        for sp in ax.spines.values(): sp.set_edgecolor('#1e3448')

CLRS = ['#3b9eff','#34d399','#fbbf24','#a78bfa','#f87171','#60a5fa','#4ade80','#fb923c']

# ── LOGIN ──────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('admin_dashboard') if session['role'] == 'manager'
                        else url_for('employee_dashboard'))
    if request.method == 'POST':
        role = request.form.get('role', 'employee')
        if role == 'employee':
            e_id = request.form.get('e_id', '').strip()
            if e_id.isdigit():
                conn = get_db(); cur = conn.cursor(dictionary=True)
                cur.execute("SELECT e_id, e_name FROM employees WHERE e_id = %s", (int(e_id),))
                emp = cur.fetchone(); conn.close()
                if emp:
                    session.update({'user': emp['e_id'], 'name': emp['e_name'], 'role': 'employee'})
                    return redirect(url_for('employee_dashboard'))
            flash('Employee ID not found.', 'danger')
        elif role == 'manager':
            m_id = request.form.get('m_id', '').strip()
            pin  = request.form.get('pin', '').strip()
            # m_id is INT in your schema
            if m_id.isdigit() and pin.isdigit():
                conn = get_db(); cur = conn.cursor(dictionary=True)
                cur.execute("SELECT m_id, m_name, pin FROM manager WHERE m_id = %s", (int(m_id),))
                mgr = cur.fetchone(); conn.close()
                if mgr and mgr['pin'] == int(pin):
                    session.update({'user': mgr['m_id'], 'name': mgr['m_name'], 'role': 'manager'})
                    return redirect(url_for('admin_dashboard'))
            flash('Invalid manager credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

# ── EMPLOYEE DASHBOARD ─────────────────────────────────────────
@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if session['role'] == 'manager': return redirect(url_for('admin_dashboard'))
    e_id = session['user']; today = datetime.now().date()
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT e.*, d.dep_name FROM employees e
                   LEFT JOIN departments d ON e.dep_id = d.dep_id WHERE e.e_id = %s""", (e_id,))
    emp = cur.fetchone()
    cur.execute("SELECT * FROM attendance WHERE e_id = %s AND login_date = %s LIMIT 1", (e_id, today))
    today_att = cur.fetchone()
    cur.execute("""SELECT login_date, login_time, status, penalty, overtime, dep_id
                   FROM attendance WHERE e_id = %s ORDER BY login_date DESC, login_time DESC LIMIT 10""", (e_id,))
    last10 = cur.fetchall()
    cur.execute("SELECT COUNT(*) AS c FROM attendance WHERE e_id = %s AND status = 'Present'", (e_id,)); present_count = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS c FROM attendance WHERE e_id = %s AND status = 'Absent'", (e_id,)); absent_count = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS c FROM attendance WHERE e_id = %s", (e_id,)); total_count = cur.fetchone()['c']
    cur.execute("SELECT dep_id, dep_name FROM departments ORDER BY dep_name"); departments = cur.fetchall()
    conn.close()
    att_rate = round(present_count / total_count * 100, 1) if total_count else 0
    return render_template('employee_dashboard.html', today=today, emp=emp, today_att=today_att,
        last10=last10, present_count=present_count, absent_count=absent_count,
        total_count=total_count, att_rate=att_rate, departments=departments)

@app.route('/employee/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    e_id = session['user']
    dep_id = request.form.get('dep_id', type=int)
    status = request.form.get('status', 'Present')
    today = datetime.now().date()
    conn = get_db(); cur = conn.cursor(dictionary=True)
    # attendance has no UNIQUE constraint — check manually
    cur.execute("SELECT e_id FROM attendance WHERE e_id = %s AND login_date = %s", (e_id, today))
    if cur.fetchone():
        flash('Attendance already marked for today!', 'warning'); conn.close()
        return redirect(url_for('employee_dashboard'))
    login_time = datetime.now().time()
    penalty = 1 if (status != 'Absent' and login_time > time(10, 30, 0)) else 0
    cur.execute("""INSERT INTO attendance (e_id, dep_id, status, login_date, login_time, penalty, overtime)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (e_id, dep_id, status, today, login_time, penalty, 0))
    conn.commit(); conn.close()
    msg = f'Attendance marked as {status}!'
    if penalty: msg += ' Late penalty applied (login after 10:30 AM).'
    flash(msg, 'success' if not penalty else 'warning')
    return redirect(url_for('employee_dashboard'))

# ── ADMIN DASHBOARD ────────────────────────────────────────────
@app.route('/admin/dashboard')
@manager_required
def admin_dashboard():
    today = datetime.now().date(); conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS c FROM employees"); total_emp = cur.fetchone()['c']
    cur.execute("""SELECT COUNT(DISTINCT e_id) AS c FROM attendance
                   WHERE login_date = %s AND status != 'Absent'""", (today,)); present_today = cur.fetchone()['c']
    cur.execute("""SELECT a.e_id, e.e_name, a.status, a.login_time, a.penalty, d.dep_name
                   FROM attendance a JOIN employees e ON a.e_id = e.e_id
                   LEFT JOIN departments d ON a.dep_id = d.dep_id
                   WHERE a.login_date = %s ORDER BY a.login_time""", (today,)); today_list = cur.fetchall()
    trend = []
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).date()
        cur.execute("""SELECT COUNT(DISTINCT e_id) AS c FROM attendance
                       WHERE login_date = %s AND status != 'Absent'""", (d,))
        trend.append({'date': str(d)[5:], 'present': cur.fetchone()['c']})
    cur.execute("""SELECT e.e_id, e.e_name FROM employees e
                   LEFT JOIN attendance a ON e.e_id = a.e_id AND a.login_date = %s
                   WHERE a.e_id IS NULL""", (today,)); not_marked = cur.fetchall()
    conn.close()
    rate = round(present_today / total_emp * 100, 1) if total_emp else 0
    return render_template('admin_dashboard.html', today=today, total_emp=total_emp,
        present_today=present_today, absent_today=total_emp - present_today,
        today_list=today_list, trend=trend, not_marked=not_marked, rate=rate)

# ── ADMIN EMPLOYEES CRUD ───────────────────────────────────────
@app.route('/admin/employees', methods=['GET', 'POST'])
@manager_required
def admin_employees():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        act = request.form.get('action')
        if act == 'add':
            cur.execute("""INSERT INTO employees (e_name, dep_id, mobile, email, city, blood_group, salary)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (request.form['e_name'], request.form['dep_id'] or None,
                         request.form['mobile'] or None, request.form['email'],
                         request.form['city'], request.form['blood_group'], request.form['salary'] or None))
            conn.commit(); flash(f'Employee added! ID: {cur.lastrowid}', 'success')
        elif act == 'update':
            cur.execute("""UPDATE employees SET e_name=%s, dep_id=%s, mobile=%s, email=%s,
                           city=%s, blood_group=%s, salary=%s WHERE e_id=%s""",
                        (request.form['e_name'], request.form['dep_id'] or None,
                         request.form['mobile'] or None, request.form['email'],
                         request.form['city'], request.form['blood_group'],
                         request.form['salary'] or None, request.form['e_id']))
            conn.commit(); flash('Employee updated.', 'success')
        elif act == 'delete':
            eid = request.form.get('e_id')
            cur.execute("DELETE FROM attendance WHERE e_id = %s", (eid,))
            cur.execute("DELETE FROM payroll WHERE e_id = %s", (eid,))
            cur.execute("DELETE FROM employees WHERE e_id = %s", (eid,))
            conn.commit(); flash('Employee deleted.', 'success')
    cur.execute("""SELECT e.*, d.dep_name FROM employees e
                   LEFT JOIN departments d ON e.dep_id = d.dep_id ORDER BY e.e_id""")
    employees = cur.fetchall()
    cur.execute("SELECT dep_id, dep_name FROM departments ORDER BY dep_name"); departments = cur.fetchall()
    conn.close()
    return render_template('admin_employees.html', employees=employees, departments=departments)

# ── ADMIN ATTENDANCE MONITOR ───────────────────────────────────
@app.route('/admin/attendance')
@manager_required
def admin_attendance():
    fd  = request.args.get('date', str(datetime.now().date()))
    fn  = request.args.get('name', '').strip()
    fdep = request.args.get('dep_id', '').strip()
    conn = get_db(); cur = conn.cursor(dictionary=True)
    q = """SELECT a.e_id, e.e_name, a.status, a.login_date, a.login_time, a.penalty, a.overtime, d.dep_name
           FROM attendance a JOIN employees e ON a.e_id = e.e_id
           LEFT JOIN departments d ON a.dep_id = d.dep_id WHERE a.login_date = %s"""
    params = [fd]
    if fn:   q += " AND e.e_name LIKE %s"; params.append(f'%{fn}%')
    if fdep: q += " AND a.dep_id = %s";   params.append(fdep)
    q += " ORDER BY a.login_time"
    cur.execute(q, params); records = cur.fetchall()
    cur.execute("""SELECT e.e_id, e.e_name, d.dep_name FROM employees e
                   LEFT JOIN departments d ON e.dep_id = d.dep_id
                   LEFT JOIN attendance a ON e.e_id = a.e_id AND a.login_date = %s
                   WHERE a.e_id IS NULL""", (fd,)); not_marked = cur.fetchall()
    cur.execute("SELECT dep_id, dep_name FROM departments ORDER BY dep_name"); departments = cur.fetchall()
    conn.close()
    return render_template('admin_attendance.html', records=records, not_marked=not_marked,
        departments=departments, filter_date=fd, filter_name=fn, filter_dept=fdep)

# ── ADMIN PAYROLL ──────────────────────────────────────────────
@app.route('/admin/payroll', methods=['GET', 'POST'])
@manager_required
def admin_payroll():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        e_id      = int(request.form['e_id'])
        dep_id    = int(request.form['dep_id'])
        per_bonus = Decimal(request.form.get('per_bonus', '0') or '0')
        pro_fund  = Decimal(request.form.get('pro_fund', '0') or '0')
        tax_pct   = Decimal(request.form.get('tax', '0') or '0')
        cur.execute("SELECT salary FROM employees WHERE e_id = %s", (e_id,)); row = cur.fetchone()
        if not row:
            flash('Employee not found!', 'danger')
        else:
            base_salary = Decimal(str(row['salary']))
            cur.execute("""
                SELECT MONTH(login_date) AS month,
                       SUM(status = 'Half_Day')        AS half_days,
                       SUM(status = 'Present')         AS full_days,
                       SUM(status = 'Work_from_home')  AS wfh_days,
                       SUM(status = 'Absent')          AS absents,
                       SUM(penalty = 1)                AS total_penalty,
                       SUM(overtime)                   AS total_overtime
                FROM attendance WHERE e_id = %s
                GROUP BY MONTH(login_date) ORDER BY month DESC LIMIT 1
            """, (e_id,)); att = cur.fetchone()
            if not att:
                flash('No attendance data for this employee!', 'warning')
            else:
                hd  = int(att['half_days']     or 0); fd2 = int(att['full_days']    or 0)
                wfh = int(att['wfh_days']       or 0); ab  = int(att['absents']      or 0)
                pen = int(att['total_penalty']  or 0); ot  = int(att['total_overtime'] or 0)
                mon = int(att['month'])
                per_day = base_salary / 30
                gross = (Decimal(fd2) * per_day + Decimal(wfh) * per_day
                       + Decimal(hd) * (per_day / 2) + Decimal(ot) * 200
                       + per_bonus - pro_fund - Decimal(pen) * 50)
                tax_amt = gross * (tax_pct / 100); net = gross - tax_amt
                # per_bonus is INT in schema
                cur.execute("""INSERT INTO payroll
                    (e_id, dep_id, half_days, full_days, wfhs, absents, month, per_bonus,
                     total_overtime, total_penalty, pro_rated_sal, tax_amount, pro_fund)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (e_id, dep_id, hd, fd2, wfh, ab, mon,
                     int(per_bonus), ot, pen, net, tax_amt, pro_fund))
                conn.commit()
                flash(f'Payroll generated! Net Pay: Rs.{net:,.2f}', 'success')
    cur.execute("""SELECT p.*, e.e_name, d.dep_name FROM payroll p
                   JOIN employees e ON p.e_id = e.e_id
                   LEFT JOIN departments d ON p.dep_id = d.dep_id
                   ORDER BY p.month DESC, e.e_name"""); payrolls = cur.fetchall()
    cur.execute("SELECT e_id, e_name FROM employees ORDER BY e_name"); employees = cur.fetchall()
    cur.execute("SELECT dep_id, dep_name FROM departments ORDER BY dep_name"); departments = cur.fetchall()
    conn.close()
    return render_template('admin_payroll.html', payrolls=payrolls, employees=employees, departments=departments)

@app.route('/admin/payment_slip/<int:e_id>')
@manager_required
def payment_slip(e_id):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT p.*, e.e_name, d.dep_name FROM payroll p
                   JOIN employees e ON p.e_id = e.e_id
                   LEFT JOIN departments d ON p.dep_id = d.dep_id
                   WHERE p.e_id = %s ORDER BY p.month DESC LIMIT 1""", (e_id,))
    slip = cur.fetchone(); conn.close()
    if not slip:
        flash('No payroll record found.', 'danger'); return redirect(url_for('admin_payroll'))
    net_pay = (float(slip['pro_rated_sal'] or 0) + float(slip['per_bonus'] or 0)
               - float(slip['tax_amount'] or 0) - float(slip['pro_fund'] or 0))
    return render_template('payment_slip.html', slip=slip, net_pay=net_pay, now=datetime.now())

# ── ANALYTICS ──────────────────────────────────────────────────
@app.route('/admin/analytics/attendance')
@manager_required
def analytics_attendance():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT login_date, SUM(status='Present') AS present, SUM(status='Absent') AS absent,
                   SUM(status='Half_Day') AS half_day, SUM(status='Work_from_home') AS wfh, SUM(penalty=1) AS late
                   FROM attendance GROUP BY login_date ORDER BY login_date DESC LIMIT 30""")
    rows = list(reversed(cur.fetchall()))
    cur.execute("SELECT status, COUNT(*) AS cnt FROM attendance GROUP BY status")
    status_totals = {r['status']: r['cnt'] for r in cur.fetchall()}
    conn.close()
    fig, axes = plt.subplots(1, 2, figsize=(17, 6)); fig.patch.set_facecolor('#0d1b2a'); style_axes(axes)
    if rows:
        labels = [str(r['login_date'])[5:] for r in rows]
        present = [int(r['present'] or 0) for r in rows]; wfh = [int(r['wfh'] or 0) for r in rows]; absent = [int(r['absent'] or 0) for r in rows]
        x = list(range(len(labels)))
        axes[0].bar(x, present, color='#34d399', label='Present', alpha=.9)
        axes[0].bar(x, wfh, bottom=present, color='#3b9eff', label='WFH', alpha=.9)
        axes[0].bar(x, absent, bottom=[p+w for p,w in zip(present,wfh)], color='#f87171', label='Absent', alpha=.9)
        axes[0].set_xticks(x[::3]); axes[0].set_xticklabels(labels[::3], rotation=45, ha='right', fontsize=8)
        axes[0].set_title('30-Day Daily Attendance', fontweight='bold', fontsize=13)
        axes[0].legend(facecolor='#131f2e', labelcolor='#dde8f4', fontsize=9); axes[0].set_ylabel('Employees')
    else:
        axes[0].text(0.5, 0.5, 'No data yet', ha='center', va='center', color='#7a95b0', transform=axes[0].transAxes, fontsize=14)
    if status_totals:
        axes[1].pie(list(status_totals.values()), labels=list(status_totals.keys()), autopct='%1.1f%%',
                    colors=CLRS[:len(status_totals)], textprops={'color':'#dde8f4','fontsize':9}, startangle=90)
        axes[1].set_title('Status Distribution', fontweight='bold', fontsize=13)
    plt.suptitle('Attendance Analytics', fontsize=17, fontweight='bold', color='#3b9eff', y=1.02)
    plt.tight_layout()
    return render_template('analytics.html', title='Attendance Analytics', chart=fig_to_b64(fig), active='attendance', now=datetime.now())

@app.route('/admin/analytics/payroll')
@manager_required
def analytics_payroll():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT d.dep_name, COUNT(DISTINCT p.e_id) AS employees, SUM(p.pro_rated_sal) AS total_pay, AVG(p.pro_rated_sal) AS avg_pay
                   FROM payroll p JOIN departments d ON p.dep_id = d.dep_id GROUP BY p.dep_id, d.dep_name"""); dept_data = cur.fetchall()
    cur.execute("""SELECT e.e_name, SUM(p.pro_rated_sal) AS net FROM payroll p JOIN employees e ON p.e_id = e.e_id
                   GROUP BY p.e_id ORDER BY net DESC LIMIT 10"""); top_earners = cur.fetchall()
    conn.close()
    fig, axes = plt.subplots(1, 2, figsize=(17, 6)); fig.patch.set_facecolor('#0d1b2a'); style_axes(axes)
    if dept_data:
        names = [r['dep_name'] for r in dept_data]; pays = [float(r['total_pay'] or 0) for r in dept_data]
        axes[0].bar(names, pays, color=CLRS[:len(names)]); axes[0].set_title('Payroll by Department', fontweight='bold', fontsize=13)
        axes[0].set_ylabel('Total Net Pay (Rs.)'); axes[0].tick_params(axis='x', rotation=20)
    else: axes[0].text(0.5, 0.5, 'No payroll data', ha='center', va='center', color='#7a95b0', transform=axes[0].transAxes, fontsize=14)
    if top_earners:
        n2 = [r['e_name'] for r in top_earners]; nets = [float(r['net'] or 0) for r in top_earners]
        axes[1].barh(n2, nets, color='#fbbf24', alpha=.9); axes[1].invert_yaxis()
        axes[1].set_title('Top 10 Earners', fontweight='bold', fontsize=13); axes[1].set_xlabel('Net Pay (Rs.)')
    else: axes[1].text(0.5, 0.5, 'No payroll data', ha='center', va='center', color='#7a95b0', transform=axes[1].transAxes, fontsize=14)
    plt.suptitle('Payroll Analytics', fontsize=17, fontweight='bold', color='#3b9eff', y=1.02); plt.tight_layout()
    return render_template('analytics.html', title='Payroll Analytics', chart=fig_to_b64(fig), active='payroll', now=datetime.now())

@app.route('/admin/analytics/department')
@manager_required
def analytics_department():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT d.dep_name, COUNT(e.e_id) AS emp_count, AVG(e.salary) AS avg_sal
                   FROM departments d LEFT JOIN employees e ON d.dep_id = e.dep_id GROUP BY d.dep_id, d.dep_name"""); dept_emp = cur.fetchall()
    cur.execute("""SELECT d.dep_name, SUM(a.penalty=1) AS late_count, SUM(a.status='Absent') AS absent_count, SUM(a.overtime) AS total_ot
                   FROM attendance a JOIN departments d ON a.dep_id = d.dep_id GROUP BY a.dep_id, d.dep_name"""); dept_att = cur.fetchall()
    conn.close()
    fig, axes = plt.subplots(1, 2, figsize=(17, 6)); fig.patch.set_facecolor('#0d1b2a'); style_axes(axes)
    if dept_emp:
        names = [r['dep_name'] for r in dept_emp]; counts = [r['emp_count'] for r in dept_emp]; avgs = [float(r['avg_sal'] or 0) for r in dept_emp]
        x = list(range(len(names)))
        axes[0].bar(x, counts, color=CLRS[:len(names)]); axes[0].set_xticks(x); axes[0].set_xticklabels(names, rotation=20)
        axes[0].set_title('Employees per Department', fontweight='bold', fontsize=13); axes[0].set_ylabel('Headcount')
        ax2 = axes[0].twinx(); ax2.plot(x, avgs, color='#fbbf24', marker='o', lw=2, ms=7)
        ax2.set_ylabel('Avg Salary (Rs.)', color='#fbbf24'); ax2.tick_params(colors='#fbbf24'); ax2.spines['right'].set_edgecolor('#fbbf24'); ax2.set_facecolor('#131f2e')
    if dept_att:
        dn = [r['dep_name'] for r in dept_att]; lt = [int(r['late_count'] or 0) for r in dept_att]; ab = [int(r['absent_count'] or 0) for r in dept_att]
        x2 = list(range(len(dn)))
        axes[1].bar(x2, lt, color='#fbbf24', label='Late', alpha=.9); axes[1].bar(x2, ab, bottom=lt, color='#f87171', label='Absent', alpha=.9)
        axes[1].set_xticks(x2); axes[1].set_xticklabels(dn, rotation=20); axes[1].set_title('Penalties & Absences by Dept', fontweight='bold', fontsize=13)
        axes[1].legend(facecolor='#131f2e', labelcolor='#dde8f4', fontsize=9)
    plt.suptitle('Department Analytics', fontsize=17, fontweight='bold', color='#3b9eff', y=1.02); plt.tight_layout()
    return render_template('analytics.html', title='Department Analytics', chart=fig_to_b64(fig), active='department', now=datetime.now())

@app.route('/admin/analytics/performance')
@manager_required
def analytics_performance():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT e.e_name, SUM(a.status='Present') AS present_days, SUM(a.status='Absent') AS absent_days,
                   SUM(a.penalty=1) AS late_count, SUM(a.overtime) AS total_overtime
                   FROM employees e LEFT JOIN attendance a ON e.e_id = a.e_id
                   GROUP BY e.e_id, e.e_name ORDER BY present_days DESC LIMIT 12"""); perf = cur.fetchall()
    conn.close()
    fig, axes = plt.subplots(1, 2, figsize=(17, 6)); fig.patch.set_facecolor('#0d1b2a'); style_axes(axes)
    if perf:
        names = [r['e_name'].split()[0] for r in perf]
        present = [int(r['present_days'] or 0) for r in perf]; late = [int(r['late_count'] or 0) for r in perf]; ot = [int(r['total_overtime'] or 0) for r in perf]
        axes[0].barh(names, present, color='#34d399', alpha=.9); axes[0].invert_yaxis()
        axes[0].set_title('Present Days — Top 12', fontweight='bold', fontsize=13); axes[0].set_xlabel('Days Present')
        sc = axes[1].scatter(present, late, c=ot, cmap='plasma', s=100, alpha=.85, edgecolors='#1e3448', linewidths=.8)
        cb = plt.colorbar(sc, ax=axes[1], label='Overtime (hrs)'); cb.ax.yaxis.label.set_color('#7a95b0'); cb.ax.tick_params(colors='#7a95b0')
        for i, r in enumerate(perf):
            axes[1].annotate(r['e_name'].split()[0], (present[i], late[i]), fontsize=7, color='#7a95b0', ha='center', va='bottom', xytext=(0,4), textcoords='offset points')
        axes[1].set_title('Present Days vs Late Arrivals', fontweight='bold', fontsize=13); axes[1].set_xlabel('Days Present'); axes[1].set_ylabel('Late Arrivals')
    else:
        for ax in axes: ax.text(0.5, 0.5, 'No data yet', ha='center', va='center', color='#7a95b0', transform=ax.transAxes, fontsize=14)
    plt.suptitle('Employee Performance', fontsize=17, fontweight='bold', color='#3b9eff', y=1.02); plt.tight_layout()
    return render_template('analytics.html', title='Employee Performance', chart=fig_to_b64(fig), active='performance', now=datetime.now())

@app.route('/api/today_stats')
@manager_required
def api_today_stats():
    today = datetime.now().date(); conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS c FROM employees"); total = cur.fetchone()['c']
    cur.execute("SELECT COUNT(DISTINCT e_id) AS c FROM attendance WHERE login_date=%s AND status!='Absent'", (today,)); present = cur.fetchone()['c']
    conn.close()
    return jsonify({'total': total, 'present': present, 'absent': total - present, 'rate': round(present/total*100,1) if total else 0})

if __name__ == '__main__':
    app.run(debug=True, port=5000)